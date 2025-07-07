__authors__ = 'Mateo Arteaga 1601190, Marc Benitez 1600946, Aaron Lozano 1636164'
__group__ = 'PRACT2_57'

import numpy as np
import utils
import math
import copy

from itertools import combinations


class KMeans:

    def __init__(self, X, K=1, options=None):
        """
         Constructor of KMeans class
             Args:
                 K (int): Number of cluster
                 options (dict): dictionary with options
            """
        self.num_iter = 0
        self.K = K
        self._init_X(X)
        self._init_options(options)  # DICT options

        self.h = X.shape[0]
        self.w = X.shape[1]
        self.ratio = self.w / self.h

    #############################################################
    ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
    #############################################################

    def _init_X(self, X):
        """Initialization of all pixels, sets X as an array of data in vector form (PxD)
            Args:
                X (list or np.array): list(matrix) of all pixel values
                    if matrix has more than 2 dimensions, the dimensionality of the sample space is the length of
                    the last dimension
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        #self.X = np.random.rand(100, 5)

        X = X * 1.0
        if X.ndim == 2:
            self.X = X
        elif X.ndim > 2:
            self.X = np.reshape(X, (-1, X.shape[-1]))

    def _init_options(self, options=None):
        """
        Initialization of options in case some fields are left undefined
        Args:
            options (dict): dictionary with options
        """
        if options is None:
            options = {}
        if 'km_init' not in options:
            options['km_init'] = 'first'
        if 'verbose' not in options:
            options['verbose'] = False
        if 'tolerance' not in options:
            options['tolerance'] = 0
        if 'max_iter' not in options:
            options['max_iter'] = np.inf
        if 'fitting' not in options:
            options['fitting'] = 'WCD'  # within class distance.

        # If your methods need any other parameter you can add it to the options dictionary
        self.options = options

        #############################################################
        ##  THIS FUNCTION CAN BE MODIFIED FROM THIS POINT, if needed
        #############################################################

    def inList(self, array, list):  # funcio afegida per comprovar si esta o no a la llista
        for element in list:
            if np.array_equal(element, array):
                return True
        return False

    def _init_centroids(self):
        """
        Initialization of centroids
        """

        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        lista = [self.X[0]]
        i = x = 0

        if self.options['km_init'].lower() == 'first':

            while i < self.K - 1:
                if not self.inList(self.X[x], lista):
                    lista.append(self.X[x])
                    i += 1
                x += 1

            self.centroids = np.array(lista)
            self.old_centroids = np.array(lista)

        elif self.options['km_init'].lower() == 'random':

            for i in range(len(self.K)):
                self.centroids = np.random.rand(self.K, self.X.shape[1])
                self.old_centroids = np.random.rand(self.K, self.X.shape[1])

        elif self.options['km_init'].lower() == 'custom':
            j = 0
            k = 0.0

            while i < self.K - 1:
                k = j * self.ratio
                if not self.inList(self.X[self.w * j + round(k)], lista):
                    lista.append(self.X[self.h * j + int(k)])
                    i += 1
                j += 1

            self.centroids = np.array(lista)
            self.old_centroids = np.array(lista)


    def get_labels(self):
        """        Calculates the closest centroid of all points in X
        and assigns each point to the closest centroid
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################
        self.labels = np.argmin(distance(self.X, self.centroids), axis=1)

    def centeroidnp(self, arr):

        length = arr.shape[0]
        x = np.sum(arr[:, 0])
        y = np.sum(arr[:, 1])
        z = np.sum(arr[:, 2])

        return x / length, y / length, z / length

    def get_centroids(self):
        """
        Calculates coordinates of centroids based on the coordinates of all the points assigned to the centroid
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        self.old_centroids = self.centroids
        self.get_labels()
        list = np.empty([self.K, 3])

        for k in range(self.K):
            list[k] = self.centeroidnp(np.array(self.X[np.where(self.labels == k)]))
        self.centroids = list


    def converges(self):
        """
        Checks if there is a difference between current and old centroids
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        return np.allclose(self.centroids, self.old_centroids, atol=self.options['tolerance'])

    def fit(self):
        """
        Runs K-Means algorithm until it converges or until the number
        of iterations is smaller than the maximum number of iterations.
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        i = 0
        self._init_centroids()

        while True:
            self.get_centroids()
            if self.options['max_iter'] == i or self.converges():
                break
            i += 1


    def withinClassDistance(self):
        """
         returns the within class distance of the current clustering
        """

        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        sum = 0

        for x in range(len(self.centroids)):
            sum += np.sum((np.square(self.X[np.where(self.labels == x)] - self.centroids[x])) ** 2)


        return sum * self.K

    def InterClassDistance(self):

        comb = list(combinations([i for i in range(self.K)], 2))
        vec = self.centroids
        ICD = 0
        for i in range(len(comb)):
            ICD += np.sum(np.square(vec[comb[i][0]] - vec[comb[i][1]]) ** 2)

        return ICD / self.K

    def find_bestK(self, max_K):
        """
         sets the best k anlysing the results up to 'max_K' clusters
        """
        #######################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #######################################################

        first = True
        aux = 0

        for i in range(2, max_K):

            if not first:
                last = aux
            self.K = i
            self.fit()
            inter = self.InterClassDistance()
            intra = self.withinClassDistance()
            aux = intra / inter

            if not first:
                if 100 - 100 * (aux / last) < 60:
                    self.K = i - 1
                    self.fit()
                    break

            first = False




def get_colors(centroids):
    """
    for each row of the numpy matrix 'centroids' returns the color label following the 11 basic colors as a LIST
    Args:
        centroids (numpy array): KxD 1st set of data points (usually centroid points)

    Returns:
        labels: list of K labels corresponding to one of the 11 basic colors
    """

        #########################################################
        ##  YOU MUST REMOVE THE REST OF THE CODE OF THIS FUNCTION
        ##  AND CHANGE FOR YOUR OWN CODE
        #########################################################

    prob_colors = utils.get_color_prob(centroids)
    colors = np.array(
        ['Red', 'Orange', 'Brown', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Black', 'Grey', 'White'])
    list = []

    for a in range(len(centroids)):
        prob = 0
        iter = 0
        for i in range(len(prob_colors[a])):
            if prob < prob_colors[a][i]:
                prob = prob_colors[a][i]
                iter = i
        list.append(colors[iter])

    return list

def distance(X, C):
    """
        Calculates the distance between each pixel and each centroid
        Args:
            X (numpy array): PxD 1st set of data points (usually data points)
            C (numpy array): KxD 2nd set of data points (usually cluster centroids points)

        Returns:
            dist: PxK numpy array position ij is the distance between the
            i-th point of the first set an the j-th point of the second set
        """
    return np.linalg.norm(np.expand_dims(X, 2) - np.expand_dims(C.T, 0), axis=1)
