from numpy import ndarray
from copy import deepcopy
# from util import convertTimeToSecond


def convertTimeToSecond(dateTime: str) -> int:
    timeList = [int(i) for i in dateTime.split(":")]
    return (timeList[0] * 60 + timeList[1]) * 60 + timeList[2]


class Vehicle:
    def __init__(self, startHub: int, timeStart: int, timeEnd: int,
                 capacity: float, volume: float, velocity: float) -> None:
        self.startHub = int(startHub) - 1
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
        self.pickupIdHub = int(pickupIdHub) - 1
        self.deliveryIdHub = int(deliveryIdHub) - 1
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
                 timeRequestProcessing: dict = dict(),
                 nextMissionOfVehicle: list[int] = list(),
                 ) -> None:
        self.idHub = idHub
        self.timeCome = timeCome
        self.timeGo = timeGo
        self.requestProcessStatus = requestProcessStatus
        self.timeRequestProcessing = timeRequestProcessing
        self.nextMissionOfVehicle = nextMissionOfVehicle

    def  __repr__(self) -> str:
        return f"{self.idHub + 1} \n {self.requestProcessStatus} \n {self.timeCome} \n {self.timeGo} \n {self.timeRequestProcessing} \n {self.nextMissionOfVehicle}"

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
    totalCost = 0
    costTime = 0
    numberOfVehicleServe = 0
    listOrderServe = set()
    
    for routeObject in routeList:
        numberOfVehicleServe += 1
        costTime += routeObject.routeNodeList[-1].timeCome - routeObject.routeNodeList[0].timeCome
        for order in routeObject.requestProcessed:
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
