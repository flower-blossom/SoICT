from util import convertTimeToSecond

class Order:
    def __init__(self, sendId, receiveId, weight,
                 volume, sendLoading, receiveLoading,
                 sendTimeStart, sendTimeEnd, receiveTimeStart,
                 receiveTimeEnd) -> None:
        self.sendId = int(sendId)
        self.receiveId = int(receiveId)
        self.weight = float(weight)
        self.volume = float(volume)
        self.sendLoading = int(sendLoading)
        self.receiveLoading = int(receiveLoading)
        self.sendTimeStart = convertTimeToSecond(sendTimeStart)
        self.sendTimeEnd = convertTimeToSecond(sendTimeEnd)
        self.receiveTimeStart = convertTimeToSecond(receiveTimeStart)
        self.receiveTimeEnd = convertTimeToSecond(receiveTimeEnd)
