import numpy as np

class Radar():
    def __init__(self, r, theta) -> None:
        self.r = r
        self.theta = theta
        self.z_k = np.array([r*np.cos(theta), r*np.sin(theta)]).reshape(2,-1)
        pass

    def jacobian():
        pass

def main():
    radar = Radar(1, 10)
    print(radar.z_k)
    pass

if __name__ == "__main__":
    main()