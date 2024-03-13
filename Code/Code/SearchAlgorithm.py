# This file contains all the required routines to make an A* search algorithm.
#
__author__ = '1632368'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2023 - 2024
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map): #OK
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list = []

    if len(path.route) > 0:
        con = map.connections[path.last]
        for c, cost in con.items():
            n_path = Path(path.route.copy())
            n_path.add_route(c)
            #n_path.update_g(cost)
            path_list.append(n_path)

    else:
        raise TypeError("Path is empty, it has no routes")
    
    return path_list


def remove_cycles(path_list): #OK
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    paths = []

    for path in path_list:
        visited = set()
        cycle = False
        for element in path.route:
            if element in visited:
                cycle = True
                break
            visited.add(element)

        if not cycle:
            paths.append(path)
            
    return paths


def insert_depth_first_search(expand_paths, list_of_path): #OK
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    #Pseudocode --> Insert up front
    for path in reversed(expand_paths):
        list_of_path.insert(0,path)
    return list_of_path


def depth_first_search(origin_id, destination_id, map): #OK
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    paths = []
    root_path = Path([origin_id])
    paths.append(root_path)

    while len(paths) > 0 and paths[0].last != destination_id:
        path = paths.pop(0)
        paths = insert_depth_first_search(remove_cycles(expand(path,map)),paths)
        
    if len(paths) <= 0:
        return []
    
    elif paths[0].last == destination_id:
        return paths[0]
    
    else:
        return []


def insert_breadth_first_search(expand_paths, list_of_path): #OK
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    # Pseudocode --> Insert at the back
    for path in expand_paths:
        list_of_path.append(path)

    return list_of_path


def breadth_first_search(origin_id, destination_id, map): #OK
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    paths = []
    root_path = Path([origin_id])
    paths.append(root_path)

    while len(paths) > 0 and paths[0].last != destination_id:
        path = paths.pop(0)
        paths = insert_breadth_first_search(remove_cycles(expand(path,map)),paths)
        
    if len(paths) <= 0:
        return []
    
    elif paths[0].last == destination_id:
        return paths[0]
    
    else:
        return []


def calculate_cost(expand_paths, map, type_preference=0): # OK
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    if type_preference == 0:
        for path in expand_paths:
            path.update_g(1)
        return expand_paths
    
    elif type_preference == 1:
        i = 0 # Debugging
        for path in expand_paths:
            if path.last in map.connections:
                con = map.connections[path.last]
                for c, cost in con.items():
                    if path.penultimate == c:
                        path.update_g(cost)
                        break
        return expand_paths
    
    elif type_preference == 2:
        # Distance = speed * time
        for path in expand_paths:
            if path.last in map.connections:
                con = map.connections[path.last]
                line_number = map.stations[path.last]['line']
                line_velocity = map.velocity[line_number]
                for c, cost in con.items():
                    if path.penultimate == c:
                        path.update_g(cost * line_velocity)
                        break
        return expand_paths
    
    elif type_preference == 3:
        for path in expand_paths:
            if len(path.route) > 2:
                path.update_g(1)
        return expand_paths

    else:
        print("Invalid type_preference value")
        return 0


def insert_cost(expand_paths, list_of_path): #OK
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    for path in expand_paths:
        list_of_path.append(path)
    
    list_of_path.sort(key=lambda path: (path.g, tuple(path.route)))

    return list_of_path


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
    Uniform Cost Search algorithm
    Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    if type_preference not in [0, 1, 2, 3]:
        print("Invalid type_preference value")
        return []
    
    paths = []

    root_path = Path([origin_id])

    paths.append(root_path)

    while len(paths) > 0 and paths[0].last != destination_id:
        print("#" * 50)
        path = paths.pop(0)
        ex = expand(path, map)
        el = remove_cycles(ex)
        c_list = calculate_cost(el, map, type_preference)
        print("Calculate Cost: ", print_list_of_path_with_cost(c_list))
        print("-" * 25)
        new_paths = copy.deepcopy(paths)
        paths = insert_cost(c_list, new_paths)
        print("Insert Cost: ", print_list_of_path_with_cost(paths))
        print("#" * 50)

    if len(paths) <= 0:
        return []
    elif paths[0].last == destination_id:
        return paths[0]
    else:
        return []


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0): #ERROR!!! - IDK HEURISTICS
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    if type_preference == 0: # Boolean --> Adjacent or not
        for path in expand_paths:
            path.update_h(1)
            if path.last == destination_id or destination_id in map.connections[path.last]:
                path.update_h(0)      
        return expand_paths
    
    elif type_preference == 1: # Eucledian distance / max speed
        max_speed = 45
        dest_coor = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]
        for path in expand_paths:
            if path.last in map.stations:
                coor = [map.stations[path.last]['x'], map.stations[path.last]['y']]
                path.update_h(euclidean_dist(coor, dest_coor) / max_speed)
        return expand_paths
    
    elif type_preference == 2: # Eucledian distance
        dest_coor = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]
        for path in expand_paths:
            if path.last in map.stations:
                coor = [map.stations[path.last]['x'], map.stations[path.last]['y']]
                path.update_h(euclidean_dist(coor, dest_coor))
        return expand_paths
    
    elif type_preference == 3:  # Boolean - Do I need more jumps after?
        for path in expand_paths:
            if path.last == destination_id:
                path.update_h(0)
            else:
                more_transfers = True
                for connection in map.connections[path.last]:
                    if destination_id in map.connections[connection]:
                        more_transfers = False
                        break
                if not more_transfers:
                    path.update_h(0)
                else:
                    path.update_h(1)
        return expand_paths
    
    else:
        print("Invalid type_preference value")
        return 0


def update_f(expand_paths): #OK
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    if len(expand_paths) >= 0:
        for path in expand_paths:
            path.update_f()
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost): #TO DO - WEIRD
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    new_paths = []
    for path in expand_paths:
        if path.last in visited_stations_cost:
            if path.g < visited_stations_cost[path.last]:
                visited_stations_cost[path.last] = path.g
                new_paths.append(path)
        else:
            visited_stations_cost[path.last] = path.g
            new_paths.append(path)
    return new_paths, list_of_path, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path): #TEST!!!
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    for path in expand_paths:
        list_of_path.append(path)
    
    list_of_path.sort(key=lambda path: path.f)

    
    return list_of_path


def distance_to_stations(coord, map): #OK
    """
        From coordinates, it computes the distance to all stations in map.
        Format of the parameter is:
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    distances = {}

    for station_id, station_info in map.stations.items():
        station_coor = [station_info['x'], station_info['y']]
        # d = round(euclidean_dist(coord, station_coor),2)
        distances[station_id] = euclidean_dist(coord, station_coor)

    sorted_distances = dict(sorted(distances.items(), key=lambda x: (x[1],x[0])))

    return sorted_distances


def Astar(origin_id, destination_id, map, type_preference=0):# TO DO 
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    paths = []
    root_path = Path([origin_id])
    paths.append(root_path)

    while len(paths) > 0 and paths[0].last != destination_id:
        path = paths.pop(0)
        paths = insert_depth_first_search(remove_cycles(expand(path,map)),paths)
        
    if len(paths) <= 0:
        return []
    
    elif paths[0].last == destination_id:
        return paths[0]
    
    else:
        return []


def Astar_improved(origin_coord, destination_coord, map): #TO DO
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
            destination_coord (list): Two REAL values, which refer to the coordinates of the final position
            map (object of Map class): All the map information

        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
    """
    pass
