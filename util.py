def isSmallerEqualNumber(firstNumber: int, secondNumber: int) -> int:
    return firstNumber <= secondNumber


def takeTimeStart(currentTime: int, time: int) -> int:
    """ Return time to start process request"""
    if currentTime > time:
        return currentTime, 0
    else:
        return time, time - currentTime
    
 # def calculateTimeFrame(routeNodeList: list ,requestList: list) -> int:
#     """ Return time using vehicle"""
#     waitTime = 0
#     movingTime = 0
#     for idxNode in range(len(routeNodeList) - 1):
#         node = routeNodeList[idxNode]
#         timeRequestProcessing = node.timeRequestProcessing
#         requestProcessStatus = node.requestProcessStatus
#         if len(timeRequestProcessing) != 0:
#             waitTime += node.timeCome - \
#                 timeRequestProcessing[requestProcessStatus[0]][0]
#         for idx in range(len(timeRequestProcessing) - 1):
#             waitTime += abs(timeRequestProcessing[requestProcessStatus[idx]]
#                             [1]) - timeRequestProcessing[requestProcessStatus[idx + 1]][0]

#         movingTime += routeNodeList[idxNode + 1].timeCome - node.timeGo

#     return waitTime + movingTime

# def totalUsingTime(firstRoute: Route, secondRoute: Route,) -> int:
#     firstRouteUsingTime = calculateUsingTime(firstRoute.routeNodeList)
#     secondRouteUsingTime = calculateUsingTime(secondRoute.routeNodeList)
#     return firstRouteUsingTime + secondRouteUsingTime
   