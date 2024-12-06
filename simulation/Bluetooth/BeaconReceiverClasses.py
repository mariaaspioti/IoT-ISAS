import math
import random
import numpy as np

# Beacon class
class Beacon:
    def __init__(self, x=-1, y=-1, tx_power=-59, id=None):
        """
        Initialize a BLE Beacon.
        
        :param x: x-coordinate of the beacon.
        :param y: y-coordinate of the beacon.
        :param tx_power: Transmission power (RSSI at 1 meter).
        :param id: Identifier for the beacon.
        """
        self._x = x
        self._y = y
        self.tx_power = tx_power
        self.id = id or f"Beacon_{random.randint(1000, 9999)}"
        
    def transmit(self):
        """
        Simulates beacon transmitting signal.
        
        :return: Position and tx_power of the beacon.
        """
        return {"id": self.id, "tx_power": self.tx_power}
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def position(self):
        if self._x == -1 or self._y == -1:
            raise ValueError("Beacon position not set")
        return self._x, self._y

    @position.setter
    def position(self, value):
        self._x, self._y = value

# Receiver class
class Receiver:
    def __init__(self, x=0, y=0, noise=1):
        """
        Initialize the Receiver.
        
        :param x: Initial x-coordinate of the receiver.
        :param y: Initial y-coordinate of the receiver.
        :param noise: Random noise to simulate real-world RSSI fluctuations.
        """
        self.x = x
        self.y = y
        self.noise = noise
        self.used_beacons = []  # Attribute to store the list of beacons used for position estimation

    def calculate_rssi(self, beacon, distance):
        """
        Calculate RSSI based on distance to a beacon.
        
        :param beacon: The transmitting beacon.
        :param distance: Distance between receiver and beacon.
        :return: Simulated RSSI value.
        """
        path_loss_exponent = 2  # Free-space path loss exponent
        rssi = beacon['tx_power'] - 10 * path_loss_exponent * math.log10(distance)
        rssi += random.gauss(0, self.noise)  # Add random noise
        return rssi

    def calculate_position(self, beacon_positions, beacon_calls):
        """
        Calculate receiver's position based on RSSI from multiple beacons.
        
        :param beacon_positions: List of tuples with beacon positions (x, y).
        :param beacon_calls: List of dictionaries with beacon transmission data.
        :return: Estimated (x, y) position of the receiver.
        """
        distances = []
        positions = []
        self.used_beacons = []  # Reset the list of used beacons

        # Calculate distances from RSSI
        for i, beacon in enumerate(beacon_calls):
            beacon_position = beacon_positions[i]
            beacon_distance = math.sqrt((self.x - beacon_position[0])**2 + (self.y - beacon_position[1])**2)
            rssi = self.calculate_rssi(beacon, beacon_distance)
            # print("RSSI: ", rssi, "Distance: ", beacon_distance)
            if rssi < -100:
                continue
            distance = 10 ** ((beacon['tx_power'] - rssi) / (10 * 2))
            distances.append(distance)
            positions.append(beacon_position)
            self.used_beacons.append(beacon)  # Store the used beacon

        # Trilateration for position estimation
        A = []
        b = []

        for i in range(len(positions) - 1):
            x1, y1 = positions[i]
            x2, y2 = positions[i + 1]
            r1, r2 = distances[i], distances[i + 1]
            A.append([2 * (x2 - x1), 2 * (y2 - y1)])
            b.append([r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2])

        A = np.array(A)
        b = np.array(b)

        # Least squares solution
        position, *_ = np.linalg.lstsq(A, b, rcond=None)
        return position.flatten()

    def calculate_position_weighted(self, beacon_positions, beacon_calls):
        if len(beacon_positions) < 3:
            raise ValueError("At least 3 beacons are required for 2D trilateration.")
        
        distances = []
        weights = []
        self.used_beacons = []  # Reset the list of used beacons

        # Calculate distances and weights from RSSI
        for i, beacon in enumerate(beacon_calls):
            beacon_position = beacon_positions[i]
            true_distance = np.linalg.norm(np.array([self.x, self.y]) - np.array(beacon_position))
            rssi = self.calculate_rssi(beacon, true_distance)
            # ignore rssi if it is less than -100
            if rssi < -100:
                continue
            estimated_distance = 10 ** ((beacon['tx_power'] - rssi) / (10 * 2))
            weight = 1 / max(estimated_distance, 1e-3)  # Prevent division by zero
            weights.append(weight)
            distances.append(estimated_distance)
            self.used_beacons.append(beacon)  # Store the used beacon

        # Normalize weights
        weights = np.array(weights)
        weights /= np.sum(weights)

        # Construct weighted matrix system for trilateration
        A = []
        b = []

        for i in range(len(beacon_positions) - 1):
            x1, y1 = beacon_positions[i]
            x2, y2 = beacon_positions[i + 1]
            r1, r2 = distances[i], distances[i + 1]
            w1, w2 = weights[i], weights[i + 1]

            # Weighted coefficients
            A.append([(x2 - x1) * w1, (y2 - y1) * w2])
            b.append([
                w1 * (r1**2 - x1**2 - y1**2) - 
                w2 * (r2**2 - x2**2 - y2**2)
            ])

        A = np.array(A)
        b = np.array(b)

        # Solve the system using least squares
        position, *_ = np.linalg.lstsq(A, b, rcond=None)
        return position.flatten()

class StoredData:
    def __init__(self, beacons, preset_positions=None):
        self.beacons = beacons
        self.preset_positions = preset_positions
        
        # if preset positions are provided, 
        if preset_positions:
            # check if the number of preset positions match the number of beacons
            if len(preset_positions) != len(beacons):
                raise ValueError("Number of preset positions must match number of beacons")
            self.relate_positions()

    def relate_positions(self):
        # for each beacon, associate its ID with its position through a dictionary
        self.beacon_positions = {}
        for i, beacon in enumerate(self.beacons):
            # beacon.position = self.preset_positions[i]
            self.beacon_positions[beacon.id] = self.preset_positions[i]

    def get_beacon_position(self, beacon_id):
        return self.beacon_positions[beacon_id]
    
    def get_beacons_positions(self, beacons):
        return [self.get_beacon_position(beacon.id) for beacon in beacons]
    
    def set_presets(self, preset_positions):
        if len(preset_positions) != len(self.beacons):
            raise ValueError("Number of preset positions must match number of beacons")

        self.preset_positions = preset_positions
        self.relate_positions()

    @staticmethod
    def set_beacon_positions(storedData, beacons):
        '''Set the positions of the objects beacons and return a list of the positions'''
        beacon_positions = []
        for beacon in beacons:
            beacon.position  = storedData.get_beacon_position(beacon.id)
            beacon_positions.append(beacon.position)
        return beacon_positions

def get_parameters():
    # Simulation setup
    beacon1 = Beacon(tx_power=-59)
    beacon2 = Beacon(tx_power=-59)
    beacon3 = Beacon(tx_power=-59)
    # beacon4 = Beacon(tx_power=-59)
    # beacons = [beacon1, beacon2, beacon3, beacon4]
    beacons = [beacon1, beacon2, beacon3]
    beacon_positions = [[0, 0], [10, 0], [0, 10]] # known from Database

    storedData = StoredData(beacons, beacon_positions)

    receiver = Receiver(x=2.5, y=2.5, noise=2)
    return beacons, receiver, storedData

def main():
    iterations = 10
    estimated_positions = []
    beacons, receiver, storedData = get_parameters()
    for _ in range(iterations):
        beacon_positions = StoredData.set_beacon_positions(storedData, beacons)
        # Simulate the receiver determining its position
        beacon_calls = [beacon.transmit() for beacon in beacons]
        estimated_position = receiver.calculate_position(beacon_positions, beacon_calls)
        estimated_positions.append(estimated_position)

    # Determine average position
    avg_position = np.mean(estimated_positions, axis=0)
    print(f"Average Position: {avg_position}    True Position: {receiver.x, receiver.y}")



if __name__ == "__main__":
    main()