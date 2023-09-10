from numpy import ndarray
from copy import deepcopy
# from util import convertTimeToSecond


def convertTimeToSecond(dateTime: str) -> int:
    timeList = [int(i) for i in dateTime.split(":")]
    return (timeList[0] * 60 + timeList[1]) * 60 + timeList[2]


class Vehicle:
    def __init__(self, startHub: int, timeStart: int, timeEnd: int,
                 capacity: float, volume: float, velocity: float) -> None:
        self.startHub = int(startHub)
        self.timeStart = convertTimeToSecond(timeStart)
        self.timeEnd = convertTimeToSecond(timeEnd)
        self.capacity = float(capacity)
        self.volume = float(volume)
        self.velocity = float(velocity)


class Request:
    def __init__(self, pickupIdHub, deliveryIdHub, weight,
                 volume, pickupLoading, deliveryLoading,
                 pickupTimeStart, pickupTimeEnd, deliveryTimeStart,
                 deliveryTimeEnd) -> None:
        self.pickupIdHub = int(pickupIdHub)
        self.deliveryIdHub = int(deliveryIdHub)
        self.weight = float(weight)
        self.volume = float(volume)
        self.pickupLoading = int(pickupLoading)
        self.deliveryLoading = int(deliveryLoading)
        self.pickupTimeStart = convertTimeToSecond(pickupTimeStart)
        self.pickupTimeEnd = convertTimeToSecond(pickupTimeEnd)
        self.deliveryTimeStart = convertTimeToSecond(deliveryTimeStart)
        self.deliveryTimeEnd = convertTimeToSecond(deliveryTimeEnd)


class DataModel:
    """
    Contains lists about description of problem
    """

    def __init__(self,
                 distanceMatrix: ndarray,
                 vehicleList: list[Vehicle],
                 requestList: list[Request],):
        self.distanceMatrix = distanceMatrix
        self.vehicleList = vehicleList
        self.requestList = requestList


class RouteNode:
    def __init__(self,
                 idHub: int,
                 requestProcessStatus: list,
                 timeCome: int,
                 timeGo: int,
                 timeRequestProcessing: list[list[int]] = None,
                 statusRequestOfVehicleCome: list[int] = None,
                 ) -> None:
        self.idHub = idHub
        self.requestProcessStatus = requestProcessStatus
        self.timeCome = timeCome
        self.timeGo = timeGo
        self.timeRequestProcessing = timeRequestProcessing
        self.statusRequestOfVehicleCome = statusRequestOfVehicleCome

class Route:
    """_summary_
    """

    def __init__(self,
                 routeNodeList: list[RouteNode],
                 vehicleObject: Vehicle,
                 requestProcessed: set[int]) -> None:
        self.routeNodeList = routeNodeList
        self.vehicleObject = vehicleObject
        self.requestProcessed = requestProcessed


WEIGHTOFREQUEST = 10**9
WEIGHTOFVEHICLE = 10**6
WEIGHTOFTIME = 1/10**3


def totalCostFuction(routeList: list[Route],
                     quantityOfRequest: int, 
                     quantityOfVehicle: int) -> int:
    totalCost, costTime, numberOfVehicleServe = 0
    numberOfVehicleServe = 0
    listOrderServe = set()
    
    for routeObject in routeList:
        numberOfVehicleServe += 1
        costTime += routeObject.timeEnd - routeObject.timeStart
        for order in routeObject.idxRequestList:
            listOrderServe.add(order)

    totalCost += WEIGHTOFREQUEST*len(listOrderServe)/quantityOfRequest
    totalCost -= WEIGHTOFVEHICLE*numberOfVehicleServe/quantityOfVehicle
    totalCost -= WEIGHTOFTIME*costTime
    return totalCost


class Solution():
    """
    """

    def __init__(self, routeList: list[Route], locationOfVehicle: list[int]):
        self.routeList = routeList
        self.positionOfProcessingRequest: list = None
        self.locationOfVehicle: list = locationOfVehicle
        self.costFuction = None

    def updateInfoClusters(self, dataModel, weightClusterSolution, distanceMatrix):
        self.locationOfProcessingRequest = self.getInfoClusters(
            dataModel, weightClusterSolution, distanceMatrix)

    def updateCostFuction(self, dataModel: DataModel):
        quantityOfRequest = len(dataModel.requestList) - 1
        quantityOfVehicle = len(dataModel.vehicleList)
        self.costFuction = totalCostFuction(self.locationOfProcessingRequest)

    # def updateSolution(self, dataModel, weightClusterSolution, distanceMatrix):
    #     self.updateInfoClusters(
    #         dataModel, weightClusterSolution, distanceMatrix)
    #     self.updateCostFuction()
    #     self.updatePositionOfRequests()

    def objective(self):
        return self.costFuction

    def __copy__(self):
        return self.__class__(deepcopy(self.routeList))


    # def updatePositionOfRequests(self):
    #     self.positionOfPoint = positionOfPoint(self.solutionList)
