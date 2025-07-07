__authors__ = 'Mateo Arteaga 1601190, Marc Benitez 1600946, Aaron Lozano 1636164'
__group__ = 'PRACT2_57'

import numpy as np
import math
import operator
from scipy.spatial.distance import cdist


class KNN:
    def __init__(self, train_data, labels):
        self._init_train(train_data)
        self.labels = np.array(labels)
        #############################################################
        ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
        #############################################################

    def _init_train(self, train_data):
        """
        initializes the train data
        :param train_data: PxMxNx3 matrix corresponding to P color images
        :return: assigns the train set to the matrix self.train_data shaped as PxD (P points in a D dimensional space)
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        aux = isinstance(train_data, float)

        if aux is False:
            self.train_data = train_data.astype(np.float)

        longitud = len(train_data)
        mida = np.size(self.train_data)
        divisio = np.divide(mida, longitud)

        self.train_data = np.reshape(self.train_data, (longitud, np.int64(divisio)))

    def get_k_neighbours(self, test_data, k):
        """
        given a test_data matrix calculates de k nearest neighbours at each point (row) of test_data on self.neighbors
        :param test_data: array that has to be shaped to a NxD matrix (N points in a D dimensional space)
        :param k: the number of neighbors to look at
        :return: the matrix self.neighbors is created (NxK)
                 the ij-th entry is the j-th nearest train point to the i-th test point
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        self.neighbors = np.random.randint(k, size=[test_data.shape[0], k])

        aux = isinstance(test_data, float)

        if aux is False:
            test_data = test_data.astype(np.float)
        else:
            print('data tipus float')

        longitud = len(test_data)
        test_data = np.reshape(test_data, (longitud, np.int64(np.divide(np.size(test_data), longitud))))
        distancia = cdist(test_data, self.train_data)
        self.neighbors = self.labels[np.argsort(distancia)[0:len(test_data), 0:k]]


    def get_class(self):
        """
        Get the class by maximum voting
        :return: 2 numpy array of Nx1 elements.
                1st array For each of the rows in self.neighbors gets the most voted value
                            (i.e. the class at which that row belongs)
                2nd array For each of the rows in self.neighbors gets the % of votes for the winning class
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        llista = []
        for x, y in enumerate(self.neighbors):
            if len(y) > 2:
                dicc = {}
                for z in y:
                    if z not in dicc:
                        dicc[z] = 1
                    else:
                        dicc[z] = dicc[z] + 1
                llista.append(max(dicc.items(), key=operator.itemgetter(1))[0])
            else:
                llista.append(y[0])

        return np.array(llista)



    def predict(self, test_data, k):
        """
        predicts the class at which each element in test_data belongs to
        :param test_data: array that has to be shaped to a NxD matrix (N points in a D dimensional space)
        :param k: the number of neighbors to look at
        :return: the output form get_class (2 Nx1 vector, 1st the class 2nd the  % of votes it got
        """

        self.get_k_neighbours(test_data, k)
        return self.get_class()
