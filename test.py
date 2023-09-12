a = dict()
a[1] = [10, 20]
a[20] = [20, 30]
a[3] = [40, 50]
    
def lastTimeProcessRequest(timeRequestProcessing: dict) -> int:
    """ Take late time to process request in node

    Args:
        timeRequestProcessing (dict): dict contain time to process requests in node

    Returns:
        int: previous time to process
    """
    maxTime = 0
    for time in timeRequestProcessing.values():
        endTimeProcess = time[1] 
        if endTimeProcess> maxTime:
            maxTime = endTimeProcess
    return maxTime    
print(a[20])