#PYTHON 
from copy import deepcopy
from typing import NoReturn
from copy import deepcopy
from random import choice, seed
import time
seed(1)


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
                 timeRequestProcessing: dict = dict(),
                 ) -> None:
        self.idHub = idHub
        self.timeCome = timeCome
        self.timeGo = timeGo
        self.requestProcessStatus = requestProcessStatus
        self.timeRequestProcessing = timeRequestProcessing

    def  __repr__(self) -> str:
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
        self.locationOfProcessRequest: list = None


WEIGHTOFREQUEST = 10**9
WEIGHTOFVEHICLE = 10**6
WEIGHTOFTIME = 1/10**3


def totalCostFuction(routeList: list,
                     quantityOfRequest: int, 
                     quantityOfVehicle: int) -> int:
    totalCost = 0
    costTime = 0
    numberOfVehicleServe = 0
    listOrderServe = set()
    
    for routeObject in routeList:
        numberOfVehicleServe += 1
        costTime += routeObject.routeNodeList[-1].timeCome - routeObject.routeNodeList[0].timeCome
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
        self.costFuction = None

    def updateCostFuction(self, dataModel: DataModel):
        quantityOfRequest = len(dataModel.requestList) - 1
        quantityOfVehicle = len(dataModel.vehicleList)
        self.costFuction = totalCostFuction(self.routeList, 
                                            quantityOfRequest, 
                                            quantityOfVehicle)

    def objective(self):
        return self.costFuction

    def __copy__(self):
        return self.__class__(deepcopy(self.routeList))


def conflictVehicleCapacity(vehicleDict: dict, sequenceRequestProcessed: int, requestList: list) -> bool:
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
        if endTimeProcess > maxTime:
            maxTime = endTimeProcess
    return maxTime


def isSmallerEqualNumber(firstNumber: int, secondNumber: int) -> int:
    return firstNumber <= secondNumber


def takeMax(firstNumber: int, secondNumber: int) -> int:
    """ Return time to start process request"""
    if firstNumber > secondNumber:
        return firstNumber
    else:
        return secondNumber


class Greedy:

    def __init__(self, ) -> None:
        # self.orderOfRequest: list = list()
        pass

    def pickVehicle(self,
                    candidateVehicle: list,
                    vehicleList: list,
                    locationOfVehicle: list,
                    numberOfRoute: int) -> dict:
        vehiclePicked = choice(candidateVehicle)
        candidateVehicle.remove(vehiclePicked)
        vehicleObject = vehicleList[vehiclePicked]
        locationOfVehicle[vehiclePicked] = numberOfRoute
        return vehicleObject

    def addFirstNodeRoute(self, newRoute: Route,) -> NoReturn:
        vehicleDict = newRoute.vehicleDict
        startVehicleNode = RouteNode(idHub=vehicleDict["startIdHub"],
                                     timeCome=vehicleDict["startTime"],
                                     timeGo=vehicleDict["startTime"],
                                     requestProcessStatus=[],
                                     timeRequestProcessing=dict(),)
        newRoute.routeNodeList.append(startVehicleNode)

    def addEndNode(self, routeNodeList: list, vehicleInfoDict: dict, distanceMatrix: list) -> NoReturn:
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

    def checkValidTimePartRoute(self, nextOrderOfRequest: list, lastNode: RouteNode,
                                vehicleDict: dict, requestList: list, distanceMatrix: list) -> (bool, list):

        tempRoute = [deepcopy(lastNode)]
        endTimeVehicle = vehicleDict["endTime"]
        lastNode = tempRoute[-1]
        for statusRequest in nextOrderOfRequest:
            self.processRequest(statusRequest, lastNode, tempRoute,
                                vehicleDict, requestList, distanceMatrix)
            lastNode = tempRoute[-1]
            if isSmallerEqualNumber(lastNode.timeGo, endTimeVehicle) is False:
                return False, None
            if self.performTheProcessRequest(lastNode, requestList) is False:
                return False, None

        self.addEndNode(tempRoute, vehicleDict, distanceMatrix)
        # self.processRequest(statusRequest, lastNode, tempRoute,
        #                         vehicleDict, requestList, distanceMatrix)
        return isSmallerEqualNumber(tempRoute[-1].timeGo, endTimeVehicle), tempRoute

    def calculateWaitTime(self, routeNodeList: list) -> int:
        """ Return time using vehicle"""
        waitTime = 0
        movingTime = 0
        for idxNode in range(len(routeNodeList) - 1):
            node = routeNodeList[idxNode]
            timeRequestProcessing = node.timeRequestProcessing
            requestProcessStatus = node.requestProcessStatus
            if len(timeRequestProcessing) != 0:
                waitTime += node.timeCome - timeRequestProcessing[requestProcessStatus[0]][0]
            for idx in range(len(timeRequestProcessing) - 1):
                waitTime += abs(timeRequestProcessing[requestProcessStatus[idx]]
                                [1]) - timeRequestProcessing[requestProcessStatus[idx + 1]][0]
    
            movingTime += routeNodeList[idxNode + 1].timeCome - node.timeGo

        return waitTime + movingTime

    def findPlaceToInsert(self,
                          statusRequest: int,
                          orderOfRequestProcessed: list,
                          routeNodeList: RouteNode, vehicleDict: dict, requestList: list, distanceMatrix: list):
        lastNode = routeNodeList[-1]
        minUsingTime = float("inf")
        idxToInsert = -1
        startIdx = 0

        if statusRequest < 0:
            startIdx = orderOfRequestProcessed.index(abs(statusRequest)) + 1

        # index of delivery < index pickup
        for index in range(startIdx, len(orderOfRequestProcessed) + 1):
            orderOfRequestProcessed.insert(index, statusRequest)
            if conflictVehicleCapacity(vehicleDict, orderOfRequestProcessed, requestList) is False:
                conditionRoute, tempRoute = self.checkValidTimePartRoute(orderOfRequestProcessed,
                                                                         lastNode,
                                                                         vehicleDict,
                                                                         requestList,
                                                                         distanceMatrix)
                if conditionRoute is True:
                    usingTime = self.calculateWaitTime(tempRoute)
                    if usingTime < minUsingTime:
                        minUsingTime = usingTime
                        idxToInsert = index
            orderOfRequestProcessed.pop(index)
        return idxToInsert, minUsingTime

    def addNewRequest(self,
                      route: Route,
                      vehicleDict: dict,
                      requestIndexCandidate: list,
                      requestList: list,
                      distanceMatrix: list) -> bool:
        """
        try to add new request 
        """
        routeNodeList = route.routeNodeList
        orderOfRequestProcessed = route.orderOfRequestProcessed
        
        # Tổng thời gian di chuyển và chờ đợi = thời gian sử dụng
        stopCondition = False
        minCost = float("inf")
        selectedRequest = -1
        idxInsertPickUp = 0
        idxInsertDelivery = 0
        for requestIdx in requestIndexCandidate:
            pickupStatus = requestIdx
            deliveryStatus = -requestIdx

            # try to insert pickup request
            idxPickUp, _ = self.findPlaceToInsert(pickupStatus, orderOfRequestProcessed, routeNodeList,
                                                  vehicleDict, requestList, distanceMatrix)
            if idxPickUp != -1:
                orderOfRequestProcessed.insert(idxPickUp, pickupStatus)
                # try to insert delivery request
                idxDelivery, cost = self.findPlaceToInsert(deliveryStatus, orderOfRequestProcessed, routeNodeList,
                                                           vehicleDict, requestList, distanceMatrix)
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

    def processRequest(self,
                       statusRequest: int,
                       lastNode: RouteNode,
                       routeNodeList: list,
                       vehicleInfoDict: dict,
                       requestList: list,
                       distanceMatrix: list) -> NoReturn:
        """
        Create node to process request
        """

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

            newNode = RouteNode(idHub=nextHub,
                                timeCome=timeGoToHub,
                                timeGo=timeGoToHub,
                                requestProcessStatus=[statusRequest],
                                timeRequestProcessing=dict(),)
            routeNodeList.append(newNode)

    def performTheProcessRequest(self, node: RouteNode, requestList: list) -> bool:
        """ 
        Try to update time to delivery or pickup request and time 
        to go out current hub 
        """
        requestProcessStatus = node.requestProcessStatus
        timeRequestProcessing = node.timeRequestProcessing
        timeCome = node.timeCome
        lastTimeAction = node.timeCome
        for requestStatusIdx in requestProcessStatus:
            requestInfoDict = requestList[abs(requestStatusIdx)]
            startProcessTime = 0
            endProcessTime = 0
            loadingTime = 0

            if len(timeRequestProcessing) == 0:
                # is first request process
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime = takeMax(
                        timeCome, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict["pickupLoadingTime"]
                else:
                    # delivery request
                    startProcessTime = takeMax(
                        timeCome, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict["deliveryLoadingTime"]
            else:

                lastTimeRequest = lastTimeProcessRequest(timeRequestProcessing)
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime = takeMax(
                        lastTimeRequest, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict["pickupLoadingTime"]
                else:
                    # delivery request
                    startProcessTime = takeMax(
                        lastTimeRequest, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict["deliveryLoadingTime"]
            endProcessTime = startProcessTime + loadingTime

            timeRequestProcessing[requestStatusIdx] = [
                startProcessTime, endProcessTime]
            lastTimeAction = endProcessTime
        node.timeGo = lastTimeAction
        return True

    def getNewRoute(self,
                    vehicleDict: dict,
                    requestInfoList: list,
                    candidateRequests: list,
                    distanceMatrix: list) -> Route:
        newRoute = Route(list(), vehicleDict, list())
        self.addFirstNodeRoute(newRoute)

        while True:
            stopCondition = self.addNewRequest(newRoute, vehicleDict, candidateRequests,
                                               requestInfoList, distanceMatrix)

            if stopCondition is False:
                break
        _, newRoute.routeNodeList = self.checkValidTimePartRoute(newRoute.orderOfRequestProcessed,
                                                                 newRoute.routeNodeList[-1],
                                                                 vehicleDict,
                                                                 requestInfoList,
                                                                 distanceMatrix)
        # self.addEndNode(newRoute, distanceMatrix)
        return newRoute

    def main(self,
             solutionArr: list,
             dataModel: DataModel,
             candidateVehicle: list,
             candidateRequests: list,
             locationOfVehicle: list,
             ) -> NoReturn:
        """ Create new Route through loop"""

        distanceMatrix = dataModel.distanceMatrix
        vehicleList = dataModel.vehicleList
        requestList = dataModel.requestList
        numberOfRoute = 0
        while True:
            vehicleDict = self.pickVehicle(
                candidateVehicle, vehicleList, locationOfVehicle, numberOfRoute)
            newRoute = self.getNewRoute(vehicleDict,
                                        requestList,
                                        candidateRequests,
                                        distanceMatrix,)
            solutionArr.append(newRoute)
            numberOfRoute += 1
            if len(candidateVehicle) == 0 or len(candidateRequests) == 0:
                break

    def solve(self, dataModel: DataModel) -> Solution:
        solutionArr = list()
        candidateRequests = [i for i in range(1, len(dataModel.requestList))]
        candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
        locationOfVehicle = [-1 for _ in range(len(dataModel.vehicleList))]
        self.main(solutionArr, dataModel, candidateVehicle,
                  candidateRequests, locationOfVehicle)
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
    print(f"{vehicle.startHub + 1} {time} {time}")


def writeRoute(route: Route):
    print(len(route.routeNodeList))
    for node in route.routeNodeList:
        print(f"{node.idHub + 1} {len(node.requestProcessStatus)} {convertSecondsToHours(node.timeCome)} {convertSecondsToHours(node.timeGo)}")
        for request in node.requestProcessStatus:
            timeProcess = node.timeRequestProcessing[request][0]
            print(f"{request} {convertSecondsToHours(timeProcess)}")


def writeOutFile(solution: Solution, dataModel: DataModel):
    vehicleList = dataModel.vehicleList
    locationOfVehicle = solution.locationOfVehicle
    routeList = solution.routeList
    for indexRoute in locationOfVehicle:
        if indexRoute == -1:
            writeVehicleNotUse(vehicleList[indexRoute])
        else:
            writeRoute(routeList[indexRoute])


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
a = Greedy().solve(dataModel)
# localSearch(a, dataModel)
print(time.time()-time1)

# print(dataModel.requestList[113])
print(a.costFuction)
# writeOutFile(a, dataModel)
