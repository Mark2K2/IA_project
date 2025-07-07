__authors__ = ['1601188','1603325','1603591']
__group__ = 'DM.12'

import numpy as np
import Kmeans
import KNN
import utils
from utils_data import read_dataset, visualize_k_means, visualize_retrieval
import matplotlib.pyplot as plt
import time
import json
import os

#Anàlisi Qualitatu
def retrieval_by_color(llistaim, color_labels, preg):
    llista = []
    imatges = [ llistaim[x]           
        for x, color_label in enumerate(color_labels)
        if all(
               color.title()  in color_label 
               for color in preg
        ) 
        and not llista.append(x)
    ]

    return np.array(imatges), llista


def retrieval_by_shape(llistaim, class_labels, preg):
    llista = []
    imatges = [ llistaim[x]
        for x, class_label in enumerate(class_labels)
        if any(shape.title() == class_label for shape in preg) and not llista.append(x)
    ]
    return np.array(imatges), llista


def retrieval_combined(llistaim, color_labels, class_labels, preg):
    llista = []
    imatges = [ llistaim[x]
           for x, (color_label, class_label) in enumerate(zip(color_labels, class_labels))
           if all(
               color.title() in color_label for color in preg['color']
        ) 
           and any(
               shape.title() == class_label
               for shape in preg['shape']
        ) 
           and not llista.append(x)
       ]

    return np.array(imatges), llista

    
def kmeans(imatges):
    color_labels = []
    print('Inicialitzant centroides...')
    init = 'first'

    for x, test_img in enumerate(imatges):
        km = Kmeans.KMeans(test_img, options={'km_init' : init})
        km.find_bestK(8)
        color_labels.append(Kmeans.get_colors(km.centroids))
        os.system('cls')

    return np.array(color_labels)


def parse_search_pregunta(pregunta, colors, classes):
    pregunta = pregunta.split()
    tipus = ''
    forma = []
    colorp = []

    for paraula in pregunta:
        paraula = paraula.title()
        if paraula == 'And':
            continue
        if paraula == 'Quit':
            tipus = 'exit'
            break
        if paraula == 'Flip':
            paraula = 'Flip flops'
        if paraula == 'sock':
            paraula = 'Socks'
            
        if any(paraula == shape for shape in classes):
            forma.append(paraula)
        if any(paraula == color for color in colors):
            colorp.append(paraula)

    if tipus != 'exit':

        if colorp and forma:
            tipus = 'combined'
        elif forma:
            tipus = 'shape'
        elif colorp:
            tipus = 'color'
        else:
            tipus = None

        pregunta = {
            'shape': forma,'color': colorp
        }

    return pregunta, tipus

#Anàlisi Quantitatiu
def get_shape_accuracy(class_labels, ground_truth):
    return round(np.mean(class_labels == ground_truth) * 100, 2)
    

def get_color_accuracy(color_labels, ground_truth):
    color_labels = np.asarray(color_labels)
    ground_truth = np.asarray(ground_truth)
    percentatge = 0

    for x, color_label in enumerate(color_labels):
        color_label = np.unique(color_label)
        accurate = [
            color_test == color_truth 
            for color_test, color_truth in zip(color_label, ground_truth[x])
        ]
        count_matches = accurate.count(True)
        
        longColor = len(color_label)
        longGround = len(ground_truth[x])
        percentatge = percentatge + count_matches / max((longColor), longGround)
    
    operacio = ((percentatge/color_labels.size)*100)    
    percentatge = round((operacio), 2)

    return percentatge


if __name__ == '__main__':

    #Load all the images and GT
    train_imgs, train_class_labels, train_color_labels, \
        test_imgs, test_class_labels, test_color_labels = read_dataset(gt_json='./images/gt.json')
    #List with all the existant classes
    classes = list(set(list(train_class_labels) + list(test_class_labels)))
    #Test colors
    n_test_colors = round(0.2 * test_imgs.shape[0])  
    color_labels = kmeans(test_imgs[:n_test_colors])
    #Train classes
    n_train_classes = round(0.20 * train_imgs.shape[0])  
    knn = KNN.KNN(train_imgs[:n_train_classes], train_class_labels[:n_train_classes])
    #Test classes
    n_test_classes = round(0.80 * test_imgs.shape[0])  #
    class_labels = knn.predict(test_imgs[:n_test_classes], 5)
    
    sortir = 0

    while sortir == 0:

        #escollir opció
        opcio = input('¿Que vols fer? \n  1. Buscar \n  2. Exactitud KNN \n  3. Exactitud K-Means \n  4. Salir \n')
        
        #per buscar colors i/o formes
        if opcio == '1':
            more_searches = True
            Nmax = 12

            while more_searches:
                pregunta_string = input('Forma/color: ')
                search_pregunta, search_type = parse_search_pregunta(pregunta_string, utils.colors, classes)  

                if search_type == "color":
                    results, llista = retrieval_by_color(test_imgs[:n_test_colors], color_labels, search_pregunta[search_type])

                    color_info = [
                        ', '.join(np.unique(color_labels[x])) + '\n Real: ' + ', '.join(test_color_labels[x])
                        for x in llista
                    ]
                    visualize_retrieval(results, Nmax, info=color_info, title='Pregunta: ' + pregunta_string)

                elif search_type == "shape":
                    results, llista = retrieval_by_shape(test_imgs[:n_test_classes], class_labels, search_pregunta[search_type])
                    
                    shape_info = [
                        test_class_labels[x]
                        for x in llista
                    ]
                    is_accurate = [
                        True if class_labels[x] == test_class_labels[x] else False
                        for x in llista
                    ]
                    visualize_retrieval(results, Nmax, info=shape_info[:Nmax], ok=is_accurate[:Nmax], title='Pregunta: ' + pregunta_string)

                elif search_type == "combined":
                    results, llista = retrieval_combined(test_imgs[:n_test_classes], color_labels, class_labels, search_pregunta)
                    shape_info = [
                        test_class_labels[x]
                        for x in llista
                    ]
                    is_accurate = [
                        True if class_labels[x] == test_class_labels[x] else False
                        for x in llista
                    ]
                    visualize_retrieval(results, Nmax, info=shape_info, ok=is_accurate, title='Pregunta: ' + pregunta_string)

                elif search_type == 'exit':
                    more_searches = False

                else:
                    print('Error: No vàlid. Escriu "quit" per finalitzar')
                    
        #et dona el percentatge de la forma               
        elif opcio == '2':
            percentatge = get_shape_accuracy(class_labels, test_class_labels[:n_test_classes])
            print(f'(KNN) Percentatge etiquetes correctes: {percentatge}%')
        #et dona el percentatge del color
        elif opcio == '3': 
            percentatge = get_color_accuracy(color_labels, test_color_labels[:n_test_colors])
            print(f'(K-Means) Percentatge etiquetes correctes: {percentatge}%')
        elif opcio == '4':
            sortir = 1
        else:
            print('Opció no es vàlida')








