from operators import *
from typing import NoReturn
from numpy import ndarray
from copy import deepcopy
from random import choice


# def checkConflictConstranints(request: Request, nodeBefore : RouteNode, vehicle: Vehicle) -> bool:


# def estimateFesibleRoute(routeNode : Route, ) -> bool:

def conflictVehicleCapacity(vehicleDict: dict, sequenceRequestProcessed: int, requestList: list) -> bool:
    vehicleCapacity = vehicleDict["capacity"]
    vehicleVolume = vehicleDict["volume"]
    currentCapacity = 0
    currentVolume = 0

    for statusRequest in sequenceRequestProcessed:
        requestDict = requestList[abs(statusRequest)]
        if statusRequest > 0:
            currentCapacity += requestDict["capacity"]
            currentVolume += requestDict["volume"]
        else:
            currentCapacity -= requestDict["capacity"]
            currentVolume -= requestDict["volume"]
        if currentVolume > vehicleVolume or currentCapacity > vehicleCapacity:
            return False
    return True


def estimateTimeMoving(distance: int, velocity: int) -> int:
    return int(distance/velocity*3600)


def estimateFesiableOfNew(startNode: RouteNode,
                          sequenceRequestProcessed: list[int],
                          vehicleOfRoute: dict) -> bool:

    return True


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
                    candidateVehicle: list[int],
                    vehicleList: list[dict],
                    locationOfVehicle: list,
                    numberOfRoute: int) -> int:
        vehiclePicked = choice(candidateVehicle)
        candidateVehicle.remove(vehiclePicked)
        vehicleObject = vehicleList[vehiclePicked]
        locationOfVehicle[vehiclePicked] = numberOfRoute
        return vehicleObject

    def addFirstNodeRoute(self, newRoute: Route,) -> NoReturn:
        vehicleObject = newRoute.vehicleObject
        startVehicleNode = RouteNode(idHub=vehicleObject.startHub,
                                     timeCome=vehicleObject.timeStart,
                                     timeGo=vehicleObject.timeStart,
                                     requestProcessStatus=[],
                                     timeRequestProcessing=dict(),)
        newRoute.routeNodeList.append(startVehicleNode)

    def addEndNode(self, routeNodeList: list, vehicleInfoDict: dict, distanceMatrix: ndarray) -> NoReturn:
        lastNode = routeNodeList[-1]
        startHub = vehicleInfoDict["startHub"]
        if startHub != lastNode.idHub:
            distance = distanceMatrix[lastNode.idHub, startHub]
            movingTime = estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeToComeBackHub = lastNode.timeGo + movingTime
            comeBackNode = RouteNode(startHub, [], timeToComeBackHub, timeToComeBackHub,
                                     timeRequestProcessing=dict(), nextMissionOfVehicle=[])
            routeNodeList.append(comeBackNode)

    def checkValidTimePartRoute(self, nextOrderOfRequest: list, lastNode: RouteNode,
                                vehicleDict: dict, requestList: list, distanceMatrix: list):

        tempRoute = [deepcopy(lastNode)]
        endTimeVehicle = vehicleDict["endTime"]

        for statusRequest in nextOrderOfRequest:
            lastNode = tempRoute.routeNodeList[-1]
            self.processRequest(statusRequest, lastNode, tempRoute,
                                vehicleDict, requestList, distanceMatrix)
            if isSmallerEqualNumber(lastNode.timeGo, endTimeVehicle) is False:
                return False, None
            if self.performTheProcessRequest(lastNode, requestList) is False:
                return False, None

        self.addEndNode(tempRoute, vehicleDict, distanceMatrix)
        return isSmallerEqualNumber(tempRoute[-1].timeGo, endTimeVehicle), tempRoute

    # def createRoute(self, nextOrderOfRequest: list, lastNode: RouteNode,
    #                 vehicleDict: dict, requestList: list, distanceMatrix: list) -> NoReturn:

    def calculateWaitTime(self, route: Route) -> int:
        """ Return time using vehicle"""
        routeNodeList = route.routeNodeList
        waitTime = 0
        movingTime = 0
        for idxNode in range(len(routeNodeList), - 1):
            node = routeNodeList[idxNode]
            timeRequestProcessing = node.timeRequestProcessing
            waitTime += node.timeCome - timeRequestProcessing[0][0]
            for idx in range(len(timeRequestProcessing), - 1):
                waitTime += abs(timeRequestProcessing[idx]
                                [1]) - timeRequestProcessing[idx + 1][0]

            movingTime += routeNodeList[idxNode + 1].timeCome - node.timeGo

        return waitTime + movingTime

    def findPlaceToInsert(self,
                          statusRequest: int,
                          orderOfRequestProcessed: list,
                          routeNodeList: RouteNode, vehicleDict: dict, requestList: list, distanceMatrix: list) -> bool:
        lastNode = routeNodeList[-1]
        minUsingTime = float("inf")
        idxToInsert = -1
        startIdx = 0
        if statusRequest < 0:
            startIdx = orderOfRequestProcessed.index(abs(statusRequest)) + 1
            
        # index of delivery < index pickup
        for index in range(startIdx,len(orderOfRequestProcessed) + 1):
            orderOfRequestProcessed.insert(index, statusRequest)
            if conflictVehicleCapacity(vehicleDict, orderOfRequestProcessed) is False:
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
        orderOfRequestProcessed.insert(idxToInsert, statusRequest)

    def addNewRequest(self,
                      route: Route,
                      vehicleDict: dict,
                      requestIndexCandidate: list[int],
                      requestList: list,
                      distanceMatrix: ndarray) -> bool:
        """
        add new request 
        """
        routeNodeList = route.routeNodeList
        orderOfRequestProcessed = route.orderOfRequestProcessed

        # Tổng thời gian di chuyển và chờ đợi = thời gian sử dụng
        for requestIdx in requestIndexCandidate:
            pickupStatus = requestIdx
            deliveryStatus = -requestIdx

            # try to insert pickup request
            self.findPlaceToInsert(pickupStatus, orderOfRequestProcessed, routeNodeList,
                                   vehicleDict, requestList, distanceMatrix)
            
            # try to insert delivery request          
            self.findPlaceToInsert(deliveryStatus, orderOfRequestProcessed, routeNodeList,
                                   vehicleDict, requestList, distanceMatrix)

        print("hookup pickupNewRequest")

    def processRequest(self,
                       statusRequest: int,
                       lastNode: RouteNode,
                       routeNodeList: list[RouteNode],
                       vehicleInfoDict: dict,
                       requestList: list[dict],
                       distanceMatrix: ndarray) -> NoReturn:
        """
        Create node to process request
        """

        currentHub = lastNode.idHub
        requestObject = requestList[abs(statusRequest)]

        nextHub = 0
        if statusRequest > 0:
            nextHub = requestObject.pickupIdHub
        if statusRequest < 0:
            nextHub = requestObject.deliveryIdHub

        if nextHub == currentHub:
            # add request to last node
            lastNode.requestProcessStatus.append(statusRequest)
        else:
            # create and moving to new node
            distance = distanceMatrix[currentHub, nextHub]
            movingTime = estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeGoToHub = lastNode.timeGo + movingTime

            newNode = RouteNode(idHub=nextHub,
                                timeCome=timeGoToHub,
                                timeGo=timeGoToHub,
                                requestProcessStatus=[statusRequest],
                                timeRequestProcessing=dict(),)
            routeNodeList.append(newNode)

    def performTheProcessRequest(self, node: RouteNode, requestList: list[dict]) -> bool:
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
                    loadingTime = requestInfoDict.pickupLoading
                else:
                    # delivery request
                    startProcessTime = takeMax(
                        timeCome, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict.deliveryLoading
            else:

                lastTimeRequest = lastTimeProcessRequest(timeRequestProcessing)
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime = takeMax(
                        lastTimeRequest, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict.pickupLoading
                else:
                    # delivery request
                    startProcessTime = takeMax(
                        lastTimeRequest, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict.deliveryLoading
            endProcessTime = startProcessTime + loadingTime

            timeRequestProcessing[requestStatusIdx] = [
                startProcessTime, endProcessTime]
            lastTimeAction = endProcessTime
        node.timeGo = lastTimeAction
        return True

    def addNextMove(self,
                    newRoute: Route,
                    requestIndexCandidate: list[int],
                    requestList: list[dict],
                    distanceMatrix: ndarray) -> bool:

        vehicleObject = newRoute.vehicleObject
        routeNodeList = newRoute.routeNodeList
        lastNode: RouteNode = routeNodeList[-1]
        stopCondition = True
        stopCondition = self.pickupNewRequest(lastNode,
                                              vehicleObject,
                                              requestIndexCandidate,
                                              requestList,
                                              distanceMatrix,)

        if len(lastNode.nextMissionOfVehicle) == 0:
            stopCondition = self.pickupNewRequest(lastNode,
                                                  vehicleObject,
                                                  requestIndexCandidate,
                                                  requestList,
                                                  distanceMatrix,)
            self.performTheProcessRequest(lastNode, requestList)
        else:
            self.processRequest(lastNode, routeNodeList, vehicleObject,
                                requestList, distanceMatrix)
            self.performTheProcessRequest(lastNode, requestList)
            stopCondition = True

        return stopCondition

    def getNewRoute(self,
                    vehicleObject: dict,
                    requestInfoList: list[dict],
                    candidateRequests: list[int],
                    distanceMatrix: ndarray) -> Route:
        newRoute = Route(list(), vehicleObject, list())
        self.addFirstNodeRoute(newRoute)

        while True:
            stopCondition = self.addNewRequest(newRoute, candidateRequests,
                                               requestInfoList, distanceMatrix)

            if stopCondition is False:
                break
        self.addEndNode(newRoute, distanceMatrix)
        return newRoute

    def main(self,
             solutionArr: list[Route],
             dataModel: DataModel,
             candidateVehicle: list[int],
             candidateRequests: list[int],
             locationOfVehicle: list[int],
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
        solutionArr: list[Route] = list()
        candidateRequests = [i for i in range(1, len(dataModel.requestList))]
        candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
        locationOfVehicle = [-1 for _ in range(len(dataModel.vehicleList))]
        self.main(solutionArr, dataModel, candidateVehicle,
                  candidateRequests, locationOfVehicle)
        initialSolution = Solution(solutionArr, locationOfVehicle)
        initialSolution.updateCostFuction(dataModel)
        return initialSolution
