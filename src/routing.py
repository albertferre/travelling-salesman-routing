from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Optional


def print_solution(manager, routing, solution, names=None):
    """
    Prints the solution on the console.

    Args:
        manager: The routing index manager.
        routing: The routing model.
        solution: The solution obtained from the routing solver.
        names (Optional[List[str]]): List of names corresponding to node indices. Defaults to None.
    """
    index = routing.Start(0)
    plan_output = "Route for vehicle:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        idx = manager.IndexToNode(index)
        if names:
            print_value = names[idx]
        else:
            print_value = idx
        plan_output += " {} ->".format(print_value)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

    idx = manager.IndexToNode(index)
    if names:
        print_value = names[idx]
    else:
        print_value = idx
    plan_output += " {}\n".format(print_value)
    plan_output += "Route distance: {:.1f}km\n".format(route_distance / 1000)
    print(plan_output)


def optimize_routes(
    distance_matrix: List[List[int]], depot: int, names: Optional[List[str]] = None
) -> List[int]:
    """
    Solves the vehicle routing problem and returns the optimized route.

    Args:
        distance_matrix (List[List[int]]): 2D list representing the distance matrix between nodes.
        depot (int): Index of the depot (starting point).
        names (Optional[List[str]]): List of names corresponding to node indices. Defaults to None.

    Returns:
        List[int]: The optimized route as a list of node indices.
    """
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix), 1, depot
    )  # num of vehicles set to 1

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console and return the optimized route.
    if solution:
        print_solution(manager, routing, solution, names)
        route = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route
    else:
        return []
