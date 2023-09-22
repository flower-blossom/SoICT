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
                 idx: int,
                 idHub: int,
                 timeCome: int,
                 timeGo: int,
                 requestProcessStatus: list,
                 timeRequestProcessing=list(),
                 ) -> None:
        self.idx = idx
        self.idHub = idHub
        self.timeCome = timeCome
        self.timeGo = timeGo
        self.requestProcessStatus = requestProcessStatus
        self.timeRequestProcessing = timeRequestProcessing
        # self.locationOfProcessRequest: RouteNode = locationOfProcessRequest

    def __repr__(self) -> str:
        return f"idHub: {self.idHub + 1} \n requestProcessStatus: {self.requestProcessStatus} \n {self.timeCome} \n {self.timeGo} \n timeRequestProcessing: {self.timeRequestProcessing} "


class Route:
    """_summary_
    """

    def __init__(self,
                 routeNodeList: RouteNode,
                 vehicleDict: dict,
                 orderOfRequestProcessed: RouteNode = []):
        self.routeNodeList = routeNodeList
        self.vehicleDict = vehicleDict
        self.orderOfRequestProcessed = orderOfRequestProcessed
        self.requestProcess = set()
        self.locationOfProcessRequest: RouteNode = dict()


WEIGHTOFREQUEST = 10**9
WEIGHTOFVEHICLE = 10**6
WEIGHTOFTIME = 1/10**3


def updateRequestProcess(routeList: RouteNode) -> NoReturn:
    for routeObject in routeList:
        for order in routeObject.orderOfRequestProcessed:
            routeObject.requestProcess.add(abs(order))


def totalCostFuction(routeList: RouteNode,
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

    def __init__(self, routeList: RouteNode, locationOfVehicle: RouteNode):
        self.routeList = routeList
        self.positionOfProcessingRequest: RouteNode = None
        self.locationOfVehicle: RouteNode = locationOfVehicle
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


def conflictVehicleCapacity(vehicleDict: dict, sequenceRequestProcessed: RouteNode, requestList: list) -> bool:
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
        if currentVolume >= vehicleVolume or currentCapacity >= vehicleCapacity:
            return True
    return False


def estimateTimeMoving(distance: int, velocity: int) -> int:
    return int(distance/velocity*3600)


def pickVehicle(candidateVehicle: RouteNode,
                vehicleList: RouteNode,
                locationOfVehicle: RouteNode,
                numberOfRoute: int) -> dict:
    vehiclePicked = choice(candidateVehicle)
    candidateVehicle.remove(vehiclePicked)
    vehicleObject = vehicleList[vehiclePicked]
    locationOfVehicle[vehiclePicked] = numberOfRoute
    return vehicleObject


class Greedy:
    def __init__(self, timeLimit=290) -> None:
        self.timeLimit = timeLimit

    def addFirstNodeRoute(self, newRoute: Route,) -> NoReturn:
        vehicleDict = newRoute.vehicleDict
        startVehicleNode = RouteNode(idx=0,
                                     idHub=vehicleDict["startIdHub"],
                                     timeCome=vehicleDict["startTime"],
                                     timeGo=vehicleDict["startTime"],
                                     requestProcessStatus=set(),
                                     timeRequestProcessing=list(),)
        newRoute.routeNodeList.append(startVehicleNode)

    def createFirstNode(self, route: Route) -> RouteNode:
        vehicleDict = route.vehicleDict
        return RouteNode(idx=0,
                         idHub=vehicleDict["startIdHub"],
                         timeCome=vehicleDict["startTime"],
                         timeGo=vehicleDict["startTime"],
                         requestProcessStatus=set(),
                         timeRequestProcessing=list(),)

    def addEndNode(self, routeNodeList: RouteNode, vehicleInfoDict: dict, distanceMatrix: RouteNode) -> int:
        lastNode = routeNodeList[-1]
        startHub = vehicleInfoDict["startIdHub"]
        timeRequestProcessing = lastNode.timeRequestProcessing
        lastTime = 0
        if startHub != lastNode.idHub:
            # create nod to moving new hub
            distance = distanceMatrix[lastNode.idHub][startHub]
            movingTime = estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeToComeBackHub = lastNode.timeGo + movingTime
            comeBackNode = RouteNode(lastNode.idx + 1, startHub, timeToComeBackHub, timeToComeBackHub, [],
                                     timeRequestProcessing=list())
            routeNodeList.append(comeBackNode)
            lastTime = timeToComeBackHub
        else:
            if len(timeRequestProcessing) != 0:
                lastTime = lastNode.timeRequestProcessing[-1][1]
            else:
                lastTime = lastNode.timeGo
        return (vehicleInfoDict["endTime"] - lastTime)

    def checkValidTimePartRoute(self, startIdx: int, nextOrderOfRequest: list, beforeNode: RouteNode,
                                vehicleDict: dict, requestList: RouteNode, distanceMatrix: RouteNode,
                                weightOfWaitTime=1, weightOfMovingTime=1, weightToDue=1) -> (bool, RouteNode):
        """
        Check part of Route and return if is true
        """
        # locationOfProcessRequest = []
        usingTime = 0
        endTimeVehicle = vehicleDict["endTime"]
        estimatePartNodeList = [deepcopy(beforeNode)]
        beforeNode = estimatePartNodeList[-1]

        for indexRequest in range(startIdx, len(nextOrderOfRequest)):
            statusRequest = nextOrderOfRequest[indexRequest]
        # for statusRequest in nextOrderOfRequest:
            usingTime += weightOfMovingTime * self.processRequest(statusRequest, beforeNode, estimatePartNodeList,
                                                             vehicleDict, requestList, distanceMatrix)
            beforeNode = estimatePartNodeList[-1]
            if isSmallerEqualNumber(beforeNode.timeGo, endTimeVehicle) is False:
                return False, None, 0
            stopCondition, waitTime = self.performTheProcessRequest(
                beforeNode, requestList)
            if stopCondition is False:
                return False, None, 0
            usingTime += weightOfWaitTime * waitTime
        usingTime += weightToDue * \
            self.addEndNode(estimatePartNodeList, vehicleDict, distanceMatrix)
        return isSmallerEqualNumber(estimatePartNodeList[-1].timeGo, endTimeVehicle), estimatePartNodeList, usingTime

    def findPlaceToInsert(self,
                          idx, locationOfProcessRequest, statusRequest: int, currentNodeList: list,
                          route: Route,
                          requestList: RouteNode,
                          distanceMatrix: RouteNode) -> (int, int, RouteNode):

        # routeNodeList = route.routeNodeList
        vehicleDict = route.vehicleDict
        orderOfRequestProcessed = route.orderOfRequestProcessed
        # locationOfProcessRequest = route.locationOfProcessRequest
        minUsingTime = float("inf")
        idxToInsert = -1
        bestNodeList = 0
        changeIdx = abs(route.routeNodeList[0].idx - currentNodeList[0].idx)

        # index of delivery < index pickup
        for index in range(idx, len(orderOfRequestProcessed) + 1):
            if len(locationOfProcessRequest) == 0 or index == 0:
                beforeNode = self.createFirstNode(route)
                # beforeNode = addFirstNodeRoute(route)
            else:
                # changeIdx = abs(route.routeNodeList[0].idx - currentNodeList[0].idx)
                beforeRequest = locationOfProcessRequest[orderOfRequestProcessed[index - 1]]
                beforeNode = currentNodeList[beforeRequest - changeIdx]

            orderOfRequestProcessed.insert(index, statusRequest)

            if conflictVehicleCapacity(vehicleDict, orderOfRequestProcessed, requestList) is False:
                conditionRoute, tempNodeList, usingTime = self.checkValidTimePartRoute(index,
                                                                                  orderOfRequestProcessed,
                                                                                  beforeNode,
                                                                                  vehicleDict,
                                                                                  requestList,
                                                                                  distanceMatrix)
                if conditionRoute is True:
                    if usingTime < minUsingTime:
                        minUsingTime = usingTime
                        idxToInsert = index
                        bestNodeList = tempNodeList
            orderOfRequestProcessed.pop(index)
        return idxToInsert, minUsingTime, bestNodeList

    def updateLocationProcessRequest(self, locationOfProcessRequest: dict, nodelist: list,) -> NoReturn:
        for node in nodelist:
            for requestStatus in node.requestProcessStatus:
                locationOfProcessRequest[requestStatus] = node.idx

    def addNewRequest(self,
                      route: Route,
                      requestIndexCandidate: RouteNode,
                      requestInfoList: RouteNode,
                      distanceMatrix: RouteNode,
                      ) -> bool:
        """
        try to add new request 
        """

        orderOfRequestProcessed = route.orderOfRequestProcessed
        routeNodeList = route.routeNodeList
        locationOfProcessRequest = route.locationOfProcessRequest

        # Tổng thời gian di chuyển và chờ đợi = thời gian sử dụng
        minCost = float("inf")
        selectedRequest = -1
        idxInsertPickUp = 0
        idxInsertDelivery = 0

        for requestIdx in requestIndexCandidate:
            pickupStatus = requestIdx
            deliveryStatus = -requestIdx

            # try to insert pickup request
            idxPickUp, _, tempNodePickUp = self.findPlaceToInsert(0, locationOfProcessRequest, pickupStatus, routeNodeList,
                                                             route, requestInfoList, distanceMatrix)
            if idxPickUp != -1:
                tempLocation = dict()
                self.updateLocationProcessRequest(tempLocation, tempNodePickUp)
                orderOfRequestProcessed.insert(idxPickUp, pickupStatus)

                # try to insert delivery request
                idxDelivery, cost, _ = self.findPlaceToInsert(idxPickUp + 1, tempLocation, deliveryStatus, tempNodePickUp,
                                                         route, requestInfoList,
                                                         distanceMatrix)
                orderOfRequestProcessed.pop(idxPickUp)
                # locationOfProcessRequest.pop(pickupStatus)
                if cost < minCost:
                    selectedRequest = requestIdx
                    idxInsertPickUp = idxPickUp
                    idxInsertDelivery = idxDelivery
                    minCost = cost

        if selectedRequest == -1:
            return False

        requestIndexCandidate.remove(selectedRequest)
        orderOfRequestProcessed.insert(idxInsertPickUp, selectedRequest)

        if len(locationOfProcessRequest) == 0:
            beforeNode = routeNodeList[-1]
        else:
            if idxInsertPickUp != 0:
                requestBefore = orderOfRequestProcessed[idxInsertPickUp - 1]
                beforeNode = routeNodeList[locationOfProcessRequest[requestBefore]]
            else:
                beforeNode = self.createFirstNode(route)

        orderOfRequestProcessed.insert(idxInsertDelivery, -selectedRequest)
        _, tempList, _ = self.checkValidTimePartRoute(0, orderOfRequestProcessed,
                                                 routeNodeList[0], route.vehicleDict,
                                                 requestInfoList, distanceMatrix)
        route.routeNodeList = tempList
        self.updateLocationProcessRequest(locationOfProcessRequest, routeNodeList)

    def processRequest(self,
                       statusRequest: int,
                       lastNode: Route,
                       routeNodeList: list,
                       vehicleInfoDict: dict,
                       requestList: list,
                       distanceMatrix: list,
                       ) -> int:
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
            lastNode.requestProcessStatus.add(statusRequest)
        else:
            # create and moving to new node
            distance = distanceMatrix[currentHub][nextHub]
            movingTime = estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeGoToHub = lastNode.timeGo + movingTime
            usingTime += movingTime
            newNode = RouteNode(idx=lastNode.idx + 1,
                                idHub=nextHub,
                                timeCome=timeGoToHub,
                                timeGo=timeGoToHub,
                                requestProcessStatus={statusRequest},
                                timeRequestProcessing=list(),)
            routeNodeList.append(newNode)
        return usingTime

    def performTheProcessRequest(self, node: RouteNode, requestList: RouteNode) -> (bool, int):
        """ 
        Try to update time to delivery or pickup request and time 
        to go out current hub 
        """

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

            endProcessTime = startProcessTime + loadingTime

            timeRequestProcessing.append([startProcessTime, endProcessTime])
            lastTimeAction = endProcessTime
        node.timeGo = lastTimeAction
        return True, waitTime

    def getNewRoute(self,
                    vehicleDict: dict,
                    requestInfoList: RouteNode,
                    candidateRequests: RouteNode,
                    distanceMatrix: RouteNode,
                    timeStart: int) -> Route:
        newRoute = Route(list(), vehicleDict, list())
        self.addFirstNodeRoute(newRoute)

        while True:
            stopCondition = self.addNewRequest(newRoute, candidateRequests,
                                               requestInfoList, distanceMatrix)

            if stopCondition is False:
                break
            if time.time() - timeStart > self.timeLimit:
                break
        return newRoute

    def main(self, solutionArr: RouteNode,
             dataModel: DataModel,
             candidateVehicle: RouteNode,
             candidateRequests: RouteNode,
             locationOfVehicle: RouteNode,
             timeStart: int) -> NoReturn:
        """ Create new Route through loop"""

        distanceMatrix = dataModel.distanceMatrix
        vehicleList = dataModel.vehicleList
        requestList = dataModel.requestList
        numberOfRoute = 0

        while True:
            vehicleDict = pickVehicle(
                candidateVehicle, vehicleList, locationOfVehicle, numberOfRoute)
            solutionArr.append(self.getNewRoute(vehicleDict,
                                                requestList,
                                                candidateRequests,
                                                distanceMatrix,
                                                timeStart))
            # solutionArr.append(newRoute)
            numberOfRoute += 1
            if len(candidateVehicle) == 0 or len(candidateRequests) == 0:
                break
            if time.time() - timeStart > self.timeLimit:
                break

    def solve(self, dataModel: DataModel) -> Solution:
        timeStart = time.time()
        solutionArr = list()
        candidateRequests = [i for i in range(1, len(dataModel.requestList))]
        candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
        locationOfVehicle = [-1 for _ in range(len(dataModel.vehicleList))]
        self.main(solutionArr, dataModel, candidateVehicle,
             candidateRequests, locationOfVehicle, timeStart)
        initialSolution = Solution(solutionArr, locationOfVehicle)
        initialSolution.updateCostFuction(dataModel)
        return initialSolution


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


def readInputFile(data: RouteNode):
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
        node.requestProcessStatus = list(node.requestProcessStatus)
        for idx in range(len(node.requestProcessStatus)):
            # for request in node.requestProcessStatus:
            # for timeProcess in timeRequestProcessing[request][0]:
            print(
                f"{abs(node.requestProcessStatus[idx])} {convertSecondsToHours(node.timeRequestProcessing[idx][0])}")
        # for idx in range(len(node.requestProcessStatus)):
        #     # for request in node.requestProcessStatus:
        #     # for timeProcess in timeRequestProcessing[request][0]:
        #     print(
        #         f"{abs(node.requestProcessStatus[idx])} {convertSecondsToHours(node.timeRequestProcessing[idx][0])}")


def writeOutFile(solution: Solution, dataModel: DataModel):
    vehicleList = dataModel.vehicleList
    locationOfVehicle = solution.locationOfVehicle
    routeList = solution.routeList
    for idx, locationRoute in enumerate(locationOfVehicle):
        if locationRoute == -1:
            writeVehicleNotUse(vehicleList[idx])
        else:
            writeRoute(routeList[locationRoute])


with open("data//10h_10v_50r.txt") as f_obj:
    data = [line.strip("\n") for line in f_obj.readlines()]

dataModel = readInputFile(data)

time1 = time.time()
a = Greedy.solve(dataModel)
print(time.time()-time1)
print(a.costFuction)
# writeOutFile(a, dataModel)

# localSearch(a, dataModel)


# def checkHub(route, requestList):
#     for node in route.routeNodeList:
#         for statusRequest in node.requestProcessStatus:
#             if statusRequest > 0:
#                 idHub = requestList[abs(statusRequest)]["pickupIdHub"]
#             else:
#                 idHub = requestList[abs(statusRequest)]["deliveryIdHub"]
#             if node.idHub != idHub:
#                 print(f"wrong hub trueHub: {route.idHub}, currentHub: {idHub}")


# def checkConfliCapacity(route, idx, requestList):
#     if conflictVehicleCapacity(route.vehicleDict, route.orderOfRequestProcessed, requestList) is True:
#         print("Conflict weight in route: ", idx + 1)


# def checkDuplicate(routeNodeList, numberOfReuest):
#     checkList = [0 for i in range(numberOfReuest)]
#     for route in routeNodeList:
#         for note in route.routeNodeList:
#             for request in note.requestProcessStatus:
#                 checkList[abs(request)] += 1
#                 if checkList[abs(request)] > 2:
#                     print(f"{abs(request)}")
#     print(checkList)

# def checkSol(sol: Solution, dataModel):
#     requestList = dataModel.requestList
#     # check time constraint
#     for idx, route in enumerate(sol.routeList):
#         checkConfliCapacity(route, idx, requestList)
#     # for route in sol.routeList:
#     #     checkHub(route, requestList)
#     #     test(route)
# checkSol(a, dataModel)
# route = a.routeList[a.locationOfVehicle[19]]
# print(route)
# checkDuplicate(a.routeList, len(dataModel.requestList))
# print(conflictVehicleCapacity(route.vehicleDict, route.orderOfRequestProcessed, dataModel.requestList))


# data = []
# while True:
#     line = input()
#     if line:
#         data.append(line)
#     else:
#         break

# dataModel = readInputFile(data)
# a = solve(dataModel)
# writeOutFile(a, dataModel)
