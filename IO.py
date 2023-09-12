import numpy as np
from operators import *
from Greedy import Greedy

def convertSecondsToHours(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    time_format = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return time_format

def takeInfoVehicle(vehicleInfo: str) -> Vehicle:
    return Vehicle(*tuple(vehicleInfo.split()))

def takeInfoOrder(orderInfo: str) -> Request:
    return Request(*tuple(orderInfo.split()))

def readInputFile(data: list[str]):
    """ Read data file txt`

    Args:
        fileName (str): name of file data

    Returns:
        dataModel: class store data after handling
    """
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
    distanceMatrix = np.array(distanceMatrix)
    currentIndex += numberOfHub
    
    numberOfVehicle = int(data[currentIndex])
    currentIndex += 1
    
    for orderIdx in range(currentIndex, currentIndex + numberOfVehicle):
        vehicleList.append(takeInfoVehicle(data[orderIdx]))
    currentIndex += numberOfVehicle
    
    numberOfOrder = int(data[currentIndex])
    currentIndex += 1
          
    for orderIdx in range(currentIndex, currentIndex + numberOfOrder):
        orderList.append(takeInfoOrder(data[orderIdx]))
    
    return DataModel(distanceMatrix, vehicleList, orderList)
    
def writeVehicleNotUse(vehicle: Vehicle):
    time = convertSecondsToHours(vehicle.timeStart)
    print(1)
    print(f"{vehicle.startHub} {time} {time}")    
    
def writeRoute(route: Route):
    print(len(route.routeNodeList))    
    for node in route.routeNodeList:
        print(f"{node.idHub + 1} {len(node.requestProcessStatus)} {convertSecondsToHours(node.timeCome)} {convertSecondsToHours(node.timeGo)}")
        for request in node.requestProcessStatus:
            timeProcess = node.timeRequestProcessing[request][0]
            print(f"{abs(request)} {convertSecondsToHours(timeProcess)}" )
        
    
def writeOutFile(solution: Solution, dataModel: DataModel):
    vehicleList = dataModel.vehicleList
    locationOfVehicle = solution.locationOfVehicle 
    routeList = solution.routeList
    for indexRoute in locationOfVehicle:
        if indexRoute == -1:
            writeVehicleNotUse(vehicleList[indexRoute])
        else:
            writeRoute(routeList[indexRoute])
    

# lines = []
# while True:
#     line = input()
#     if line:
#         lines.append(line)
#     else:
#         break

with open("data//test_data.txt") as f_obj:
        data = [line.strip("\n") for line in f_obj.readlines()]

dataModel = readInputFile(data)

a = Greedy().solve(dataModel)

# for route in a.routeList:
#     # print(route)
#     print("---------------------------")
#     print(f"route:  {route.requestProcessed}")
#     for node in route.routeNodeList:
#         print(node)
print(a.costFuction)
writeOutFile(a, dataModel)


    
    