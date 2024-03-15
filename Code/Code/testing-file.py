from SearchAlgorithm import *
from SubwayMap import *
from utils import *

def create_path_with_cost_g(list_nodes, cost_g):
    path = Path(list_nodes)
    path.g = cost_g
    return path

def print_list_of_path_with_heu(path_list):
    for p in path_list:
        print("Route: {}, \t Cost: {}".format(p.route, round(p.h,2)))

def test_1(n):
    print(f"He programat i provat {n} funcions.")

def test_2():
    example_path = calculate_cost(expand(Path([2]), map), map, 3)
    print_list_of_path_with_cost(example_path)

def test_3():
    example_path = expand(Path([8]), map)
    calculate_cost(example_path, map,2)
    print_list_of_path_with_cost(example_path)

def test_4():
    path = uniform_cost_search(10, 14, map, 0)
    print_list_of_path_with_cost([path])

def test_5():
    path = uniform_cost_search(10, 10, map, 2)
    print_list_of_path_with_cost([path])

def test_6():
    print("No llegible")

def test_7(x,y):
    d = distance_to_stations([x,y], map)
    for s, x in d.items():
        print(f"Station: {s}; Distance: {x}.")

def test_8():
    x = Astar(4,14,map,1)
    print_list_of_path_with_cost([x])

def test_9(x):
    print(f"Espabila crack, la has liado en {x} funciones (como minimo).")

def test_main():
    print("INITIALIZING TESTS")
    print("#"*50)
    i = 0
    print("="*25)
    print("Test 1")
    print("="*25)
    t1 = int(input("How many functions have you programmed and tested? "))
    test_1(t1)
    t1 = input("La has liado? (y/n) ")
    if t1 == "y":
        i += 1
    print("#"*50)
    print("="*25)
    print("Test 2")
    print("="*25)
    test_2()
    t2 = input("La has liado? (y/n) ")
    if t2 == "y":
        i += 1
    print("#"*50)
    print("="*25)
    print("Test 3")
    print("="*25)
    test_3()
    t3 = input("La has liado? (y/n) ")
    if t3 == "y":
        i += 1
    print("#"*50)
    print("="*25)
    print("Test 4")
    print("="*25)
    test_4()
    t4 = input("La has liado? (y/n) ")
    if t4 == "y":
        i += 1
    print("#"*50)
    print("="*25)
    print("Test 5")
    print("="*25)
    test_5()
    t5 = input("La has liado? (y/n) ")
    if t5 == "y":
        i += 1
    print("#"*50)
    print("="*25)
    print("Test 6")
    print("="*25)
    test_6()
    t6 = input("La has liado? (y/n) ")
    if t6 == "y":
        i += 1
    print("#"*50)
    print("="*25)
    print("Test 7")
    print("="*25)
    x = int(input("X Coordinate: "))
    y = int(input("Y Coordinate: "))
    test_7(x,y)
    t7 = input("La has liado? (y/n) ")
    if t7 == "y":
        i += 1
    print("#"*50)
    print("="*25)
    print("Test 8")
    print("="*25)
    test_8(i)

def get_cost(path, subway_map, type_preference):
    new_path = Path([path.head])
    for i in range(1, len(path.route)):
        new_path.add_route(path.route[i])
        paths_with_cost = calculate_cost([new_path], subway_map, type_preference)
        new_path = paths_with_cost[0]
    return new_path

def support_session_test():
    print()
    print("="*50)
    print("Test 1: Transfer ")
    print("-"*25)
    expanded = expand(Path([2]), map)
    print_list_of_path([path for path in calculate_cost(expanded, map, 3) if (path.g > 0)])
    print(f"Expected result: [2, 5] and [2, 10]")
    print("="*50)
    
    print()
    print("="*50)
    print("Test 2: Closest Stations ")
    print("-"*25)
    expanded = expand(Path([8]), map)
    expanded = calculate_cost(expanded, map, 2)
    expanded = sorted(expanded, key=lambda item: item.g)
    print_list_of_path(expanded)
    print(f"Expected result: [8, 12] and [8, 13]")
    print("="*50)
    
    print()
    print("="*50)
    print("Test 3: Stops ")
    print("-"*25)
    best_path = uniform_cost_search(10, 14, map, 0)
    print(best_path.g)
    print(f"Expected result: 4")
    print("="*50)
    
    print()
    print("="*50)
    print("Test 4: Uniform Cost Search")
    print("-"*25)
    best_path = uniform_cost_search(10, 10, map, 2)
    print(best_path.route)
    print(best_path.g)
    print(f"Expected result: [10], 0")

    print()
    print("="*50)
    print("Test 5: Heuristic")
    print("-"*25)
    expanded_paths = [Path([10, 7 , 6]), Path([10, 7, 8])]
    updated_paths = calculate_heuristics(expanded_paths, map, 9, 1)
    updated_paths = update_f(updated_paths)
    heuristic_values = sorted([path.h for path in updated_paths])
    print(heuristic_values)
    print(f"Expected result: 0,63")
    print("="*50)
    
    print()
    print("="*50)
    print("Test 6: Distance to stations")
    print("-"*25)
    print(distance_to_stations([108, 206], map))
    print(f"Expected result: 8, 12, 13")
    print("="*50)
    
    print()
    print("="*50)
    print("Test 7: Astar")
    print("-"*25)
    best_path = Astar(4, 14, map, 1)
    print(best_path.route,"\n", best_path.g)
    print(f"Expected result: [4, 5, 6, 7, 8, 13, 14], 50.1964")
    print("="*50)

if __name__=="__main__":
    ROOT_FOLDER = '../CityInformation/Lyon_SmallCity/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)

    support_session_test()
    
    

    