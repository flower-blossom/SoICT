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
                                     processRequestInHub=[],
                                     timeCome=vehicleObject.timeStart,
                                     timeGo=vehicleObject.timeStart)
        newRoute.routeNodeList.append(startVehicleNode)

    def newStatusRequestOfVehicleCome(self,
                                      statusRequestOfVehicleCome: list[int],
                                      requestProcessStatus: list[int]) -> list:
        tempList = statusRequestOfVehicleCome.copy()
        for element in requestProcessStatus:
            if element > 0:
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
        currentHub = node.idHub
        startTime = node.timeGo
        velocity = vehicleObject.velocity

        requestIsSelectedIdx = -1
        minTimeDifference = float("inf")
        for requestIdx in requestIndexCandidate:
            requestObject = requestList[requestIdx]
            pickupIdHub = requestObject.pickupIdHub

            if currentHub == pickupIdHub:
                movingTime = 0
            else:
                distance = distanceMatrix[currentHub, pickupIdHub]
                movingTime = estimateTimeMoving(distance, velocity)
            timeToComeNewHub = startTime + movingTime
            if timeToComeNewHub > requestObject.deliveryTimeEnd:
                pass
            estimateUsingTime = abs(
                timeToComeNewHub - requestObject.deliveryTimeEnd)

            if minTimeDifference < estimateUsingTime:
                estimateUsingTime = minTimeDifference
                requestIsSelectedIdx = requestIdx

        if requestIsSelectedIdx == -1:
            return False
        else:
            requestIndexCandidate.remove(requestIsSelectedIdx)
            node.requestProcessed.append(requestIsSelectedIdx)
            self.orderOfRequest.add(requestIsSelectedIdx)
            return True
        print("hookup pickupNewRequest")

    def deliveryRequest(self,
                        statusRequestIdx: int,
                        lastNode: RouteNode,
                        routeNodeList: list[RouteNode],
                        vehicleObject: Vehicle,
                        requestList: list[Request],
                        distanceMatrix: ndarray) -> NoReturn:
        """
        Create node to delivery request
        """
        requestIdx = abs(statusRequestIdx)
        currentHub = lastNode.idHub
        statusRequestOfVehicleCome = lastNode.statusRequestOfVehicleCome
        velocityVehicle = vehicleObject.velocity

        # add new node to delivery
        requestObject = requestList[requestIdx]
        deliveryHub = requestObject.deliveryIdHub
        requestProcessStatus = [statusRequestIdx]

        distance = distanceMatrix[currentHub, deliveryHub]
        movingTime = estimateTimeMoving(distance, velocityVehicle)
        timeGoToHub = lastNode.timeGo + movingTime

        if timeGoToHub >= requestObject.deliveryTimeStart:
            startTimeDeliveryRequest = timeGoToHub
        else:
            startTimeDeliveryRequest = requestObject.deliveryTimeStart

        endDeliveryTime = startTimeDeliveryRequest + requestObject.deliveryLoading
        timeRequestProcessing = [startTimeDeliveryRequest, endDeliveryTime]
        timeGo = endDeliveryTime
        statusRequestOfVehicleCome = self.newStatusRequestOfVehicleCome(lastNode.statusRequestOfVehicleCome,
                                                                        requestProcessStatus=requestProcessStatus)

        newNode = RouteNode(idHub=deliveryHub,
                            requestProcessStatus=requestProcessStatus,
                            timeCome=timeGoToHub,
                            timeGo=endDeliveryTime,
                            timeRequestProcessing=timeRequestProcessing,
                            statusRequestOfVehicleCome=statusRequestOfVehicleCome)
        routeNodeList.append(newNode)

    def pickUpRequest(self,
                      statusRequestIdx: int,
                      lastNode: RouteNode,
                      routeNodeList: list[RouteNode],
                      vehicleObject: Vehicle,
                      requestList: list[Request],
                      distanceMatrix: ndarray) -> NoReturn:
        """ Create node to pickup request

        Args:
            requestIdx (int): _description_
            lastNode (RouteNode): _description_
            routeNodeList (list[RouteNode]): _description_
            vehicleObject (Vehicle): _description_
            requestList (list[Request]): _description_
            distanceMatrix (ndarray): _description_

        Returns:
            NoReturn: _description_
        """
        requestIdx = abs(statusRequestIdx)
        currentHub = lastNode.idHub
        statusRequestOfVehicleCome = lastNode.statusRequestOfVehicleCome
        velocityVehicle = vehicleObject.velocity

        # add new node to delivery
        requestObject = requestList[requestIdx]
        pickupHub = requestObject.deliveryIdHub
        requestProcessStatus = [statusRequestIdx]

        distance = distanceMatrix[currentHub, pickupHub]
        movingTime = estimateTimeMoving(distance, velocityVehicle)
        timeGoToHub = lastNode.timeGo + movingTime

        if timeGoToHub >= requestObject.pickupTimeStart:
            startTimeDeliveryRequest = timeGoToHub
        else:
            startTimeDeliveryRequest = requestObject.pickupTimeStart

        endDeliveryTime = startTimeDeliveryRequest + requestObject.pickupLoading
        timeRequestProcessing = [startTimeDeliveryRequest, endDeliveryTime]
        timeGo = endDeliveryTime
        statusRequestOfVehicleCome = self.newStatusRequestOfVehicleCome(lastNode.statusRequestOfVehicleCome,
                                                                        requestProcessStatus=requestProcessStatus)

        newNode = RouteNode(idHub=pickupHub,
                            requestProcessStatus=requestProcessStatus,
                            timeCome=timeGoToHub,
                            timeGo=endDeliveryTime,
                            timeRequestProcessing=timeRequestProcessing,
                            statusRequestOfVehicleCome=statusRequestOfVehicleCome)
        routeNodeList.append(newNode)
        

    def addNextMove(self,
                    newRoute: Route,
                    requestIndexCandidate: list[int],
                    requestList: list[Request],
                    distanceMatrix: ndarray) -> bool:
        vehicleObject = newRoute.vehicleObject
        routeNodeList = newRoute.routeNodeList
        velocityVehicle = vehicleObject.velocity

        lastNode: RouteNode = routeNodeList[-1]

        currentHub = lastNode.idHub
        if len(lastNode.statusRequestOfVehicleCome) == 0:
            return self.pickupNewRequest(lastNode,
                                         vehicleObject,
                                         requestIndexCandidate,
                                         requestList,
                                         distanceMatrix,)
        else:
            for statusRequestIdx in lastNode.statusRequestOfVehicleCome:
                if statusRequestIdx <= 0:
                    self.deliveryRequest(statusRequestIdx, lastNode, routeNodeList, 
                                         vehicleObject, requestList, distanceMatrix)
                    return True
                else:
                    self.pickUpRequest()
                    return True
        return True

    def getNewRoute(self,
                    vehicleObject: Vehicle,
                    requestList: list[Request],
                    requestIndex: list[int],
                    distanceMatrix: ndarray) -> Route:
        routeNodeList = list()

        newRoute = Route(routeNodeList, vehicleObject, list())
        self.addFirstNodeRoute(newRoute)

        while True:
            stopCondition = self.addNextMove(newRoute, requestIndex,
                                             requestList, distanceMatrix)
            if stopCondition is False:
                break
        newRoute.requestProcessed = self.orderOfRequest.copy()
        return newRoute

    def main(self,
             solutionArr: list[Route],
             dataModel: DataModel,
             vehicleIndex: list[int],
             requestIndex: list[int],
             locationOfVehicle: list[int],
             ) -> NoReturn:
        distanceMatrix = dataModel.distance
        while vehicleIndex or requestIndex:
            vehicleIdx = self.pickVehicle(vehicleIndex,)
            vehicleObject = dataModel.vehicleList[vehicleIdx]
            locationOfVehicle.append(vehicleIdx)

            newRoute = self.getNewRoute(vehicleObject,
                                        dataModel.requestList,
                                        requestIndex,
                                        distanceMatrix,)
            solutionArr.append(newRoute)

    def solve(self, dataModel: DataModel) -> Solution:
        solutionArr: list[Route] = list()
        requestIndex = [i for i in range(1, len(dataModel.requestList))]
        vehicleIndex = [i for i in range(len(dataModel.vehicleList))]
        locationOfVehicle = [-1 for i in range(len(dataModel.vehicleList))]
        self.main(solutionArr, dataModel, vehicleIndex,
                  requestIndex, locationOfVehicle)
        initialSolution = Solution(solutionArr,)
        return initialSolution
    
    

