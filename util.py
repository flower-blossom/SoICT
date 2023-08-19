def convertTimeToSecond(dateTime: str) -> int:
    timeList = [int(i) for i in dateTime.split(":")]
    return (timeList[0] * 60 + timeList[1]) * 60 + timeList[2]