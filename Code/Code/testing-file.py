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



    ###BELOW HERE YOU CAN CALL ANY FUNCTION THAT YOU HAVE PROGRAMED TO ANSWER THE QUESTIONS FOR THE TEST###

    #example
    example_path = expand(Path([5]), map)
    print_list_of_path(example_path)
