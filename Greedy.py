from operators import *
from typing import NoReturn
from numpy import ndarray
from copy import deepcopy
from random import choice


# giai quyet tam thoi van de giao va lay 1 requet trong moi node

# tao 1 dict trong node de mieu ta trang tai giao hang hoac lay hang trong request


# lay xe
# trang thai don hang, giao va tra hang
# list trang thai cac rang buoc xuyen suot lua chon route
# tao
# viet rieng ham rang buoc ?,
# dk dung của rouxte

# dieu kien
# xe dem som so voi thoi gian, xe den muon
# chen hang doi, dk thich ung. Them vao index ?

# hienj taij:
# them phan tu request dau tien tac dong toi nhung phan tu nao
# chon cac request sau
# xu ly viec vua tra hang va lay hang cung luc và ràng buộc về trọng lượng lẫn thời gian ?
# tạo thêm biến lưu trữ, nhưng lưu ở đâu
#


# def checkConflictConstranints(request: Request, nodeBefore : RouteNode, vehicle: Vehicle) -> bool:

# def checkValidRoute(route: Route, ) -> bool:


# def estimateFesibleRoute(routeNode : Route, ) -> bool:

# def waitToNewRequest(newRoute: Route,
#                   requestIndex: list[int],
#                   requestList: list[Request],
#                   queueOfRequest: list[int],
#                   distanceMatrix: ndarray, ) -> bool:
#     vehicleObject = newRoute.vehicleObject
#     velocityVehicle = vehicleObject.velocity
#     timeEndVehicle = vehicleObject.timeEnd
#     temporaryNode = deepcopy(newRoute.routeNodeList[-1])

#     statusOfVehicleCome = temporaryNode.statusOfVehicleCome
#     statusOfVehicleGo = temporaryNode.statusOfVehicleGo

#     for requestIdx in requestIndex:
#         requestObject = requestList[requestIdx]

#         if temporaryNode.currentHub == requestObject.sendIdHub:
#             movingTime = 0
#             # các điều kiện thỏa mãn ràng buộc hàng
#             waitingTime = requestObject.sendTimeStart -
#             estimateUsingTime = abs(
#                 timeStartVehicle + movingTime - requestObject.sendTimeStart)

#             distance = distanceMatrix[startHub, requestObject.sendIdHub]

#         estimateFesibleRoute()

#         queueOfRequest.append(requestIsSelectedIdx)
#         requestIndex.remove(requestIsSelectedIdx)


#     return False

def estimateTimeMoving(distance: int, velocity: int) -> int:
    return int(distance/velocity*3600)


def estimateFesiableOfNew(nodeStart: RouteNode,
                          sequenceRequestProcessed: list[int],
                          vehicleOfRoute: Vehicle) -> bool:

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


def takeTimeStart(currentTime: int, processTimeStart: int) -> int:
    """ Return time to start process request"""
    if currentTime > processTimeStart:
        return currentTime
    else:
        return processTimeStart

class Greedy:

    def __init__(self, ) -> None:
        self.orderOfRequest: set = set()

    def pickVehicle(self, vehicleIndex: list[int]) -> int:
        vehiclePicked = choice(vehicleIndex)
        vehicleIndex.remove(vehiclePicked)
        return vehiclePicked

    def addFirstNodeRoute(self, newRoute: Route,) -> NoReturn:
        vehicleObject = newRoute.vehicleObject
        startVehicleNode = RouteNode(idHub=vehicleObject.startHub,
                                     requestProcessStatus=[],
                                     timeCome=vehicleObject.timeStart,
                                     timeGo=vehicleObject.timeStart,
                                     timeRequestProcessing=dict(),
                                     nextMissionOfVehicle=[])
        newRoute.routeNodeList.append(startVehicleNode)

    def addLastNode(self, newRoute: Route, distanceMatrix: ndarray) -> NoReturn:
        lastNode = newRoute.routeNodeList[-1]
        vehicleObject = newRoute.vehicleObject
        startHub = vehicleObject.startHub
        distance = distanceMatrix[lastNode.idHub, startHub]
        movingTime = estimateTimeMoving(distance, vehicleObject.velocity)
        timeToComeBackHub = lastNode.timeGo + movingTime
        comeBackNode = RouteNode(startHub, [], timeToComeBackHub, timeToComeBackHub, 
                                 timeRequestProcessing=dict(), nextMissionOfVehicle=[])
        newRoute.routeNodeList.append(comeBackNode)

    def newStatusRequestOfVehicleCome(self,
                                      nextMissionOfVehicle: list[int],
                                      requestProcessStatus: list[int]) -> list:
        # [-3, 4] , [-3] => [-4]
        tempList = nextMissionOfVehicle.copy()
        for element in requestProcessStatus:
            if element > 0:
                tempList.remove(element)
                tempList.append(-element)
            elif element < 0:
                tempList.remove(element)
            else:
                print("error in updateStatusRequestOfVehicleCome")
        return tempList

    def pickupNewRequest(self,
                         node: RouteNode,
                         vehicleObject: Vehicle,
                         requestIndexCandidate: list[int],
                         requestList: list[Request],
                         distanceMatrix: ndarray) -> bool:
        """
        add new request to pickup last node
        """

        currentHub = node.idHub
        startTime = node.timeGo
        velocity = vehicleObject.velocity

        requestIsSelectedIdx = -1
        minTimeDifference = float("inf")

        for requestIdx in requestIndexCandidate:
            requestObject = requestList[requestIdx]
            pickupIdHub = requestObject.pickupIdHub

            estimateUsingTime = 0
            movingTime = 0
            if currentHub == pickupIdHub:
                movingTime = 0
            else:
                movingTime = estimateTimeMoving(
                    distanceMatrix[currentHub, pickupIdHub], velocity)
            timeToComeNewHub = startTime + movingTime
            if timeToComeNewHub < requestObject.deliveryTimeEnd:
                estimateUsingTime = abs(
                    timeToComeNewHub - requestObject.pickupTimeStart)
                if estimateUsingTime < minTimeDifference:
                    minTimeDifference = estimateUsingTime
                    requestIsSelectedIdx = requestIdx

        if requestIsSelectedIdx == -1:
            return False
        else:
            requestObject = requestList[requestIsSelectedIdx]
            if requestObject.pickupIdHub == currentHub:
                node.requestProcessStatus.append(requestIsSelectedIdx)
                node.nextMissionOfVehicle.append(-requestIsSelectedIdx)
            else:
                node.nextMissionOfVehicle.append(requestIsSelectedIdx)
            requestIndexCandidate.remove(requestIsSelectedIdx)
            self.orderOfRequest.add(requestIsSelectedIdx)
            return True
        print("hookup pickupNewRequest")

    def moveToNewNode(self,
                      lastNode: RouteNode,
                      routeNodeList: list[RouteNode],
                      vehicleObject: Vehicle,
                      requestList: list[Request],
                      distanceMatrix: ndarray) -> NoReturn:
        """
        Create node to delivery request
        """
        # seclect next hub
        currentHub = lastNode.idHub
        nextMissionOfVehicle = lastNode.nextMissionOfVehicle
        velocityVehicle = vehicleObject.velocity

        statusRequestIdx = 0
        minDistance = float("inf")
        for statusRequest in nextMissionOfVehicle:
            requestIdx = abs(statusRequest)
            requestObject = requestList[requestIdx]
            if statusRequest > 0:
                nextHub = requestObject.pickupIdHub
            if statusRequest < 0:    
                nextHub = requestObject.deliveryIdHub
            distance = distanceMatrix[currentHub, nextHub]
            if distance < minDistance:
                minDistance = distance
                statusRequestIdx = statusRequest

        requestObject = requestList[abs(statusRequestIdx)]
        requestProcessStatus = [statusRequestIdx]

        movingTime = estimateTimeMoving(minDistance, velocityVehicle)
        timeGoToHub = lastNode.timeGo + movingTime

        nextMissionOfVehicle = self.newStatusRequestOfVehicleCome(lastNode.nextMissionOfVehicle,
                                                                  requestProcessStatus=requestProcessStatus)

        newNode = RouteNode(idHub=nextHub,
                            requestProcessStatus=requestProcessStatus,
                            timeCome=timeGoToHub,
                            timeGo=timeGoToHub,
                            timeRequestProcessing=dict(),
                            nextMissionOfVehicle=nextMissionOfVehicle)
        routeNodeList.append(newNode)


    def performTheProcessRequest(self, node: RouteNode, requestList: list[Request]) -> NoReturn:
        """ 
        update time to delivery or pickup request 
        """

        requestProcessStatus = node.requestProcessStatus
        timeRequestProcessing = node.timeRequestProcessing
        timeCome = node.timeCome
        lastTimeAction = node.timeCome
        for requestStatusIdx in requestProcessStatus:
            requestObjest = requestList[abs(requestStatusIdx)]
            startProcessTime = 0
            endProcessTime = 0

            if len(timeRequestProcessing) == 0:
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime = takeTimeStart(
                        timeCome, requestObjest.pickupTimeStart)
                    endProcessTime = startProcessTime + requestObjest.pickupLoading
                else:
                    # delivery request
                    startProcessTime = takeTimeStart(
                        timeCome, requestObjest.deliveryTimeStart)
                    endProcessTime = startProcessTime + requestObjest.deliveryLoading
            else:
                lastTimeRequest = lastTimeProcessRequest(timeRequestProcessing)
                if requestStatusIdx > 0:
                    # pickUp request
                    startProcessTime = takeTimeStart(
                        lastTimeRequest, requestObjest.pickupTimeStart)
                    endProcessTime = startProcessTime + requestObjest.pickupLoading
                else:
                    # delivery request
                    startProcessTime = takeTimeStart(
                        lastTimeRequest, requestObjest.deliveryTimeStart)
                    endProcessTime = startProcessTime + requestObjest.deliveryLoading
            timeRequestProcessing[requestStatusIdx] = [
                startProcessTime, endProcessTime]
            lastTimeAction = endProcessTime
        node.timeGo = lastTimeAction


    def addNextMove(self,
                    newRoute: Route,
                    requestIndexCandidate: list[int],
                    requestList: list[Request],
                    distanceMatrix: ndarray) -> bool:

        vehicleObject = newRoute.vehicleObject
        routeNodeList = newRoute.routeNodeList
        lastNode: RouteNode = routeNodeList[-1]
        stopCondition = True

        if len(lastNode.nextMissionOfVehicle) == 0:
            stopCondition = self.pickupNewRequest(lastNode,
                                                  vehicleObject,
                                                  requestIndexCandidate,
                                                  requestList,
                                                  distanceMatrix,)
            self.performTheProcessRequest(lastNode, requestList)
        else:
            self.moveToNewNode(lastNode, routeNodeList, vehicleObject,
                               requestList, distanceMatrix)
            self.performTheProcessRequest(lastNode, requestList)
            # print(lastNode)
            stopCondition = True
            
        return stopCondition 

    def getNewRoute(self,
                    vehicleObject: Vehicle,
                    requestList: list[Request],
                    requestIndex: list[int],
                    distanceMatrix: ndarray) -> Route:
        newRoute = Route([], vehicleObject, list())
        self.addFirstNodeRoute(newRoute)

        while True:
            stopCondition = self.addNextMove(newRoute, requestIndex,
                                             requestList, distanceMatrix)
            if stopCondition is False:
                break
        self.addLastNode(newRoute, distanceMatrix)
        newRoute.requestProcessed = self.orderOfRequest.copy()
        self.orderOfRequest.clear()
        return newRoute

    def main(self,
             solutionArr: list[Route],
             dataModel: DataModel,
             vehicleIndex: list[int],
             requestIndex: list[int],
             locationOfVehicle: list[int],
             ) -> NoReturn:
        """ Create new Route through loop"""

        distanceMatrix = dataModel.distanceMatrix
        vehicleList = dataModel.vehicleList
        requestList = dataModel.requestList
        numberOfRoute = 0
        while True:
            vehicleIdx = self.pickVehicle(vehicleIndex,)
            vehicleObject = vehicleList[vehicleIdx]
            locationOfVehicle[vehicleIdx] = numberOfRoute
            newRoute = self.getNewRoute(vehicleObject,
                                        requestList,
                                        requestIndex,
                                        distanceMatrix,)
            solutionArr.append(newRoute)
            numberOfRoute += 1
            if len(vehicleIndex) == 0 or len(requestIndex) == 0:
                break

    def solve(self, dataModel: DataModel) -> Solution:
        solutionArr: list[Route] = list()
        requestIndex = [i for i in range(1, len(dataModel.requestList))]
        vehicleIndex = [i for i in range(len(dataModel.vehicleList))]
        locationOfVehicle = [-1 for i in range(len(dataModel.vehicleList))]
        self.main(solutionArr, dataModel, vehicleIndex,
                  requestIndex, locationOfVehicle)
        initialSolution = Solution(solutionArr, locationOfVehicle)
        initialSolution.updateCostFuction(dataModel)
        return initialSolution
