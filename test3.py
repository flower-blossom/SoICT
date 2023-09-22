# PYTHON
# PYTHON
from typing import NoReturn
from copy import deepcopy
from random import choice, seed
import time
seed(1)


def isSmallerEqualNumber(firstNumber: int, secondNumber: int) -> int:
    return firstNumber <= secondNumber


def takeTimeStart(currentTime: int, time: int) -> int:
    """ Return time to start process request"""
    if currentTime > time:
        return currentTime, 0
    else:
        return time, time - currentTime


class DataModel:
    """
    Contains lists about description of problem
    """

    def __init__(self,
                 distanceMatrix: list,
                 vehicleList: list,
                 requestList: list,):
        self.distanceMatrix = distanceMatrix
        self.vehicleList = vehicleList
        self.requestList = requestList


class RouteNode:
    def __init__(self,
                 idHub: int,
                 timeCome: int,
                 timeGo: int,
                 requestProcessStatus: list,
                 timeRequestProcessing=list(),
                 locatioOfProcessRequest=list(),
                 ) -> None:
        self.idHub = idHub
        self.timeCome = timeCome
        self.timeGo = timeGo
        self.requestProcessStatus = requestProcessStatus
        self.timeRequestProcessing = timeRequestProcessing
        self.locatioOfProcessRequest = locatioOfProcessRequest

    def __repr__(self) -> str:
        return f"idHub: {self.idHub + 1} \n requestProcessStatus: {self.requestProcessStatus} \n {self.timeCome} \n {self.timeGo} \n timeRequestProcessing: {self.timeRequestProcessing} "


class Route:
    """_summary_
    """

    def __init__(self,
                 routeNodeList: list,
                 vehicleDict: dict,
                 orderOfRequestProcessed: list = []):
        self.routeNodeList = routeNodeList
        self.vehicleDict = vehicleDict
        self.orderOfRequestProcessed = orderOfRequestProcessed
        self.requestProcess = set()
        self.locationOfProcessRequest: list = None


WEIGHTOFREQUEST = 10**9
WEIGHTOFVEHICLE = 10**6
WEIGHTOFTIME = 1/10**3


def updateRequestProcess(routeList: list) -> NoReturn:
    for routeObject in routeList:
        for order in routeObject.orderOfRequestProcessed:
            routeObject.requestProcess.add(abs(order))


def totalCostFuction(routeList: list,
                     quantityOfRequest: int,
                     quantityOfVehicle: int) -> int:
    totalCost = 0
    costTime = 0
    numberOfVehicleServe = 0
    listOrderServe = set()

    for routeObject in routeList:
        costTime += routeObject.routeNodeList[-1].timeCome - \
            routeObject.routeNodeList[0].timeCome
        numberOfVehicleServe += 1
        for order in routeObject.orderOfRequestProcessed:
            listOrderServe.add(abs(order))

    totalCost += WEIGHTOFREQUEST*len(listOrderServe)/quantityOfRequest
    totalCost -= WEIGHTOFVEHICLE*numberOfVehicleServe/quantityOfVehicle
    totalCost -= WEIGHTOFTIME*costTime
    return totalCost


class Solution():
    """
    """

    def __init__(self, routeList: list, locationOfVehicle: list):
        self.routeList = routeList
        self.positionOfProcessingRequest: list = None
        self.locationOfVehicle: list = locationOfVehicle
        self.weightOfCost = dict()
        self.costFuction = 0

    def updateCostFuction(self, dataModel: DataModel):
        quantityOfRequest = len(dataModel.requestList) - 1
        quantityOfVehicle = len(dataModel.vehicleList)
        self.weightOfCost["request"] = WEIGHTOFREQUEST/quantityOfRequest
        self.weightOfCost["vehicle"] = WEIGHTOFVEHICLE/quantityOfVehicle
        self.costFuction = totalCostFuction(self.routeList,
                                            quantityOfRequest,
                                            quantityOfVehicle)

    def objective(self):
        return self.costFuction


def conflictVehicleCapacity(vehicleDict: dict, sequenceRequestProcessed: list, requestList: list) -> bool:
    vehicleCapacity = vehicleDict["capacity"]
    vehicleVolume = vehicleDict["volume"]
    currentCapacity = 0
    currentVolume = 0

    for statusRequest in sequenceRequestProcessed:
        requestDict = requestList[abs(statusRequest)]
        if statusRequest > 0:
            currentCapacity += requestDict["weight"]
            currentVolume += requestDict["volume"]
        else:
            currentCapacity -= requestDict["weight"]
            currentVolume -= requestDict["volume"]
        if currentVolume > vehicleVolume or currentCapacity > vehicleCapacity:
            return True
    return False


def estimateTimeMoving(distance: int, velocity: int) -> int:
    return int(distance/velocity*3600)


def pickVehicle(candidateVehicle: list,
                vehicleList: list,
                locationOfVehicle: list,
                numberOfRoute: int) -> dict:
    vehiclePicked = choice(candidateVehicle)
    candidateVehicle.remove(vehiclePicked)
    vehicleObject = vehicleList[vehiclePicked]
    locationOfVehicle[vehiclePicked] = numberOfRoute
    return vehicleObject


def addFirstNodeRoute(newRoute: Route,) -> NoReturn:
    vehicleDict = newRoute.vehicleDict
    startVehicleNode = RouteNode(idHub=vehicleDict["startIdHub"],
                                 timeCome=vehicleDict["startTime"],
                                 timeGo=vehicleDict["startTime"],
                                 requestProcessStatus=[],
                                 timeRequestProcessing=list(),)
    newRoute.routeNodeList.append(startVehicleNode)


def addEndNode(routeNodeList: list, vehicleInfoDict: dict, distanceMatrix: list, weightToDue=-1) -> int:
    lastNode = routeNodeList[-1]
    startHub = vehicleInfoDict["startIdHub"]
    if startHub != lastNode.idHub:
        distance = distanceMatrix[lastNode.idHub][startHub]
        movingTime = estimateTimeMoving(
            distance, vehicleInfoDict["velocity"])
        timeToComeBackHub = lastNode.timeGo + movingTime
        comeBackNode = RouteNode(startHub, timeToComeBackHub, timeToComeBackHub, [],
                                 timeRequestProcessing=dict())
        routeNodeList.append(comeBackNode)
        return weightToDue * (vehicleInfoDict["endTime"] - timeToComeBackHub)
    else:
        return weightToDue*(vehicleInfoDict["endTime"] - lastNode.timeRequestProcessing[-1][1])


def checkValidTimePartRoute(index: int, nextOrderOfRequest: list, lastNode: RouteNode,
                            vehicleDict: dict, requestList: list, distanceMatrix: list) -> (bool, list):
    usingTime = 0
    estimatePartNodeList = [deepcopy(lastNode)]
    endTimeVehicle = vehicleDict["endTime"]
    lastNode = estimatePartNodeList[-1]

    for indexRequest in range(index, len(nextOrderOfRequest)):
        statusRequest = nextOrderOfRequest[indexRequest]
    for statusRequest in nextOrderOfRequest:
        usingTime += processRequest(statusRequest, lastNode, estimatePartNodeList,
                                    vehicleDict, requestList, distanceMatrix)
        lastNode = estimatePartNodeList[-1]
        if isSmallerEqualNumber(lastNode.timeGo, endTimeVehicle) is False:
            return False, None, 0
        stopCondition, waitTime = performTheProcessRequest(
            lastNode, requestList)
        if stopCondition is False:
            return False, None, 0
        usingTime += waitTime
    usingTime += addEndNode(estimatePartNodeList, vehicleDict, distanceMatrix)

    return isSmallerEqualNumber(estimatePartNodeList[-1].timeGo, endTimeVehicle), estimatePartNodeList, usingTime


def findPlaceToInsert(statusRequest: int, orderOfRequestProcessed: list,
                      beforeNode: RouteNode, vehicleDict: dict,
                      requestList: list, distanceMatrix: list) -> (int, int):
    minUsingTime = float("inf")
    idxToInsert = -1
    startIdx = 0

    if statusRequest < 0:
        startIdx = orderOfRequestProcessed.index(abs(statusRequest)) + 1

    # index of delivery < index pickup
    for index in range(startIdx, len(orderOfRequestProcessed) + 1):
        orderOfRequestProcessed.insert(index, statusRequest)
        if conflictVehicleCapacity(vehicleDict, orderOfRequestProcessed, requestList) is False:
            conditionRoute, _, usingTime = checkValidTimePartRoute(index,
                                                                   orderOfRequestProcessed,
                                                                   beforeNode,
                                                                   vehicleDict,
                                                                   requestList,
                                                                   distanceMatrix)
            if conditionRoute is True:
                if usingTime < minUsingTime:
                    minUsingTime = usingTime
                    idxToInsert = index
        orderOfRequestProcessed.pop(index)
    return idxToInsert, minUsingTime


def addNewRequest(route: Route,
                  vehicleDict: dict,
                  requestIndexCandidate: list,
                  requestList: list,
                  distanceMatrix: list,
                  ) -> bool:
    """
    try to add new request 
    """
    routeNodeList = route.routeNodeList
    orderOfRequestProcessed = route.orderOfRequestProcessed

    # Tổng thời gian di chuyển và chờ đợi = thời gian sử dụng
    minCost = float("inf")
    stopCondition = False
    selectedRequest = -1
    idxInsertPickUp = 0
    idxInsertDelivery = 0

    for requestIdx in requestIndexCandidate:
        pickupStatus = requestIdx
        deliveryStatus = -requestIdx

        # try to insert pickup request
        beforeNode = routeNodeList[-1]
        idxPickUp, _ = findPlaceToInsert(pickupStatus, orderOfRequestProcessed, beforeNode,
                                         vehicleDict, requestList, distanceMatrix)
        if idxPickUp != -1:
            orderOfRequestProcessed.insert(idxPickUp, pickupStatus)
            # try to insert delivery request
            beforeNode = routeNodeList[-1]
            idxDelivery, cost = findPlaceToInsert(deliveryStatus, orderOfRequestProcessed, beforeNode,
                                                  vehicleDict, requestList, distanceMatrix)
            # print(cost)
            orderOfRequestProcessed.pop(idxPickUp)
            if cost < minCost:
                selectedRequest = requestIdx
                idxInsertPickUp = idxPickUp
                idxInsertDelivery = idxDelivery
                minCost = cost

    if selectedRequest == -1:
        return stopCondition
    requestIndexCandidate.remove(selectedRequest)
    orderOfRequestProcessed.insert(idxInsertPickUp, selectedRequest)
    orderOfRequestProcessed.insert(idxInsertDelivery, -selectedRequest)


def processRequest(statusRequest: int,
                   lastNode: RouteNode,
                   routeNodeList: list,
                   vehicleInfoDict: dict,
                   requestList: list,
                   distanceMatrix: list) -> int:
    """
    Create node to process request
    """
    usingTime = 0
    currentHub = lastNode.idHub
    requestObject = requestList[abs(statusRequest)]

    nextHub = 0
    if statusRequest > 0:
        nextHub = requestObject["pickupIdHub"]
    if statusRequest < 0:
        nextHub = requestObject["deliveryIdHub"]

    if nextHub == currentHub:
        # add request to last node
        lastNode.requestProcessStatus.append(statusRequest)
    else:
        # create and moving to new node
        distance = distanceMatrix[currentHub][nextHub]
        movingTime = estimateTimeMoving(
            distance, vehicleInfoDict["velocity"])
        timeGoToHub = lastNode.timeGo + movingTime
        usingTime += timeGoToHub
        newNode = RouteNode(idHub=nextHub,
                            timeCome=timeGoToHub,
                            timeGo=timeGoToHub,
                            requestProcessStatus=[statusRequest],
                            timeRequestProcessing=list(),)
        routeNodeList.append(newNode)
    return usingTime


def performTheProcessRequest(node: RouteNode, requestList: list) -> (bool, int):
    """ 
    Try to update time to delivery or pickup request and time 
    to go out current hub 
    """

    usingTime = 0
    requestProcessStatus = node.requestProcessStatus
    timeRequestProcessing = node.timeRequestProcessing
    timeRequestProcessing.clear()
    timeCome = node.timeCome
    lastTimeAction = node.timeCome
    startProcessTime = 0
    endProcessTime = 0
    loadingTime = 0
    waitTime = 0

    for requestStatusIdx in requestProcessStatus:
        requestInfoDict = requestList[abs(requestStatusIdx)]
        if len(timeRequestProcessing) == 0:
            # is first request process
            if requestStatusIdx > 0:
                # pickUp request
                startProcessTime, waitTime = takeTimeStart(
                    timeCome, requestInfoDict["pickupTime"][0])
                if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                    return False, 0
                loadingTime = requestInfoDict["pickupLoadingTime"]
            else:
                # delivery request
                startProcessTime, waitTime = takeTimeStart(
                    timeCome, requestInfoDict["deliveryTime"][0])
                if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                    return False, 0
                loadingTime = requestInfoDict["deliveryLoadingTime"]
        else:
            lastTimeRequest = timeRequestProcessing[-1][1]
            if requestStatusIdx > 0:
                # pickUp request
                startProcessTime, waitTime = takeTimeStart(
                    lastTimeRequest, requestInfoDict["pickupTime"][0])
                if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                    return False, 0
                loadingTime = requestInfoDict["pickupLoadingTime"]
            else:
                # delivery request
                startProcessTime, waitTime = takeTimeStart(
                    lastTimeRequest, requestInfoDict["deliveryTime"][0])
                if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                    return False, 0
                loadingTime = requestInfoDict["deliveryLoadingTime"]

        usingTime += waitTime
        endProcessTime = startProcessTime + loadingTime

        timeRequestProcessing.append([startProcessTime, endProcessTime])
        lastTimeAction = endProcessTime
    node.timeGo = lastTimeAction
    return True, usingTime


def getNewRoute(vehicleDict: dict,
                requestInfoList: list,
                candidateRequests: list,
                distanceMatrix: list,
                timeStart: int) -> Route:
    newRoute = Route(list(), vehicleDict, list())
    addFirstNodeRoute(newRoute)

    while True:
        stopCondition = addNewRequest(newRoute, vehicleDict, candidateRequests,
                                      requestInfoList, distanceMatrix)

        if stopCondition is False:
            break
        if time.time() - timeStart > 290:
            break
    _, newRoute.routeNodeList, _ = checkValidTimePartRoute(0,
                                                           newRoute.orderOfRequestProcessed,
                                                           newRoute.routeNodeList[-1],
                                                           vehicleDict,
                                                           requestInfoList,
                                                           distanceMatrix)
    return newRoute


def main(solutionArr: list,
         dataModel: DataModel,
         candidateVehicle: list,
         candidateRequests: list,
         locationOfVehicle: list,
         timeStart: int
         ) -> NoReturn:
    """ Create new Route through loop"""

    distanceMatrix = dataModel.distanceMatrix
    vehicleList = dataModel.vehicleList
    requestList = dataModel.requestList
    numberOfRoute = 0
    while True:
        vehicleDict = pickVehicle(
            candidateVehicle, vehicleList, locationOfVehicle, numberOfRoute)
        newRoute = getNewRoute(vehicleDict,
                               requestList,
                               candidateRequests,
                               distanceMatrix,
                               timeStart)
        solutionArr.append(newRoute)
        numberOfRoute += 1
        if len(candidateVehicle) == 0 or len(candidateRequests) == 0:
            break
        if time.time() - timeStart > 290:
            break



class initalSolution:
    def __init__(self, timeLimit=300) -> None:
        self.timeLimit = timeLimit
    
    

def initalSolutionByVehicle(self,dataModel: DataModel) -> Solution:
    timeStart = time.time()
    solutionArr = list()
    candidateRequests = [i for i in range(1, len(dataModel.requestList))]
    candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
    locationOfVehicle = [-1 for _ in range(len(dataModel.vehicleList))]
    main(solutionArr, dataModel, candidateVehicle,
         candidateRequests, locationOfVehicle, timeStart)
    initialSolution = Solution(solutionArr, locationOfVehicle)
    initialSolution.updateCostFuction(dataModel)
    return initialSolution

    # partOfObjective, vnd


def solByRequest(self,
                 solutionArr: list,
                 dataModel: DataModel,
                 candidateVehicle: list,
                 candidateRequests: list,
                 locationOfVehicle: list,
                 timeStart: int
                 ) -> NoReturn:
    """ Create new Route through loop"""

    distanceMatrix = dataModel.distanceMatrix
    vehicleList = dataModel.vehicleList
    requestList = dataModel.requestList
    numberOfRoute = 0

    # Tổng thời gian di chuyển và chờ đợi = thời gian sử dụng
    minCost = float("inf")
    stopCondition = False
    selectedRequest = -1
    idxInsertPickUp = 0
    idxInsertDelivery = 0

    for requestIdx in candidateRequests:
        pickupStatus = requestIdx
        deliveryStatus = -requestIdx

        # try to insert pickup request
        for routeObject in solutionArr:
            
            idxPickUp, _ = findPlaceToInsert(pickupStatus, orderOfRequestProcessed, beforeNode,
                                            vehicleDict, requestList, distanceMatrix)
            if idxPickUp != -1:
                orderOfRequestProcessed.insert(idxPickUp, pickupStatus)
                # try to insert delivery request
                beforeNode = routeNodeList[-1]
                idxDelivery, cost = findPlaceToInsert(deliveryStatus, orderOfRequestProcessed, beforeNode,
                                                    vehicleDict, requestList, distanceMatrix)
                # print(cost)
                orderOfRequestProcessed.pop(idxPickUp)
                if cost < minCost:
                    selectedRequest = requestIdx
                    idxInsertPickUp = idxPickUp
                    idxInsertDelivery = idxDelivery
                    minCost = cost

    if selectedRequest == -1:
        return stopCondition
    requestIndexCandidate.remove(selectedRequest)
    orderOfRequestProcessed.insert(idxInsertPickUp, selectedRequest)
    orderOfRequestProcessed.insert(idxInsertDelivery, -selectedRequest)    


def initalSolutionByRequest(self, dataModel: DataModel) -> Solution:
    timeStart = time.time()
    candidateRequests = [i for i in range(1, len(dataModel.requestList))]
    solutionArr = [Route(list(), vehicleDict, list()) for vehicleDict in dataModel.vehicleList]
    locationOfVehicle = [-1 for _ in range(len(dataModel.vehicleList))]
    
    solByRequest(solutionArr, dataModel, candidateRequests, locationOfVehicle, timeStart)
    initialSolution = Solution(solutionArr, locationOfVehicle)
    initialSolution.updateCostFuction(dataModel)
    return initialSolution




def createLocationOfRequests(tempSol, requestList: list) -> NoReturn:
    routeList = tempSol.routeList
    locationOfRequests = [-1 for _ in range(0, len(requestList) - 1)]
    numberOfRoute = 0
    for routeObject in routeList:
        for order in routeObject.orderOfRequestProcessed:
            locationOfRequests[abs(order)] = numberOfRoute
        numberOfRoute += 1
    return locationOfRequests

    # local search with function is number of request and time


def insertRequestToNewRoute(newRequest: int,
                            route: Route,
                            requestList: list,
                            distanceMatrix: list) -> (bool, int):
    """
    Insert request to new route if valid
    """

    pickupStatus = newRequest
    deliveryStatus = -newRequest
    routeNodeList = route.routeNodeList
    vehicleDict = route.vehicleDict
    orderOfRequestProcessed = route.orderOfRequestProcessed

    usingTime = -1
    idxDelivery = idxPickUp = -1
    idxPickUp, _ = findPlaceToInsert(pickupStatus, orderOfRequestProcessed, routeNodeList,
                                     vehicleDict, requestList, distanceMatrix)
    if idxPickUp != -1:
        print(f"idxPickUp: {idxPickUp}")
        orderOfRequestProcessed.insert(idxPickUp, pickupStatus)
        # try to insert delivery request
        idxDelivery, usingTime = findPlaceToInsert(deliveryStatus, orderOfRequestProcessed, routeNodeList,
                                                   vehicleDict, requestList, distanceMatrix)
        print(f"idxDelivery: {idxDelivery}")
        orderOfRequestProcessed.pop(idxPickUp)

    if idxDelivery == -1 or idxPickUp == -1:
        return False, usingTime
    orderOfRequestProcessed.insert(idxPickUp, pickupStatus)
    orderOfRequestProcessed.insert(idxDelivery, -deliveryStatus)
    route.requestProcess.add(newRequest)
    return True, usingTime


def singlePairedInsertion(tempSol: list, requestList: list, distanceMatrix: list) -> NoReturn:
    routeList = tempSol.routeList
    for idxCurentRoute in range(len(routeList)):
        curentRoute = routeList[idxCurentRoute]
        for idxAnotherRoute in range(len(routeList)):
            # print(f"curentRoute: {idxCurentRoute}")
            # print(f"idxAnotherRoute: {idxAnotherRoute}")
            if idxCurentRoute == idxAnotherRoute:
                pass
            else:
                anotherRoute = routeList[idxAnotherRoute]

                for request in anotherRoute.requestProcess:
                    insertCondition, _ = insertRequestToNewRoute(request, curentRoute,
                                                                 requestList, distanceMatrix)
                    if insertCondition is True:
                        anotherRoute.requestProcess.remove(request)
                        anotherRoute.orderOfRequestProcessed.remove(request)
                        anotherRoute.orderOfRequestProcessed.remove(-request)
                        print("Insert complete")


def findIdxOfRequestInOrder(request: int, orderOfRequestProcessed: list) -> NoReturn:
    indexOfOldPickupRequest = orderOfRequestProcessed.index(request)
    indexOfOldPickupDelivery = orderOfRequestProcessed.index(-request)
    return indexOfOldPickupRequest, indexOfOldPickupDelivery


def deletePairRequestInOrder(indexOfOldPickupRequest: int, indexOfOldPickupDelivery: int,
                             orderOfRequestProcessed: list) -> NoReturn:
    orderOfRequestProcessed.pop(indexOfOldPickupRequest)
    orderOfRequestProcessed.pop(indexOfOldPickupDelivery - 1)


def insertRequestToRoute(request: int, indexOfOldPickupRequest: int, indexOfOldPickupDelivery: int,
                         orderOfRequestProcessed: list, requestProcess: dict) -> NoReturn:
    requestProcess.add(request)
    orderOfRequestProcessed.insert(indexOfOldPickupRequest, request)
    orderOfRequestProcessed.insert(indexOfOldPickupDelivery, -request)


def requestExchangeOperator(newRequest: int, oldRequest: int, route: Route,
                            requestList: list, distanceMatrix: list) -> bool:
    orderOfRequestProcessed = route.orderOfRequestProcessed
    indexOfOldPickupRequest, indexOfOldPickupDelivery = findIdxOfRequestInOrder(oldRequest,
                                                                                orderOfRequestProcessed)

    # temporary delete oldRequest
    usingTime = -1
    deletePairRequestInOrder(indexOfOldPickupRequest, indexOfOldPickupDelivery,
                             orderOfRequestProcessed)
    insertCondition, usingTime = insertRequestToNewRoute(newRequest, route,
                                                         requestList, distanceMatrix)
    route.requestProcess.remove(oldRequest)
    if insertCondition is False:
        insertRequestToRoute(oldRequest, indexOfOldPickupRequest, indexOfOldPickupDelivery,
                             orderOfRequestProcessed, route.requestProcess)
    return usingTime


def swapRequestInTwoRoute(firstRoute: Route, secondRoute: Route,
                          requestList: list, distanceMatrix: list) -> bool:
    stopCondition = False
    currentUsingTime = totalUsingTime(firstRoute, secondRoute)
    for request in firstRoute.requestProcess:
        for secondRouteRequest in secondRoute.requestProcess:
            usingFirstRouteTime = requestExchangeOperator(secondRouteRequest, request,
                                                          firstRoute, requestList, distanceMatrix)
            usingSecondRouteTime = requestExchangeOperator(request, secondRouteRequest,
                                                           secondRoute, requestList, distanceMatrix)
        if usingSecondRouteTime + usingFirstRouteTime < currentUsingTime:
            print(
                f"Can Swap old using new: {usingSecondRouteTime + usingFirstRouteTime}, old: {currentUsingTime} ")
            _, firstRoute.routeNodeList = checkValidTimePartRoute(firstRoute.orderOfRequestProcessed,
                                                                  firstRoute.routeNodeList[-1],
                                                                  firstRoute.vehicleDict,
                                                                  requestList,
                                                                  distanceMatrix)
            _, firstRoute.routeNodeList = checkValidTimePartRoute(secondRoute.orderOfRequestProcessed,
                                                                  secondRoute.routeNodeList[-1],
                                                                  secondRoute.vehicleDict,
                                                                  requestList,
                                                                  distanceMatrix)
            currentUsingTime = totalUsingTime(firstRoute, secondRoute)
            stopCondition = True

    return stopCondition


def swapRequestOperator(tempSol: Solution, requestList: list, distanceMatrix: list) -> NoReturn:
    routeList = tempSol.routeList
    stopCondition = True
    while stopCondition:
        for idxCurentRoute in range(len(routeList)):
            currentRoute = routeList[idxCurentRoute]
            for idxAnotherRoute in range(len(routeList)):
                # print(f"curentRoute: {idxCurentRoute}")
                # print(f"idxAnotherRoute: {idxAnotherRoute}")
                if idxCurentRoute == idxAnotherRoute:
                    pass
                else:
                    # anotherRoute = routeList[idxAnotherRoute]
                    swapCondition = swapRequestInTwoRoute(currentRoute, routeList[idxAnotherRoute],
                                                          requestList, distanceMatrix)
                    if swapCondition is True:
                        stopCondition = stopCondition


def localSearch(sol, dataModel):
    tempSol = deepcopy(sol)
    requestList = dataModel.requestList
    distanceMatrix = dataModel.distanceMatrix
    updateRequestProcess(tempSol.routeList)
    candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
    locationOfVehicle = tempSol.locationOfVehicle.copy()
    # locationOfRequests = createLocationOfRequests(
    #     tempSol, requestList)
    # print(locationOfRequests)
    # singlePairedInsertion(tempSol, requestList, distanceMatrix)
    swapRequestOperator(tempSol, requestList, distanceMatrix)
    return tempSol
    # localsearch through route Node
    # while True:


def convertTimeToSecond(dateTime: str) -> int:
    timeList = [int(i) for i in dateTime.split(":")]
    return (timeList[0] * 60 + timeList[1]) * 60 + timeList[2]


def convertSecondsToHours(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_format = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return time_format


def createInfoVehicle(vehicleInfo: str) -> dict:
    infoList = vehicleInfo.split()
    infoDict = {
        "startIdHub": int(infoList[0]) - 1,
        "startTime": convertTimeToSecond(infoList[1]),
        "endTime": convertTimeToSecond(infoList[2]),
        "capacity": float(infoList[3]),
        "volume": float(infoList[4]),
        "velocity": float(infoList[5]),
    }
    return infoDict


def createInfoRequest(requestInfo: str) -> dict:
    infoList = requestInfo.split()
    infoDict = {
        "pickupIdHub": int(infoList[0]) - 1,
        "deliveryIdHub": int(infoList[1]) - 1,
        "weight": float(infoList[2]),
        "volume": float(infoList[3]),
        "pickupLoadingTime": int(infoList[4]),
        "deliveryLoadingTime": int(infoList[5]),
        "pickupTime": [convertTimeToSecond(infoList[6]), convertTimeToSecond(infoList[7])],
        "deliveryTime": [convertTimeToSecond(infoList[8]), convertTimeToSecond(infoList[9])],
    }
    return infoDict


def readInputFile(data: list):
    currentIndex = 0
    numberOfHub = int(data[currentIndex])
    currentIndex += 1

    orderList = []
    orderList.append([])
    vehicleList = []
    distanceMatrix = []

    for hubNumber in range(currentIndex, currentIndex + numberOfHub):
        arr = data[hubNumber]
        distanceMatrix.append(list(map(int, arr.split())))
    # distanceMatrix = np.array(distanceMatrix)
    currentIndex += numberOfHub

    numberOfVehicle = int(data[currentIndex])
    currentIndex += 1

    for orderIdx in range(currentIndex, currentIndex + numberOfVehicle):
        vehicleList.append(createInfoVehicle(data[orderIdx]))
    currentIndex += numberOfVehicle

    numberOfOrder = int(data[currentIndex])
    currentIndex += 1

    for orderIdx in range(currentIndex, currentIndex + numberOfOrder):
        orderList.append(createInfoRequest(data[orderIdx]))

    return DataModel(distanceMatrix, vehicleList, orderList)


def writeVehicleNotUse(vehicle: dict):
    time = convertSecondsToHours(vehicle["startTime"])
    print(1)
    print(f"{vehicle['startIdHub'] + 1} 0 {time} {time}")


def writeRoute(route: Route):
    print(len(route.routeNodeList))
    for node in route.routeNodeList:
        print(f"{node.idHub + 1} {len(node.requestProcessStatus)} {convertSecondsToHours(node.timeCome)} {convertSecondsToHours(node.timeGo)}")
        for idx in range(len(node.requestProcessStatus)):
            # for request in node.requestProcessStatus:
            # for timeProcess in timeRequestProcessing[request][0]:
            print(
                f"{abs(node.requestProcessStatus[idx])} {convertSecondsToHours(node.timeRequestProcessing[idx][0])}")


def writeOutFile(solution: Solution, dataModel: DataModel):
    vehicleList = dataModel.vehicleList
    locationOfVehicle = solution.locationOfVehicle
    routeList = solution.routeList
    for idx, locationRoute in enumerate(locationOfVehicle):
        if locationRoute == -1:
            writeVehicleNotUse(vehicleList[idx])
        else:
            writeRoute(routeList[locationRoute])


# data = []
# while True:
#     line = input()
#     if line:
#         data.append(line)
#     else:
#         break

with open("data//50h_50v_1000r.txt") as f_obj:
    data = [line.strip("\n") for line in f_obj.readlines()]

dataModel = readInputFile(data)

time1 = time.time()
a = initalSolutionByVehicle(dataModel)
# localSearch(a, dataModel)
print(time.time()-time1)
print(a.costFuction)


# print(dataModel.requestList[113])

# def checkTimeConstraint(route, vehicleList):
#     for node in route:

# def checkHub(route, requestList):
#     for node in route.routeNodeList:
#         for statusRequest in node.requestProcessStatus:
#             if statusRequest > 0:
#                 idHub = requestList[abs(statusRequest)]["pickupIdHub"]
#             else:
#                 idHub = requestList[abs(statusRequest)]["deliveryIdHub"]
#             if node.idHub != idHub:
#                 print(f"wrong hub trueHub: {route.idHub}, currentHub: {idHub}")

# def test(route):
#     for node in route.routeNodeList:
#         if node.idHub == 5:
#             print(node)

# def checkSol(sol: Solution, dataModel):
#     requestList = dataModel.requestList
#     # check time constraint
#     route = sol.routeList
#     for route in sol.routeList:
#         checkHub(route, requestList)
#         test(route)
# checkSol(a, dataModel)
# for
# for i in a.routeList:
#     print(i.orderOfRequestProcessed)

# writeOutFile(a, dataModel)
