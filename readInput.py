import numpy as np
from Vehicle import Vehicle
from Order import Order
    

def takeInfoVehicle(vehicleInfo: str) -> Vehicle:
    return Vehicle(*tuple(vehicleInfo.split()))

def takeInfoOrder(orderInfo: str) -> Order:
    return Order(*tuple(orderInfo.split()))

def readInputFile(fileName):
    """ Read data file txt`

    Args:
        fileName (str): name of file data

    Returns:
        dataModel: class store data after handling
    """
    with open(fileName) as f_obj:
        data = [line.strip("\n") for line in f_obj.readlines()]

    currentIndex = 0
    numberOfHub = int(data[currentIndex]) 
    currentIndex += 1
    
    distanceMatrix = []
    for hubNumber in range(currentIndex, currentIndex + numberOfHub):
        arr = data[hubNumber]
        distanceMatrix.append(list(map(int, arr.split())))
    distanceMatrix = np.array(distanceMatrix)
    currentIndex += numberOfHub
    
    numberOfVehicle = int(data[currentIndex])
    currentIndex += 1
    
    vehicleArr = []
    for orderIdx in range(currentIndex, currentIndex + numberOfVehicle):
        vehicleArr.append(takeInfoVehicle(data[orderIdx]))
    currentIndex += numberOfVehicle
    
    numberOfOrder = int(data[currentIndex])
    currentIndex += 1
          
    print(currentIndex)
    orderArr = []
    for orderIdx in range(currentIndex, currentIndex + numberOfOrder):
        orderArr.append(takeInfoOrder(data[orderIdx]))
    
    
readInputFile('test_input.txt')


# def calculateScore(solution,):
#     return None

# def outputToSolution(file,):
#     return None

# def writeOutput(solution):
    
#     return None