import numpy as np
import time
from simpleGPS import GPSReceiver

def simulation_setup():
    """
    Sets up the simulation environment with a GPS receiver.
    """
    # Initialize the GPS receiver at a true position
    gps_receiver = GPSReceiver(x=15, y=15)
    return gps_receiver

def repeat_estimate():
    """
    Repeats the GPS position estimation process multiple times and calculates the average position and error.
    """
    iterations = 10
    estimated_positions = []
    gps_receiver = simulation_setup()

    for _ in range(iterations):
        # Simulate a GPS reading
        estimated_position = gps_receiver.simulate_reading()
        estimated_positions.append(estimated_position)

    # Average estimated positions
    estimated_positions = np.array(estimated_positions)
    average_position = np.mean(estimated_positions, axis=0)
    error = np.linalg.norm(average_position - np.array(gps_receiver.true_position))
    print(f"Average estimated position: {average_position}   True position: {gps_receiver.true_position}  Error: {error}")

def gps_transmission_simulation():
    """
    Simulates GPS position estimations and backend updates over time.
    """
    gps_receiver = simulation_setup()

    transmission_interval = 0.5  # GPS updates every 0.5 seconds
    backend_update_interval = 2  # Backend updates every 2 seconds
    simulation_duration = 20  # Run simulation for 20 seconds

    start_time = time.time()
    last_transmit = start_time
    last_backend_update = start_time

    accumulated_estimations = []
    backend_values = []
    estimation_errors = []

    while time.time() - start_time < simulation_duration:
        current_time = time.time()

        # GPS reading (transmission)
        if current_time - last_transmit >= transmission_interval:
            estimated_position = gps_receiver.simulate_reading()
            print(f"[{(current_time - start_time):.2f}] 📡 GPS Reading: {estimated_position}")
            accumulated_estimations.append(estimated_position)
            last_transmit = current_time

        # Backend update
        if current_time - last_backend_update >= backend_update_interval:
            if accumulated_estimations:
                average_position = np.mean(accumulated_estimations, axis=0)
                backend_values.append(average_position)
                error = np.linalg.norm(average_position - np.array(gps_receiver.true_position))
                estimation_errors.append(error)
                print(f"[{(current_time - start_time):.2f}] ⚠️  Backend Updated with position: {average_position}")
                # Clear accumulated estimations
                accumulated_estimations = []
            last_backend_update = current_time

        time.sleep(0.1)  # Small delay to reduce CPU usage

    # Final values sent to backend
    print(f"| Number of backend updates: {len(backend_values)}")
    # Average estimated positions
    average_position = np.mean(backend_values, axis=0)
    # Average error
    error = np.mean(estimation_errors)
    error_percentage = error / np.linalg.norm(np.array(gps_receiver.true_position)) * 100
    print(f"| Average estimated position: {average_position}   True position: {gps_receiver.true_position}")
    print(f"| Average Error percentage: {error_percentage:.2f}%")

def main():
    """
    Main function to run the GPS transmission simulation.
    """
    # repeat_estimate()
    gps_transmission_simulation()

if __name__ == "__main__":
    main()
