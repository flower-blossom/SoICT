def createLocationOfRequests(tempSol, requestList: list) -> NoReturn:
    routeList = tempSol.routeList
    locationOfRequests = [-1 for _ in range(0, len(requestList) - 1)]
    numberOfRoute = 0
    for routeObject in routeList:
        for order in routeObject.orderOfRequestProcessed:
            locationOfRequests[abs(order)] = numberOfRoute
        numberOfRoute += 1
    return locationOfRequests

    # local search with function is number of request and time


def insertRequestToNewRoute(newRequest: int,
                            route: Route,
                            requestList: list,
                            distanceMatrix: list) -> (bool, int):
    """
    Insert request to new route if valid
    """

    pickupStatus = newRequest
    deliveryStatus = -newRequest
    routeNodeList = route.routeNodeList
    vehicleDict = route.vehicleDict
    orderOfRequestProcessed = route.orderOfRequestProcessed

    usingTime = -1
    idxDelivery = idxPickUp = -1
    idxPickUp, _ = findPlaceToInsert(pickupStatus, orderOfRequestProcessed, routeNodeList,
                                     vehicleDict, requestList, distanceMatrix)
    if idxPickUp != -1:
        print(f"idxPickUp: {idxPickUp}")
        orderOfRequestProcessed.insert(idxPickUp, pickupStatus)
        # try to insert delivery request
        idxDelivery, usingTime = findPlaceToInsert(deliveryStatus, orderOfRequestProcessed, routeNodeList,
                                                   vehicleDict, requestList, distanceMatrix)
        print(f"idxDelivery: {idxDelivery}")
        orderOfRequestProcessed.pop(idxPickUp)

    if idxDelivery == -1 or idxPickUp == -1:
        return False, usingTime
    orderOfRequestProcessed.insert(idxPickUp, pickupStatus)
    orderOfRequestProcessed.insert(idxDelivery, -deliveryStatus)
    route.requestProcess.add(newRequest)
    return True, usingTime




def singlePairedInsertion(tempSol: list, requestList: list, distanceMatrix: list) -> NoReturn:
    routeList = tempSol.routeList
    for idxCurentRoute in range(len(routeList)):
        curentRoute = routeList[idxCurentRoute]
        for idxAnotherRoute in range(len(routeList)):
            # print(f"curentRoute: {idxCurentRoute}")
            # print(f"idxAnotherRoute: {idxAnotherRoute}")
            if idxCurentRoute == idxAnotherRoute:
                pass
            else:
                anotherRoute = routeList[idxAnotherRoute]

                for request in anotherRoute.requestProcess:
                    insertCondition, _ = insertRequestToNewRoute(request, curentRoute,
                                                                 requestList, distanceMatrix)
                    if insertCondition is True:
                        anotherRoute.requestProcess.remove(request)
                        anotherRoute.orderOfRequestProcessed.remove(request)
                        anotherRoute.orderOfRequestProcessed.remove(-request)
                        print("Insert complete")


def findIdxOfRequestInOrder(request: int, orderOfRequestProcessed: list) -> NoReturn:
    indexOfOldPickupRequest = orderOfRequestProcessed.index(request)
    indexOfOldPickupDelivery = orderOfRequestProcessed.index(-request)
    return indexOfOldPickupRequest, indexOfOldPickupDelivery


def deletePairRequestInOrder(indexOfOldPickupRequest: int, indexOfOldPickupDelivery: int,
                             orderOfRequestProcessed: list) -> NoReturn:
    orderOfRequestProcessed.pop(indexOfOldPickupRequest)
    orderOfRequestProcessed.pop(indexOfOldPickupDelivery - 1)


def insertRequestToRoute(request: int, indexOfOldPickupRequest: int, indexOfOldPickupDelivery: int,
                         orderOfRequestProcessed: list, requestProcess: dict) -> NoReturn:
    requestProcess.add(request)
    orderOfRequestProcessed.insert(indexOfOldPickupRequest, request)
    orderOfRequestProcessed.insert(indexOfOldPickupDelivery, -request)


def requestExchangeOperator(newRequest: int, oldRequest: int, route: Route,
                            requestList: list, distanceMatrix: list) -> bool:
    orderOfRequestProcessed = route.orderOfRequestProcessed
    indexOfOldPickupRequest, indexOfOldPickupDelivery = findIdxOfRequestInOrder(oldRequest,
                                                                                orderOfRequestProcessed)

    # temporary delete oldRequest
    usingTime = -1
    deletePairRequestInOrder(indexOfOldPickupRequest, indexOfOldPickupDelivery,
                             orderOfRequestProcessed)
    insertCondition, usingTime = insertRequestToNewRoute(newRequest, route,
                                                         requestList, distanceMatrix)
    route.requestProcess.remove(oldRequest)
    if insertCondition is False:
        insertRequestToRoute(oldRequest, indexOfOldPickupRequest, indexOfOldPickupDelivery,
                             orderOfRequestProcessed, route.requestProcess)
    return usingTime


def swapRequestInTwoRoute(firstRoute: Route, secondRoute: Route,
                          requestList: list, distanceMatrix: list) -> bool:
    stopCondition = False
    currentUsingTime = totalUsingTime(firstRoute, secondRoute)
    for request in firstRoute.requestProcess:
        for secondRouteRequest in secondRoute.requestProcess:
            usingFirstRouteTime = requestExchangeOperator(secondRouteRequest, request,
                                                          firstRoute, requestList, distanceMatrix)
            usingSecondRouteTime = requestExchangeOperator(request, secondRouteRequest,
                                                           secondRoute, requestList, distanceMatrix)
        if usingSecondRouteTime + usingFirstRouteTime < currentUsingTime:
            print(
                f"Can Swap old using new: {usingSecondRouteTime + usingFirstRouteTime}, old: {currentUsingTime} ")
            _, firstRoute.routeNodeList = checkValidTimePartRoute(firstRoute.orderOfRequestProcessed,
                                                                  firstRoute.routeNodeList[-1],
                                                                  firstRoute.vehicleDict,
                                                                  requestList,
                                                                  distanceMatrix)
            _, firstRoute.routeNodeList = checkValidTimePartRoute(secondRoute.orderOfRequestProcessed,
                                                                  secondRoute.routeNodeList[-1],
                                                                  secondRoute.vehicleDict,
                                                                  requestList,
                                                                  distanceMatrix)
            currentUsingTime = totalUsingTime(firstRoute, secondRoute)
            stopCondition = True

    return stopCondition


def swapRequestOperator(tempSol: Solution, requestList: list, distanceMatrix: list) -> NoReturn:
    routeList = tempSol.routeList
    stopCondition = True
    while stopCondition:
        for idxCurentRoute in range(len(routeList)):
            currentRoute = routeList[idxCurentRoute]
            for idxAnotherRoute in range(len(routeList)):
                # print(f"curentRoute: {idxCurentRoute}")
                # print(f"idxAnotherRoute: {idxAnotherRoute}")
                if idxCurentRoute == idxAnotherRoute:
                    pass
                else:
                    # anotherRoute = routeList[idxAnotherRoute]
                    swapCondition = swapRequestInTwoRoute(currentRoute, routeList[idxAnotherRoute],
                                                          requestList, distanceMatrix)
                    if swapCondition is True:
                        stopCondition = stopCondition


def localSearch(sol, dataModel):
    tempSol = deepcopy(sol)
    requestList = dataModel.requestList
    distanceMatrix = dataModel.distanceMatrix
    updateRequestProcess(tempSol.routeList)
    candidateVehicle = [i for i in range(len(dataModel.vehicleList))]
    locationOfVehicle = tempSol.locationOfVehicle.copy()
    # locationOfRequests = createLocationOfRequests(
    #     tempSol, requestList)
    # print(locationOfRequests)
    # singlePairedInsertion(tempSol, requestList, distanceMatrix)
    swapRequestOperator(tempSol, requestList, distanceMatrix)
    return tempSol
    # localsearch through route Node
    # while True:

