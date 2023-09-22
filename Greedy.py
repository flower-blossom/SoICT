from operators import *
from typing import NoReturn
from numpy import ndarray
from copy import deepcopy
from random import choice


# def checkConflictConstranints(request: Request, nodeBefore : RouteNode, vehicle: Vehicle) -> bool:


# def estimateFesibleRoute(routeNode : Route, ) -> bool:

def conflictVehicleCapacity(vehicleDict: dict, sequenceRequestProcessed: int, requestList: RouteNode) -> bool:
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


def estimateFesiableOfNew(startNode: RouteNode,
                          sequenceRequestProcessed: RouteNode[int],
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


def takeTimeStart(firstNumber: int, secondNumber: int) -> int:
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
                    candidateVehicle: RouteNode[int],
                    vehicleList: RouteNode[dict],
                    locationOfVehicle: RouteNode,
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

    def addEndNode(self, routeNodeList: RouteNode, vehicleInfoDict: dict, distanceMatrix: ndarray) -> NoReturn:
        lastNode = routeNodeList[-1]
        startHub = vehicleInfoDict["startIdHub"]
        if startHub != lastNode.idHub:
            distance = distanceMatrix[lastNode.idHub, startHub]
            movingTime = estimateTimeMoving(
                distance, vehicleInfoDict["velocity"])
            timeToComeBackHub = lastNode.timeGo + movingTime
            comeBackNode = RouteNode(startHub, timeToComeBackHub, timeToComeBackHub, [],
                                     timeRequestProcessing=dict())
            routeNodeList.append(comeBackNode)

    def checkValidTimePartRoute(self, nextOrderOfRequest: RouteNode, lastNode: RouteNode,
                                vehicleDict: dict, requestList: RouteNode, distanceMatrix: RouteNode) -> (bool, RouteNode):

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

    def calculateWaitTime(self, routeNodeList: RouteNode) -> int:
        """ Return time using vehicle"""

        # routeNodeList = route.routeNodeList
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
                          orderOfRequestProcessed: RouteNode,
                          routeNodeList: RouteNode, vehicleDict: dict, requestList: RouteNode, distanceMatrix: RouteNode):
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
                      requestIndexCandidate: RouteNode[int],
                      requestList: RouteNode,
                      distanceMatrix: ndarray) -> bool:
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
                       routeNodeList: RouteNode[RouteNode],
                       vehicleInfoDict: dict,
                       requestList: RouteNode[dict],
                       distanceMatrix: ndarray) -> NoReturn:
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

    def performTheProcessRequest(self, node: RouteNode, requestList: RouteNode[dict]) -> bool:
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
                    startProcessTime = takeTimeStart(
                        timeCome, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict["pickupLoadingTime"]
                else:
                    # delivery request
                    startProcessTime = takeTimeStart(
                        timeCome, requestInfoDict["deliveryTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["deliveryTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict["deliveryLoadingTime"]
            else:

                lastTimeRequest = lastTimeProcessRequest(timeRequestProcessing)
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime = takeTimeStart(
                        lastTimeRequest, requestInfoDict["pickupTime"][0])
                    if isSmallerEqualNumber(startProcessTime, requestInfoDict["pickupTime"][1]) is False:
                        return False
                    loadingTime = requestInfoDict["pickupLoadingTime"]
                else:
                    # delivery request
                    startProcessTime = takeTimeStart(
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

    # def addNextMove(self,
    #                 newRoute: Route,
    #                 requestIndexCandidate: list[int],
    #                 requestList: list[dict],
    #                 distanceMatrix: ndarray) -> bool:

    #     vehicleObject = newRoute.vehicleObject
    #     routeNodeList = newRoute.routeNodeList
    #     lastNode: RouteNode = routeNodeList[-1]
    #     stopCondition = True
    #     stopCondition = self.pickupNewRequest(lastNode,
    #                                           vehicleObject,
    #                                           requestIndexCandidate,
    #                                           requestList,
    #                                           distanceMatrix,)

    #     if len(lastNode.nextMissionOfVehicle) == 0:
    #         stopCondition = self.pickupNewRequest(lastNode,
    #                                               vehicleObject,
    #                                               requestIndexCandidate,
    #                                               requestList,
    #                                               distanceMatrix,)
    #         self.performTheProcessRequest(lastNode, requestList)
    #     else:
    #         self.processRequest(lastNode, routeNodeList, vehicleObject,
    #                             requestList, distanceMatrix)
    #         self.performTheProcessRequest(lastNode, requestList)
    #         stopCondition = True

    #     return stopCondition

    def getNewRoute(self,
                    vehicleDict: dict,
                    requestInfoList: RouteNode[dict],
                    candidateRequests: RouteNode[int],
                    distanceMatrix: ndarray) -> Route:
        newRoute = Route(RouteNode(), vehicleDict, RouteNode())
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
             solutionArr: RouteNode[Route],
             dataModel: DataModel,
             candidateVehicle: RouteNode[int],
             candidateRequests: RouteNode[int],
             locationOfVehicle: RouteNode[int],
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
        solutionArr: RouteNode[Route] = RouteNode()
        candidateRequests = [i for i in range(1, len(dataModel.requestList))]
        candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
        locationOfVehicle = [-1 for _ in range(len(dataModel.vehicleList))]
        self.main(solutionArr, dataModel, candidateVehicle,
                  candidateRequests, locationOfVehicle)
        initialSolution = Solution(solutionArr, locationOfVehicle)
        initialSolution.updateCostFuction(dataModel)
        return initialSolution
