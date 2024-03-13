from SearchAlgorithm import *
from SubwayMap import *
from utils import *

def print_list_of_path_with_heu(path_list):
    for p in path_list:
        print("Route: {}, \t Cost: {}".format(p.route, round(p.h,2)))

if __name__=="__main__":
    ROOT_FOLDER = '../CityInformation/Lyon_SmallCity/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)

    #example_path = expand(Path([5]), map)
    #print_list_of_path_with_cost(example_path)


    route = uniform_cost_search(9, 3, map, 0)
    print_list_of_path_with_cost([route])
    print_list_of_path_with_cost(calculate_cost([Path([9, 8, 7, 6, 5, 2, 3])], map, 0))
    print("#"*50)

    route = uniform_cost_search(9, 3, map, 1)
    print_list_of_path_with_cost([route])
    print_list_of_path_with_cost(calculate_cost([Path([9, 8, 12, 11, 10, 2, 3])], map, 1))
    print("#"*50)

    route = uniform_cost_search(9, 3, map, 2)
    print_list_of_path_with_cost([route])
    print_list_of_path_with_cost(calculate_cost([Path([9, 8, 12, 11, 10, 2, 3])], map, 2))
    print("#"*50)

    route = uniform_cost_search(9, 3, map, 3)
    print_list_of_path_with_cost([route])
    print_list_of_path_with_cost(calculate_cost([Path([9, 8, 7, 6, 5, 2, 3])], map, 3))
    print("#"*50)