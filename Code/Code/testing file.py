from SearchAlgorithm import *
from SubwayMap import *
from utils import *

if __name__=="__main__":
    ROOT_FOLDER = '../CityInformation/Lyon_smallCity/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)

    ###BELOW HERE YOU CAN CALL ANY FUNCTION THAT YOU HAVE PROGRAMED TO ANSWER THE QUESTIONS FOR THE TEST###
    #example - Used testing
    """"
    example_path = expand(Path([14, 13, 8, 12]), map)
    example_path = remove_cycles(example_path)
    for path in example_path:
        print(f"Route: {path.route}")
        print(f"Cost: {path.g}")
    
    route1 = depth_first_search(2, 7, map)
    route2 = depth_first_search(13, 1,map)
    route3 = depth_first_search(5, 12,map)
    route4 = depth_first_search(14, 10, map)
    print(route1.route)
    print(route2.route)
    print(route3.route)
    print(route4.route)

    route1 = breadth_first_search(2, 7, map)
    route2 = breadth_first_search(13, 1,map)
    route3 = breadth_first_search(5, 12,map)
    route4 = breadth_first_search(14, 10, map)
    print(route1.route)
    print(route2.route)
    print(route3.route)
    print(route4.route)

    distances = distance_to_stations([300, 111], map)
    for k, v in distances.items():
        print(f"{k}:{v}")
    print(round(distances[9], 6))
"""

    """"
    Test 1
    example_path = expand(Path([2]), map)
    print_list_of_path(example_path)
    Route: [2, 1]
    Route: [2, 3]
    Route: [2, 5]
    Route: [2, 10]
    """

    """"
    Test 2
    example_path = expand(Path([4,5]), map)
    print_list_of_path(example_path)
    Route: [4, 5, 2]
    Route: [4, 5, 4]
    Route: [4, 5, 6]
    Route: [4, 5, 10]
    """

    """""
    # Test 3
    example_path = expand(Path([4,5,6]), map)
    print_list_of_path(example_path)
    print("----------")
    example_path = remove_cycles(example_path)
    print_list_of_path(example_path)
    Route: [4, 5, 6, 5]
    Route: [4, 5, 6, 7]
    ----------
    Route: [4, 5, 6, 7]
    """

    """"
    # Test 4
    example_path = remove_cycles([Path([7,7])])
    print_list_of_path(example_path)

    (retorna buit)
    """

    """"
    # Test 5
    example_path = depth_first_search(3, 10, map)
    print_list_of_path([example_path])
    Route: [3, 2, 5, 6, 7, 8, 12, 11, 10]
    """

    """
    # Test 6
    example_path = depth_first_search( 10 , 10, map )
    print_list_of_path([example_path])
    Route: [10]
    """

    """""
    #Test 7
    example_path = depth_first_search( 1 , 10, map )
    print_list_of_path([example_path])
    print("--------------------")
    example_path = breadth_first_search( 1 , 10, map )
    print_list_of_path([example_path])
    Route: [1, 2, 5, 6, 7, 8, 12, 11, 10]
    --------------------
    Route: [1, 2, 10]
    """

    """"
    # Test 8 --> ERROR. Ha de retornar llista buida
    example_path = breadth_first_search( 10, 10000, map)
    print_list_of_path([example_path])
    ERROR
    """

    """
    # Test 9
    distances = distance_to_stations([0, 0], map)
    for k, v in distances.items():
        print(f"{k}:{v}")
    1:103.58571330062848
    4:142.57980221616245
    2:150.78461459976612
    5:150.78461459976612
    10:150.78461459976612
    11:172.10461934532728
    3:178.84350701101786
    6:181.1767093199344
    7:210.35446275275456
    9:231.97629189208106
    8:232.59406699226014
    12:232.59406699226014
    13:232.59406699226014
    14:275.68822970885066
    """

    


    

