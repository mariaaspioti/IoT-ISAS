import numpy as np

class GPSReceiver:
    def __init__(self, x=0, y=0, error_std=4 / 1.96):
        """
        Initialize the GPS Receiver.
        
        :param x: True x-coordinate of the GPS receiver.
        :param y: True y-coordinate of the GPS receiver.
        :param error_std: Standard deviation of the GPS noise.
                          Default corresponds to a 95% confidence interval of ±4 meters.
        """
        self.x = x
        self.y = y
        self.error_std = error_std

    def simulate_reading(self):
        """
        Simulate a noisy GPS reading.
        
        :return: A tuple (noisy_x, noisy_y) representing the simulated position.
        """
        noisy_x = np.random.normal(loc=self.x, scale=self.error_std)
        noisy_y = np.random.normal(loc=self.y, scale=self.error_std)
        return noisy_x, noisy_y

    @property
    def true_position(self):
        """
        Get the true position of the receiver.
        
        :return: A tuple (x, y).
        """
        return self.x, self.y

    @true_position.setter
    def true_position(self, position):
        """
        Set the true position of the receiver.
        
        :param position: A tuple (x, y).
        """
        self.x, self.y = position


def main():
    """
    Main function to test GPSReceiver simulation with multiple readings.
    """
    # Initialize GPS Receiver at a true position
    gps_receiver = GPSReceiver(x=15, y=15)

    # Number of iterations for GPS simulation
    iterations = 10
    readings = []

    # Collect multiple noisy GPS readings
    for i in range(iterations):
        gps_reading = gps_receiver.simulate_reading()
        readings.append(gps_reading)
        print(f"Iteration {i + 1}: Simulated GPS Reading: {gps_reading}")

    # Calculate the average position from all readings
    avg_position = np.mean(readings, axis=0)

    # Output the results
    print(f"\nTrue Position: {gps_receiver.true_position}")
    print(f"Average Simulated Position: {avg_position}")


if __name__ == "__main__":
    main()
