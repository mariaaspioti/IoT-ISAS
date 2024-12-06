import os

def run_transmission_simulation():
    transmission_simulation_path = os.path.join('Bluetooth', 'TransmissionSimulation.py')
    os.system(f'python {transmission_simulation_path}')

def run_bt_gps_interactive_simulation():
    bt_gps_simulation_path = os.path.join('BT-GPSInteractiveSimulation.py')
    os.system(f'python {bt_gps_simulation_path}')

if __name__ == "__main__":
    print("||=> Beacons transmit at intervals, receiver calculates RSSI, we estimate position, \n||=> and update backend at larger intervals with the average of the estimated positions accumulated until then.")
    print("=========")
    run_transmission_simulation()
    
    user_input = input("Do you want to run the BT-GPS Interactive Simulation? (yes/no): ")
    if user_input.lower() == 'yes' or user_input.lower() == 'y':
        run_bt_gps_interactive_simulation()
    else:
        print("BT-GPS Interactive Simulation was not run.")