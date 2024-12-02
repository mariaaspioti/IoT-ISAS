import numpy as np
import time

from BeaconReceiverClasses import Beacon, Receiver, StoredData

def simulation_setup():
    # Simulation setup
    beacon1 = Beacon(tx_power=-59)
    beacon2 = Beacon(tx_power=-59)
    beacon3 = Beacon(tx_power=-59)
    beacon4 = Beacon(tx_power=-59)
    beacons = [beacon1, beacon2, beacon3, beacon4]
    beacon_positions = [[0, 0], [4, 0], [0, 4], [4, 4]] # known from Database

    storedData = StoredData(beacons) 
    storedData.set_presets(beacon_positions)

    receiver = Receiver(x=3.23, y=1.89, noise=2)
    return beacons, receiver, storedData

def estimate_receiver_position(beacons, receiver, storedData):
    '''Estimate the position of the receiver using the beacons and receiver objects'''

    # Set beacon positions
    beacon_positions = StoredData.set_beacon_positions(storedData, beacons)
    # Simulate the receiver determining its position
    beacon_calls = [beacon.transmit() for beacon in beacons]
    estimated_position = receiver.calculate_position(beacon_positions, beacon_calls)

    return estimated_position

def repeat_estimate():
    iterations = 10
    estimated_positions = []
    beacons, receiver, storedData = simulation_setup()
    for _ in range(iterations):
        estimated_position = estimate_receiver_position(beacons, receiver, storedData)
        estimated_positions.append(estimated_position)

    # Average estimated positions
    estimated_positions = np.array(estimated_positions)
    average_position = np.mean(estimated_positions, axis=0)
    error = np.linalg.norm(average_position - np.array([receiver.x, receiver.y]))
    print(f"Average estimated position: {average_position}   True position: {receiver.x, receiver.y}  Error: {error}")
    
def transmission_simulation():
    beacons, receiver, storedData = simulation_setup()
    beacon_positions = StoredData.set_beacon_positions(storedData, beacons)

    transmission_interval = 0.5  # Beacons transmit every 0.5 seconds
    estimation_interval = 0.52    # Receiver estimates position every 0.5 seconds
    backend_update_interval = 2  # Backend updates every 2 seconds
    simulation_duration = 20   # Run simulation for 20 seconds

    start_time = time.time()
    last_transmit = start_time
    last_estimate = start_time
    last_backend_update = start_time

    estimation_errors = []

    accumulated_estimations = []

    backend_values = []
    while time.time() - start_time < simulation_duration:
        current_time = time.time()

        # Beacon transmission
        if current_time - last_transmit >= transmission_interval:
            beacon_calls = [beacon.transmit() for beacon in beacons]
            print(f"[{(current_time - start_time):.2f}] 📶 Beacons Transmitted")
            last_transmit = current_time

        # Receiver estimation
        if current_time - last_estimate >= estimation_interval:
            estimated_position = receiver.calculate_position(beacon_positions, beacon_calls)
            print(f"[{(current_time - start_time):.2f}] Receiver Estimated Position: {estimated_position}")
            accumulated_estimations.append(estimated_position)
            last_estimate = current_time

        # Backend update $$Check weighted average
        if current_time - last_backend_update >= backend_update_interval:
            average_position = np.mean(accumulated_estimations, axis=0)
            backend_values.append(average_position)
            error = np.linalg.norm(average_position - np.array([receiver.x, receiver.y]))
            estimation_errors.append(error)
            print(f"[{(current_time - start_time):.2f}] ⚠️  Backend Updated with position: {backend_values[-1]}")
            # Clear accumulated estimations
            accumulated_estimations = []
            last_backend_update = current_time

        time.sleep(0.1)  # Small delay to reduce CPU usage

    # Final values send to backend
    # print(f"Backend values: {[value.tolist() for value in backend_values]}")
    print(f"| Number of backend updates: {len(backend_values)}")
    # Average estimated positions
    average_position = np.mean(backend_values, axis=0)
    # Average percentage error
    error = np.mean(estimation_errors)
    error_percentage = error / np.linalg.norm(np.array([receiver.x, receiver.y])) * 100
    print(f"| Average estimated position: {average_position}   True position: {receiver.x, receiver.y}")
    print(f"| Average Error percentage: {error_percentage:.2f}%")

def main():
    # repeat_estimate()
    transmission_simulation()
    

if __name__ == "__main__":
    main()