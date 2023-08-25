class BollingerBand:
    def __init__(self, moving_average, std_dev):
        self.upper_band = moving_average + (2 * std_dev)
        self.lower_band = moving_average - (2 * std_dev)