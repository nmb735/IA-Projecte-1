from SubwayMap import Map
import numpy as np
import math

# Infinite cost represented by INF
INF = 9999


def euclidean_dist(x, y):
    x1, y1 = x
    x2, y2 = y
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def read_station_information(filename):
    # read_station_information: Given a filename, it reads the information of this file.
    subway_map = Map()
    with open(filename, 'r', encoding='utf-8') as fileMetro:
        for line in fileMetro:
            information = line.split('\t')
            subway_map.add_station(int(information[0]), information[1], information[2], int(information[3]),
                                   int((information[4].replace('\n', '')).replace(' ', '')))
    return subway_map


def read_information(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        vel = fp.readlines()
        vel = [i.split('\n')[0] for i in vel]
    vector = [int(v.split(':')[-1]) for v in vel]
    return vector


def read_cost_table(filename):
    adj_matrix = np.loadtxt(filename)
    row, col = adj_matrix.nonzero()
    connections = {}
    for r, c in zip(row, col):
        if r + 1 not in connections:
            connections[r + 1] = {c + 1: adj_matrix[r][c]}
        else:
            connections[r + 1].update({c + 1: adj_matrix[r][c]})

    return connections


def print_list_of_path(path_list):
    for p in path_list:
        print("Route: {}".format(p.route))


def print_list_of_path_with_cost(path_list):
    for p in path_list:
        print("Route: {}, \t Cost: {}".format(p.route, p.g))
