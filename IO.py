import numpy as np
from operators import DataModel, Request, Vehicle  
from Greedy import Greedy

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
    print(data)
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
    
# a = readInputFile('data//test_data.txt')

lines = []
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        break
dataModel = readInputFile(lines)

print(dataModel)
a = Greedy().solve(dataModel)
# def readOutput(fileName):
#     with open(fileName) as f_obj:
#         data = [line.strip("\n") for line in f_obj.readlines()]

#     routes = []
#     currentIndex = 0
#     while currentIndex > len(data):
#         route = []
#         currentIndex += 1
#         numberOfPointInRoute = int(data[currentIndex]) 
#         for line in range(currentIndex, currentIndex + numberOfPointInRoute):
#             if line == currentIndex and line == currentIndex + numberOfPointInRoute:
                
#             else:
                
        
#     for 
    
    
    
    
    
    
# def calculateScore(solution,):
#     return None

# def outputToSolution(file,):
#     return None

# def writeOutput(solution):
    
#     return None