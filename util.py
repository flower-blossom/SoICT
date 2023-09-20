def isSmallerEqualNumber(firstNumber: int, secondNumber: int) -> int:
    return firstNumber <= secondNumber


def takeTimeStart(currentTime: int, time: int) -> int:
    """ Return time to start process request"""
    if currentTime > time:
        return currentTime, 0
    else:
        return time, time - currentTime