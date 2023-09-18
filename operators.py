from numpy import ndarray
from copy import deepcopy
# from util import convertTimeToSecond



class DataModel:
    """
    Contains lists about description of problem
    """

    def __init__(self,
                 distanceMatrix: ndarray,
                 vehicleList: list[dict],
                 requestList: list[dict],):
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
        return f"{self.idHub + 1} \n {self.requestProcessStatus} \n {self.timeCome} \n {self.timeGo} \n {self.timeRequestProcessing} \n {self.nextMissionOfVehicle}"

class Route:
    """_summary_
    """

    def __init__(self,
                 routeNodeList: list[RouteNode],
                 vehicleDict: dict,
                 orderOfRequestProcessed: list = []):
        self.routeNodeList = routeNodeList
        self.vehicleDict = vehicleDict
        self.orderOfRequestProcessed = orderOfRequestProcessed
        self.locationOfProcessRequest: list = None


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
        for order in routeObject.orderOfRequestProcessed:
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
