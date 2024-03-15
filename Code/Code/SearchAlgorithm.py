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

def print_list_of_path_with_heu(path_list):
    for p in path_list:
        print("Route: {}, \t Cost: {}".format(p.route, round(p.h,2)))

def print_list_of_path_with_f(path_list):
    for p in path_list:
        print("Route: {}, \t Cost: {}".format(p.route, round(p.f,2)))

def print_list_of_path_with_data(path_list):
    for p in path_list:
        print(f"Route: {p.route}, Cost: {round(p.g,2)}, Heuristic: {round(p.h,2)}, f: {round(p.f,2)}")

def expand(path, map):
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
            n_path.g = path.g
            path_list.append(n_path)

    else:
        raise TypeError("Path is empty, it has no routes")
    
    return path_list

def remove_cycles(path_list):
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

def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    #Pseudocode: Insert up front
    for path in reversed(expand_paths):
        list_of_path.insert(0,path)
    return list_of_path

def depth_first_search(origin_id, destination_id, map):
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
    paths = [Path([origin_id])]

    while len(paths) > 0 and paths[0].last != destination_id:
        path = paths.pop(0)
        paths = insert_depth_first_search(remove_cycles(expand(path,map)),paths)
        
    if len(paths) <= 0:
        return []
    
    elif paths[0].last == destination_id:
        return paths[0]
    
    else:
        return []

def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    # Pseudocode: Insert at the back
    for path in expand_paths:
        list_of_path.append(path)

    return list_of_path

def breadth_first_search(origin_id, destination_id, map):
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
    paths = [Path([origin_id])]

    while len(paths) > 0 and paths[0].last != destination_id:
        path = paths.pop(0)
        paths = insert_breadth_first_search(remove_cycles(expand(path,map)),paths)
        
    if len(paths) <= 0:
        return []
    
    elif paths[0].last == destination_id:
        return paths[0]
    
    else:
        return []

def calculate_cost(expand_paths, map, type_preference=0):
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
            distance = distance_to_stations([map.stations[path.penultimate]['x'], map.stations[path.penultimate]['y']], map)[path.last]
            if distance != 0.0:
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
            line_number = int(map.stations[path.last]['line'])
            prev_line_number = int(map.stations[path.penultimate]['line'])
            if line_number != prev_line_number:
                path.update_g(1)
        return expand_paths

    else:
        print("Invalid type_preference value")
        return expand_paths

def insert_cost(expand_paths, list_of_path):
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
    
    paths = [Path([origin_id])]

    while len(paths) > 0 and paths[0].last != destination_id:
        path = paths.pop(0)
        paths = insert_cost(calculate_cost(remove_cycles(expand(path,map)),map,type_preference),paths) 

    if len(paths) <= 0:
        return []
    elif paths[0].last == destination_id:
        return paths[0]
    else:
        return []

def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
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
    if type_preference == 0: # Boolean - Adjacent or not
        for path in expand_paths:
            path.update_h(1)
            if path.last == destination_id:
                path.update_h(0)      
        return expand_paths
    
    elif type_preference == 1: # Eucledian distance / max speed
        max_speed = 0
        for station_id, station_info in map.stations.items():
            velocity = station_info['velocity']
            if velocity > max_speed:
                max_speed = velocity
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
    
    elif type_preference == 3:  # Same line: h = 1; else: h = 0
        for path in expand_paths:
            if path.last == destination_id:
                path.update_h(0)
            else:
                line_number = map.stations[path.last]['line']
                dest_line_number = map.stations[destination_id]['line']
                if line_number != dest_line_number:
                    path.update_h(1)
        return expand_paths
    
    else:
        print("Invalid type_preference value")
        return 0

def update_f(expand_paths):
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

def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
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
        if path.g < visited_stations_cost.get(path.last, float('inf')):
            new_paths.append(path)
            visited_stations_cost[path.last] = path.g
                
    new_list_of_path = []
    for last_path in list_of_path:
        remove = False
        for new_path in new_paths:
            if new_path.last in last_path.route:
                remove = True
                break
        if not remove:
            new_list_of_path.append(last_path)
    
    return new_paths, new_list_of_path, visited_stations_cost

def insert_cost_f(expand_paths, list_of_path):
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

def distance_to_stations(coord, map):
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
        distances[station_id] = euclidean_dist(coord, station_coor)

    sorted_distances = dict(sorted(distances.items(), key=lambda x: (x[1],x[0])))

    return sorted_distances

def Astar(origin_id, destination_id, map, type_preference=0): 
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
    paths = [Path([origin_id])]
    visited_stations_cost = {}

    while len(paths) > 0 and paths[0].last != destination_id:
        path = paths.pop(0)
        expand_paths = update_f(calculate_heuristics(calculate_cost(remove_cycles(expand(path,map)), map, type_preference), map, destination_id, type_preference))
        expand_paths, paths, visited_stations_cost = remove_redundant_paths(expand_paths, paths, visited_stations_cost)
        paths = insert_cost_f(expand_paths, paths)

    if len(paths) <= 0:
        return []
    
    elif paths[0].last == destination_id:
        return paths[0]
    
    else:
        return []

def Astar_improved(origin_coord, destination_coord, map):
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
    walk_speed = 5
    new_map = copy.deepcopy(map)
    new_map.add_station(0, "Origin", 0, origin_coord[0], origin_coord[1])
    new_map.add_station(-1, "Destination", 0, destination_coord[0], destination_coord[1])
    new_map.stations[0]['velocity'] = walk_speed
    new_map.stations[-1]['velocity'] = walk_speed

    # Add connections from origin to all stations
    distances_origin = distance_to_stations(origin_coord, map)
    new_map.connections[0] = {}
    for station_id, distance in distances_origin.items():
        new_map.connections[0][station_id] = distance / walk_speed
        new_map.connections[station_id][0] = distance / walk_speed
    
    # Add connections of destination to all stations
    distances_destination = distance_to_stations(destination_coord, map)
    new_map.connections[-1] = {}
    for station_id, distance in distances_destination.items():
        new_map.connections[station_id][-1] = distance / walk_speed
        new_map.connections[-1][station_id] = distance / walk_speed

    # Connect origin to destination
    new_map.connections[0][-1] = euclidean_dist(origin_coord, destination_coord) / walk_speed
    new_map.connections[-1][0] = euclidean_dist(origin_coord, destination_coord) / walk_speed

    # Run A* algorithm
    optimal = Astar(0, (-1), new_map, 1)

    return optimal
  

