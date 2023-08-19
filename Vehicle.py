from util import convertTimeToSecond

class Vehicle:
    def __init__(self, identity, timeStart, timeEnd, 
                 capacity, volume, velocity) -> None:
        self.identity = int(identity)
        self.timeStart = convertTimeToSecond(timeStart)
        self.timeEnd = convertTimeToSecond(timeEnd)
        self.capacity = float(capacity)
        self.volume = float(volume)
        self.velocity = float(velocity)
