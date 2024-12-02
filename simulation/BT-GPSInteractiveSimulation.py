import pygame
import pygame.gfxdraw
import numpy as np
import time
from Bluetooth.BeaconReceiverClasses import Beacon, Receiver, StoredData
from GPS.simpleGPS import GPSReceiver

# Constants
WIDTH, HEIGHT = 800, 800
BEACON_RADIUS = 10
ESTIMATED_DOT_RADIUS = 5
TRUE_POSITION_RADIUS = 8
RECEIVER_TRAIL_RADIUS = 3
SCALE = 50  # Pixels per simulation unit
OFFSET = 50  # Offset for visualization borders

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
GRAY = (128, 128, 128)

def simulation_setup():
    num_beacons = 25
    beacons = [Beacon(tx_power=-59) for _ in range(num_beacons)]
    beacon_positions = [
        [0, 0], [2, 0], [0, 2], [4, 0], [0, 4], [2, 2], [2, 4], [4, 2], [4, 4],
        [6, 0], [0, 6], [6, 2], [2, 6], [6, 4], [4, 6], [6, 6],
        [8, 0], [0, 8], [8, 2], [2, 8], [8, 4], [4, 8], [8, 6], [6, 8], [8, 8]
    ]
    storedData = StoredData(beacons)
    storedData.set_presets(beacon_positions)
    receiver = Receiver(x=3.23, y=1.89, noise=1.5)
    gps_receiver = GPSReceiver(x=10.0, y=10.0, error_std=4 / 1.96)  # GPS receiver starts at (10, 10)
    return beacons, receiver, gps_receiver, storedData

def scale_position(position):
    x, y = position
    return int(x * SCALE + OFFSET), int(HEIGHT - (y * SCALE + OFFSET))

def handle_input(true_position):
    keys = pygame.key.get_pressed()
    # walking speed of 1.4 m/s, and the simulation runs at 2x speed
    movement_per_frame = 0.009

    if keys[pygame.K_w]:
        true_position[1] += movement_per_frame
    if keys[pygame.K_s]:
        true_position[1] -= movement_per_frame
    if keys[pygame.K_a]:
        true_position[0] -= movement_per_frame
    if keys[pygame.K_d]:
        true_position[0] += movement_per_frame

def draw_elements(screen, beacon_positions, beacon_flash_times, current_time, true_position, 
                  backend_values, pure_backend_values, last_10_average_values, 
                  door_positions, receiver_trail=None, trail_lifetime=100000):
    screen.fill(GRAY)

    # Calculate the boundaries of the rectangle
    min_x = min(pos[0] for pos in beacon_positions)
    max_x = max(pos[0] for pos in beacon_positions)
    min_y = min(pos[1] for pos in beacon_positions)
    max_y = max(pos[1] for pos in beacon_positions)

    # Extend the boundary a few units
    min_x -= 1
    max_x += 1
    min_y -= 1
    max_y += 1

    # Scale the boundaries
    top_left = scale_position((min_x, max_y))
    bottom_right = scale_position((max_x, min_y))

    # Draw the rectangle
    pygame.draw.rect(screen, WHITE, (*top_left, bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]), 2)

    # Draw doors and check if true position passed through
    for door_pos in door_positions:
        if door_pos[2] == 'horizontal':
            door_top_left = scale_position((door_pos[0] - 0.5, door_pos[1] + 0.1))
            door_bottom_right = scale_position((door_pos[0] + 0.5, door_pos[1] - 0.1))
        else:
            door_top_left = scale_position((door_pos[0] - 0.1, door_pos[1] + 0.5))
            door_bottom_right = scale_position((door_pos[0] + 0.1, door_pos[1] - 0.5))

        pygame.draw.rect(screen, RED, (*door_top_left, door_bottom_right[0] - door_top_left[0], door_bottom_right[1] - door_top_left[1]))

    # Draw beacons
    for i, pos in enumerate(beacon_positions):
        color = LIGHT_GREEN if current_time - beacon_flash_times[i] < 100 else GREEN
        pygame.draw.circle(screen, color, scale_position(pos), BEACON_RADIUS)

    # Draw true position
    pygame.draw.circle(screen, BLUE, scale_position(true_position), TRUE_POSITION_RADIUS)

    # Draw receiver trail if applicable
    if receiver_trail is not None:
        receiver_trail = [(pos, timestamp) for pos, timestamp in receiver_trail if current_time - timestamp < trail_lifetime]
        for trail_pos, timestamp in receiver_trail:
            alpha = max(0, 255 - int(255 * (current_time - timestamp) / trail_lifetime))  # Fade with age
            trail_color = (0, 0, 255, alpha)
            pygame.gfxdraw.filled_circle(screen, *scale_position(trail_pos), RECEIVER_TRAIL_RADIUS, trail_color)

    # Draw backend averaged positions
    backend_values = [(pos, timestamp) for pos, timestamp in backend_values if current_time - timestamp < 5000]
    for avg_pos, _ in backend_values:
        pygame.draw.circle(screen, RED, scale_position(avg_pos), ESTIMATED_DOT_RADIUS)

    # Draw last 10 averages
    if len(pure_backend_values) >= 10:
        last_10_avg = np.mean([pos for pos, _ in pure_backend_values[-10:]], axis=0)
        last_10_average_values.append(last_10_avg)
        if len(last_10_average_values) > 1500:
            last_10_average_values.pop(0)
        for avg_pos in last_10_average_values:
            pygame.draw.circle(screen, WHITE, scale_position(avg_pos), ESTIMATED_DOT_RADIUS)

def update_backend(accumulated_estimations, backend_values, pure_backend_values, current_time):
    if accumulated_estimations:
        weights = np.array([1 / max(np.linalg.norm(pos - np.mean(accumulated_estimations, axis=0)), 1e-3) 
                            for pos in accumulated_estimations])
        weights /= np.sum(weights)
        weighted_average = np.average(accumulated_estimations, axis=0, weights=weights)
        backend_values.append((weighted_average, current_time))
        pure_backend_values.append((weighted_average, current_time))
        accumulated_estimations.clear()

def calculate_percentage_error(true_position, estimated_position):
    distance = np.linalg.norm(np.array(true_position) - np.array(estimated_position))
    percentage_error = (distance / np.linalg.norm(true_position)) * 100
    return percentage_error

def run_simulation(trail_enabled=False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Beacon Positioning Simulation")
    clock = pygame.time.Clock()

    # Initialize font
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 25)
    
    # Setup
    beacons, receiver, gps_receiver, storedData = simulation_setup()
    beacon_positions = StoredData.set_beacon_positions(storedData, beacons)

    # Calculate the boundaries of the rectangle
    min_x = min(pos[0] for pos in beacon_positions)
    max_x = max(pos[0] for pos in beacon_positions)
    min_y = min(pos[1] for pos in beacon_positions)
    max_y = max(pos[1] for pos in beacon_positions)

    # Extend the boundary a few units
    min_x -= 1
    max_x += 1
    min_y -= 1
    max_y += 1

    # Define door positions (relative to the rectangle)
    door_positions = [
        ((min_x + max_x) / 2, min_y, 'horizontal'),  # Bottom center
        ((min_x + max_x) / 2, max_y, 'horizontal'),  # Top center
        (min_x, (min_y + max_y) / 2, 'vertical'),    # Left center
        (max_x, (min_y + max_y) / 2, 'vertical')     # Right center
    ]

    # Parameters
    transmission_interval = 250 / 2 # double the time
    estimation_interval = 250 / 2 # double the time
    backend_update_interval = 2000 / 2 # double the time
    trail_lifetime = 30000 if trail_enabled else 0

    # State
    start_time = pygame.time.get_ticks()
    last_transmit = start_time
    last_estimate = start_time
    last_backend_update = start_time
    beacon_flash_times = [0] * len(beacons)
    true_position = np.array([receiver.x, receiver.y])
    accumulated_estimations = []
    backend_values = []
    pure_backend_values = []
    last_10_average_values = []
    receiver_trail = [] if trail_enabled else None
    running = True
    tracking_method = "Bluetooth"  # Initial tracking method
    inside = True  # Initial state is inside
    in_door = False  # Initial state is not in a door

    while running:
        current_time = pygame.time.get_ticks()
        handle_input(true_position)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update receiver position
        receiver.x, receiver.y = true_position
        gps_receiver.x, gps_receiver.y = true_position

        # Add to trail
        if trail_enabled:
            receiver_trail.append((true_position.copy(), current_time))

        # Simulate beacon transmission
        if current_time - last_transmit >= transmission_interval:
            beacon_calls = [beacon.transmit() for beacon in beacons]
            last_transmit = current_time
            beacon_flash_times = [current_time] * len(beacons)

        # Check if true position passed through a door
        door_passed = False
        for door_pos in door_positions:
            if door_pos[2] == 'horizontal':
                door_top_left = scale_position((door_pos[0] - 0.5, door_pos[1] + 0.1))
                door_bottom_right = scale_position((door_pos[0] + 0.5, door_pos[1] - 0.1))
            else:
                door_top_left = scale_position((door_pos[0] - 0.1, door_pos[1] + 0.5))
                door_bottom_right = scale_position((door_pos[0] + 0.1, door_pos[1] - 0.5))

            true_x, true_y = scale_position(true_position)
            if door_top_left[0] <= true_x <= door_bottom_right[0] and door_top_left[1] <= true_y <= door_bottom_right[1]:
                door_passed = True
                break

        # Switch tracking method if passed through a door
        if door_passed:
            if not in_door:
                inside = not inside
                tracking_method = "Bluetooth" if inside else "GPS"
                in_door = True
        else:
            in_door = False

        # Simulate receiver estimation
        if current_time - last_estimate >= estimation_interval:
            if tracking_method == "Bluetooth":
                estimated_position = receiver.calculate_position(beacon_positions, beacon_calls)
            else:
                estimated_position = gps_receiver.simulate_reading()

            accumulated_estimations.append(estimated_position)
            last_estimate = current_time

        # Backend update
        if current_time - last_backend_update >= backend_update_interval:
            update_backend(accumulated_estimations, backend_values, pure_backend_values, current_time)
            last_backend_update = current_time

        draw_elements(screen, beacon_positions, beacon_flash_times, current_time, 
                      true_position, backend_values, pure_backend_values, 
                      last_10_average_values, door_positions, receiver_trail, trail_lifetime)

        # Calculate elapsed time in seconds
        elapsed_time = (current_time - start_time) // 1000
        # Calculate the inner simulation time, which is double the real time
        inner_time = (current_time - start_time) // 2000

        # Calculate percentage error
        if len(last_10_average_values) > 0 and len(receiver_trail) > 0:
            last_white_dot = last_10_average_values[-1]
            # corresponding_trail_pos = receiver_trail[-1][0]  # Assuming the last trail position corresponds to the last white dot
            # find the shortest euclidean distance between the last white dot and all trail positions
            corresponding_trail_pos = min(receiver_trail, key=lambda x: np.linalg.norm(np.array(x[0]) - np.array(last_white_dot)))[0]
            percentage_error = calculate_percentage_error(corresponding_trail_pos, last_white_dot)
        else:
            percentage_error = 0

        # Render the elapsed time and percentage error as text
        timer_text = font.render(f'True Time: {elapsed_time}s', True, BLACK)
        inner_timer_text = font.render(f'Inner Time: {inner_time}s', True, BLACK)
        tracking_method_text = font.render(f'Tracking Method: {tracking_method}', True, BLACK)
        error_text = font.render(f'Error: {percentage_error:.2f}%', True, BLACK)
        screen.blit(timer_text, (10, 10))
        screen.blit(inner_timer_text, (10, 40))
        screen.blit(tracking_method_text, (10, 70))
        screen.blit(error_text, (10, 100))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_simulation(trail_enabled=True)