# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1600946'
__group__ = 'DJ.17'

import operator

# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2022 - 2023
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


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

    path_list = [] #creem la llista que mes endavant retornarem
    for estacio in map.connections.keys(): #mirem el mapa i si coincideix amb l'ultima estació
        if estacio == path.last:
            for x in map.connections[estacio].keys():
                llista_cami = copy.deepcopy(path)
                llista_cami.add_route(x)
                path_list.append(llista_cami) #copiem el camí i l'afegim a la llista que retornem

    return path_list

    pass


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    llista_final = path_list.copy() #copiem la llista que ens passen per parametre per retornarla sense cicles
    for cami in path_list:
        for estacio in cami.route[:-1]:
            if estacio == cami.last: #si una estacio a un cami es igual a l'element final
                llista_final.remove(cami)
                break #eliminem el cami del cicle

    return llista_final

    pass


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
    for cami_no_visitat in list_of_path:
        expand_paths.append(cami_no_visitat)

    return expand_paths

    pass


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
    llista_DFS = [Path(origin_id)]

    while((llista_DFS[0].last != destination_id) and (llista_DFS is not None)): #mentre no arribem al final i no estigui buit...
        C = llista_DFS[0] #seguim l'algoritme presentat a la presentació
        E = expand(C, map)
        E = remove_cycles(E)
        llista_DFS = insert_depth_first_search(E, llista_DFS[1:])

    if (llista_DFS != None): #si no esta buida retornem la llista
        return llista_DFS[0]
    else:
        return ("Error")

    pass


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
    for cami_no_visitat in expand_paths:
        list_of_path.append(cami_no_visitat)

    return list_of_path

    pass


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
    llista_BFS = [Path(origin_id)]

    while((llista_BFS[0].last != destination_id) and (llista_BFS is not None)):
        C = llista_BFS[0] #seguim l'algoritme de la presentació
        E = expand(C, map)
        E = remove_cycles(E)
        llista_BFS = insert_breadth_first_search(E, llista_BFS[1:])

    if (llista_BFS != None):
        return llista_BFS[0]
    else:
        return ("Error")

    pass


def calculate_cost(expand_paths, map, type_preference):
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

    preferencia = type_preference

    if(preferencia == 0):
        for cami in expand_paths: #mirem els camins dels camins fills
            cami.update_g(1)

    if(preferencia == 1):
        for cami in expand_paths:
            temps = map.connections[cami.penultimate][cami.last]
            cami.update_g(temps)

    if(preferencia == 2):
        for cami in expand_paths:
            if(map.stations[cami.last]['line'] == map.stations[cami.penultimate]['line']):
                temps = map.connections[cami.penultimate][cami.last]
                velocitat = map.stations[cami.penultimate]['velocity']
                distancia = velocitat * temps
                cami.update_g(distancia)

    if(preferencia == 3):
        for cami in expand_paths:
            if(map.stations[cami.last]['line'] != map.stations[cami.penultimate]['line']):
                cami.update_g(1)
    return expand_paths

    pass


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
    llista_paths = list_of_path

    for cami in expand_paths:
        llista_paths.append(cami)

    #ordenem segons sigui el cost
    llista_paths = sorted(llista_paths, key = operator.attrgetter('g'))

    return llista_paths

    pass


def uniform_cost_search(origin_id, destination_id, map, type_preference):
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
    llista_cost_uniforme = [Path(origin_id)]

    while((llista_cost_uniforme[0].last != destination_id) and (llista_cost_uniforme is not None)):
        C = llista_cost_uniforme[0]
        E = expand(C,map)
        E = remove_cycles(E)
        C = calculate_cost(E, map, type_preference)
        llista_cost_uniforme = insert_cost(C, llista_cost_uniforme[1:])

    return llista_cost_uniforme[0]

    pass


def calculate_heuristics(expand_paths, map, destination_id, type_preference):
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
    preferencia = type_preference

    if(preferencia == 0):
        for cami in expand_paths:
            if ((cami.last != destination_id) and (cami.last not in map.connections[destination_id].keys())):
                cami.update_h(1)
            else:
                cami.update_h(0)
    if(preferencia == 1):
        for cami in expand_paths:
            distancia = euclidean_dist([map.stations[cami.last]['x'], map.stations[cami.last]['y']], [map.stations[destination_id]['x'], map.stations[destination_id]['y']])
            velocitat = max(map.velocity.values())  # necessitem la velocitat mes gran per que el temps sigui minim
            temps = distancia / velocitat
            cami.update_h(temps)
    if(preferencia == 2):
        for cami in expand_paths:
            distancia = euclidean_dist([map.stations[cami.last]['x'], map.stations[cami.last]['y']],[map.stations[destination_id]['x'], map.stations[destination_id]['y']])
            cami.update_h(distancia)
    if(preferencia == 3):
        for cami in expand_paths:
            if (map.stations[cami.last]['line'] != map.stations[destination_id]['line']):
                cami.update_h(1)
            else:
                cami.update_h(0)

    return expand_paths

    pass


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for cami in expand_paths:
        cami.update_f()

    return expand_paths

    pass


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
    for cami in expand_paths:
        if(cami.last in visited_stations_cost.keys()):
            cost_estacions = visited_stations_cost[cami.last]

            if (cami.g >= cost_estacions):
                expand_paths.remove(cami)
            else:
                visited_stations_cost[cami.last] = cami.g

                for cami_aux in list_of_path:
                    if(cami_aux.last == cami.last):
                        list_of_path.remove(cami_aux)
        else:
            visited_stations_cost[cami.last] = cami.g

    return expand_paths, list_of_path, visited_stations_cost

    pass


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
    for cami in expand_paths:
        list_of_path.append(cami)

    list_of_path = sorted(list_of_path, key = operator.attrgetter('f'))

    return list_of_path

    pass


def coord2station(coord, map):
    """
        From coordinates, it searches the closest stations.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """
    posibles_origens = []
    llista_id = []
    llista_distancia = []

    for estacions in map.stations:
        distancia_x = map.stations[estacions]['x'] - coord[0]
        distancia_y = map.stations[estacions]['y'] - coord[1]
        distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)
        llista_distancia.append(distancia)
        llista_id.append(estacions)

    i = 1
    min_distancia = llista_distancia[0]
    min_index = llista_id[0]
    while (i != len(llista_distancia)):
        if llista_distancia[i] < min_distancia:
            min_distancia = llista_distancia[i]
            min_index = llista_id[i]
        i = i + 1
    posibles_origens.append(min_index)
    i = 0

    while (i != len(llista_distancia)):
        if (llista_distancia[i] == min_distancia and min_index != llista_id[i]):
            posibles_origens.append(llista_id[i])
        i = i + 1

    print(posibles_origens)

    return posibles_origens

    pass


def Astar(origin_id, destination_id, map, type_preference):
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
    coord_origin = [map.stations[origin_id]['x'],map.stations[origin_id]['y']]
    coord_destinacio = [map.stations[destination_id]['x'], map.stations[destination_id]['y']]

    origen = coord2station(coord_origin, map)[0]
    destinacio = coord2station(coord_destinacio,map)[0]

    llista_Astar = [Path(origen)]
    cost_estacions_visitades = {}

    while((llista_Astar[0].last != destinacio) and (llista_Astar is not None)):
        C = llista_Astar[0]
        E = expand(C, map)
        E = remove_cycles(E)
        C = calculate_cost(E, map, type_preference)
        H = calculate_heuristics(C, map, destination_id, type_preference)
        F = update_f(H)
        F, llista_Astar, cost_estacions_visitades = remove_redundant_paths(F, llista_Astar, cost_estacions_visitades)
        llista_Astar = insert_cost(F, llista_Astar[1:])

    if(llista_Astar != None):
        return llista_Astar[0]
    else:
        return ("Error")

    pass
