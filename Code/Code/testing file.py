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

    #example
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


