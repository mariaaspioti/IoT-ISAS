import pygame
import pygame.gfxdraw
import numpy as np
import time
from BeaconReceiverClasses import Beacon, Receiver, StoredData

# Constants
WIDTH, HEIGHT = 800, 800
BEACON_RADIUS = 10
ESTIMATED_DOT_RADIUS = 5
TRUE_POSITION_RADIUS = 8
RECEIVER_TRAIL_RADIUS = 3
SCALE = 50  # Pixels per simulation unit
# SCALE = 150  # Pixels per simulation unit
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
    # Simulation setup
    num_beacons = 25
    beacons = [Beacon(tx_power=-59) for _ in range(num_beacons)]
    beacon_positions = [[0, 0], [2, 0], [0, 2], [4, 0], [0, 4], [2, 2], [2, 4], [4, 2], [4, 4],\
                        [6, 0], [0, 6], [6, 2], [2, 6], [6, 4], [4, 6], [6, 6],\
                        [8, 0], [0, 8], [8, 2], [2, 8], [8, 4], [4, 8], [8, 6], [6, 8], [8, 8]] # known from Database
    # beacon_positions = [[0, 0], [4, 0], [0, 4], [4, 4]] # known from Database

    storedData = StoredData(beacons) 
    storedData.set_presets(beacon_positions)

    receiver = Receiver(x=3.23, y=1.89, noise=1.5)
    return beacons, receiver, storedData

def scale_position(position):
    """Scale simulation units to screen units."""
    x, y = position
    return int(x * SCALE + OFFSET), int(HEIGHT - (y * SCALE + OFFSET))

def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Beacon Positioning Simulation")
    clock = pygame.time.Clock()

    # Simulation setup
    beacons, receiver, storedData = simulation_setup()
    beacon_positions = StoredData.set_beacon_positions(storedData, beacons)

    # Simulation parameters
    transmission_interval = 125  # in milliseconds
    estimation_interval = 125  # in milliseconds
    backend_update_interval = 1000  # in milliseconds
    simulation_duration = 20000  # in milliseconds
    dot_lifetime = 5000  # Lifetime of estimated dots in milliseconds
    flash_duration = 100  # Duration to flash the beacon in milliseconds

    # State variables
    start_time = pygame.time.get_ticks()
    last_transmit = start_time
    last_estimate = start_time
    last_backend_update = start_time
    beacon_flash_times = [0] * len(beacons)  # Track last flash time for each beacon

    true_position = np.array([receiver.x, receiver.y])
    accumulated_estimations = []
    backend_values = []
    pure_backend_values = []
    last_10_average_values = []
    running = True

    # Main loop
    while running:
        screen.fill(GRAY)

        current_time = pygame.time.get_ticks()
        # Draw beacons
        for i, pos in enumerate(beacon_positions):
            if current_time - beacon_flash_times[i] < flash_duration:
                color = LIGHT_GREEN  # Flash color
            else:
                color = GREEN  # Normal color
            pygame.draw.circle(screen, color, scale_position(pos), BEACON_RADIUS)

        # Draw true position
        pygame.draw.circle(screen, BLUE, scale_position(true_position), TRUE_POSITION_RADIUS)

        # Draw backend averaged positions
        backend_values = [(pos, timestamp) for pos, timestamp in backend_values if current_time - timestamp < dot_lifetime]
        for avg_pos, _ in backend_values:
            pygame.draw.circle(screen, RED, scale_position(avg_pos), ESTIMATED_DOT_RADIUS)
        
        # Draw the average of the last 10 backend values
        if len(pure_backend_values) >= 5:
            last_10_avg = np.mean([pos for pos, _ in pure_backend_values[-10:]], axis=0)
            last_10_average_values.append(last_10_avg)
            if len(last_10_average_values) > 1000:
                last_10_average_values.pop(0) # Remove the oldest value
            for last_10_avg_pos in last_10_average_values:
                pygame.draw.circle(screen, WHITE, scale_position(last_10_avg_pos), ESTIMATED_DOT_RADIUS)

        # Event handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            true_position[1] += 0.005
        if keys[pygame.K_s]:
            true_position[1] -= 0.005
        if keys[pygame.K_a]:
            true_position[0] -= 0.005
        if keys[pygame.K_d]:
            true_position[0] += 0.005

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update receiver position
        receiver.x, receiver.y = true_position

        # Simulate beacon transmission
        if current_time - last_transmit >= transmission_interval:
            beacon_calls = [beacon.transmit() for beacon in beacons]
            last_transmit = current_time
            beacon_flash_times = [current_time] * len(beacons)  # Update flash times

        # Simulate receiver estimation
        if current_time - last_estimate >= estimation_interval:
            estimated_position = receiver.calculate_position(beacon_positions, beacon_calls)
            accumulated_estimations.append(estimated_position)
            last_estimate = current_time

        # Backend update
        # if current_time - last_backend_update >= backend_update_interval:
        #     if accumulated_estimations:
        #         avg_position = np.mean(accumulated_estimations, axis=0)
        #         backend_values.append((avg_position, current_time))
        #         accumulated_estimations = []
        #     last_backend_update = current_time
        # Backend update
        if current_time - last_backend_update >= backend_update_interval:
            if accumulated_estimations:
                # Assign weights based on inverse distance from the average
                weights = []
                for pos in accumulated_estimations:
                    distance_to_avg = np.linalg.norm(pos - np.mean(accumulated_estimations, axis=0))
                    weight = 1 / max(distance_to_avg, 1e-3)  # Prevent division by zero
                    weights.append(weight)

                # Normalize weights
                weights = np.array(weights)
                weights /= np.sum(weights)

                # Compute weighted average
                weighted_average = np.average(accumulated_estimations, axis=0, weights=weights)
                backend_values.append((weighted_average, current_time))
                pure_backend_values.append((weighted_average, current_time))
                accumulated_estimations = []
            last_backend_update = current_time

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def run_simulation_trailed():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Beacon Positioning Simulation")
    clock = pygame.time.Clock()

    # Simulation setup
    beacons, receiver, storedData = simulation_setup()
    beacon_positions = StoredData.set_beacon_positions(storedData, beacons)

    # Simulation parameters
    transmission_interval = 125  # in milliseconds
    estimation_interval = 125  # in milliseconds
    backend_update_interval = 1000  # in milliseconds
    simulation_duration = 20000  # in milliseconds
    dot_lifetime = 5000  # Lifetime of estimated dots in milliseconds
    flash_duration = 100  # Duration to flash the beacon in milliseconds
    trail_lifetime = 100000  # Lifetime of receiver's trail in milliseconds

    # State variables
    start_time = pygame.time.get_ticks()
    last_transmit = start_time
    last_estimate = start_time
    last_backend_update = start_time
    beacon_flash_times = [0] * len(beacons)  # Track last flash time for each beacon

    true_position = np.array([receiver.x, receiver.y])
    accumulated_estimations = []
    backend_values = []
    pure_backend_values = []
    last_10_average_values = []
    receiver_trail = []  # List to store receiver's trail positions and timestamps
    running = True

    # Main loop
    while running:
        screen.fill(GRAY)

        current_time = pygame.time.get_ticks()

        # Draw beacons
        for i, pos in enumerate(beacon_positions):
            if current_time - beacon_flash_times[i] < flash_duration:
                color = LIGHT_GREEN  # Flash color
            else:
                color = GREEN  # Normal color
            pygame.draw.circle(screen, color, scale_position(pos), BEACON_RADIUS)

        # Draw true position
        pygame.draw.circle(screen, BLUE, scale_position(true_position), TRUE_POSITION_RADIUS)

        # Draw the receiver trail
        receiver_trail = [(pos, timestamp) for pos, timestamp in receiver_trail if current_time - timestamp < trail_lifetime]
        for trail_pos, timestamp in receiver_trail:
            alpha = max(0, 255 - int(255 * (current_time - timestamp) / trail_lifetime))  # Fade with age
            trail_color = (0, 0, 255, alpha)  # Semi-transparent blue
            pygame.gfxdraw.filled_circle(screen, *scale_position(trail_pos), RECEIVER_TRAIL_RADIUS, trail_color)

        # Draw backend averaged positions
        backend_values = [(pos, timestamp) for pos, timestamp in backend_values if current_time - timestamp < dot_lifetime]
        for avg_pos, _ in backend_values:
            pygame.draw.circle(screen, RED, scale_position(avg_pos), ESTIMATED_DOT_RADIUS)
        
        # Draw the average of the last 10 backend values
        if len(pure_backend_values) >= 5:
            last_10_avg = np.mean([pos for pos, _ in pure_backend_values[-10:]], axis=0)
            last_10_average_values.append(last_10_avg)
            if len(last_10_average_values) > 1000:
                last_10_average_values.pop(0)  # Remove the oldest value
            for last_10_avg_pos in last_10_average_values:
                pygame.draw.circle(screen, WHITE, scale_position(last_10_avg_pos), ESTIMATED_DOT_RADIUS)

        # Event handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            true_position[1] += 0.005
        if keys[pygame.K_s]:
            true_position[1] -= 0.005
        if keys[pygame.K_a]:
            true_position[0] -= 0.005
        if keys[pygame.K_d]:
            true_position[0] += 0.005

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update receiver position
        receiver.x, receiver.y = true_position

        # Add current position to receiver trail
        receiver_trail.append((true_position.copy(), current_time))

        # Simulate beacon transmission
        if current_time - last_transmit >= transmission_interval:
            beacon_calls = [beacon.transmit() for beacon in beacons]
            last_transmit = current_time
            beacon_flash_times = [current_time] * len(beacons)  # Update flash times

        # Simulate receiver estimation
        if current_time - last_estimate >= estimation_interval:
            estimated_position = receiver.calculate_position(beacon_positions, beacon_calls)
            accumulated_estimations.append(estimated_position)
            last_estimate = current_time

        # Backend update
        if current_time - last_backend_update >= backend_update_interval:
            if accumulated_estimations:
                # Assign weights based on inverse distance from the average
                weights = []
                for pos in accumulated_estimations:
                    distance_to_avg = np.linalg.norm(pos - np.mean(accumulated_estimations, axis=0))
                    weight = 1 / max(distance_to_avg, 1e-3)  # Prevent division by zero
                    weights.append(weight)

                # Normalize weights
                weights = np.array(weights)
                weights /= np.sum(weights)

                # Compute weighted average
                weighted_average = np.average(accumulated_estimations, axis=0, weights=weights)
                backend_values.append((weighted_average, current_time))
                pure_backend_values.append((weighted_average, current_time))
                accumulated_estimations = []
            last_backend_update = current_time

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_simulation_trailed()
