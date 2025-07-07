from SearchAlgorithm import *
from SubwayMap import *
from utils import *

if __name__=="__main__":
    ROOT_FOLDER = '../CityInformation/Barcelona_City/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)

    ### BELOW HERE YOU CAN CALL ANY FUNCTION THAT yoU HAVE PROGRAMED TO ANSWER THE QUESTIONS OF THE EXAM ###
    ### this code is just for you, you won't have to upload it after the exam ###

    #this is an example of how to call some of the functions that you have programed
    #example_path=uniform_cost_search(9, 3, map, 1)
    #print_list_of_path_with_cost([example_path])

    #pregunta 1; remove cycles sobre una lista de caminos
    #path_list = remove_cycles([Path([8,3,4,2,5]),Path([8,3,4,2,1]),Path([8,3,4,2,8]),Path([8,3,4,2,3]),Path([8,3,4,2,7])])
    #print_list_of_path(path_list)

    #pregunta 2; estaciones con conexión con Navas L1
    #estacion = Path([2])
    #lista = expand(estacion, map)
    #print_list_of_path(lista)

    #pregunta 3; cerca en profunditat en un cami
    #lista = depth_first_search(22, 17, map)
    #print(lista.route)

    #pregunta 4; cost G en TEMPS del cami
    #example_path=uniform_cost_search(4, 7, map, 1)
    #print_list_of_path_with_cost([example_path])

    #pregunta 5; Astar amb criteri temps minim
    #lista = Astar(24, 2, map, 1)
    #print(lista.route)



