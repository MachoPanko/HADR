import copy
import math

import tents
from global_var import found_solution
import numpy as np
import inspect
import sys

# placing_order = ["SentryTent", "LogisticsTent", "MaintenanceTent", "POLTent", "EnsuiteDuoTent", "CleanTent", "UCCTent",  "CommunityTent", "MedicalTent", "MessTent", "RestTent", "K9Tent"]
class Map:
    def __init__(self, length, breadth, tentList , entrance_xy, xy_out_of_bounds , placing_order):
        self.entrance_xy = entrance_xy
        self.length = length
        self.breadth = breadth
        self.matrix = np.zeros((length,breadth)).astype(int).tolist()
        self.messCluster = []
        self.MainPOLCluster = []
        self.cleanCluster = []
        self.medicalCluster = []
        self.restCluster = []
        self.ensuiteCluster = []
        self.K9Cluster = []
        self.tentList = tentList
        self.uniqueTents = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules['tents']) if inspect.isclass(cls_obj)]
        self.tentDict = {}
        self.tentset = set()
        self.placing_order = placing_order
        for xy in xy_out_of_bounds:
            self.matrix[xy[0]][xy[1]] = -1
            # oob = tents.OutOfBoundsMarker()
            # oob.place(xy[0], xy[1], self.matrix)
        for tent_names in self.uniqueTents:
            self.tentDict[tent_names] = []
        for tent in self.tentList:
            self.tentDict[tent.__class__.__name__].append(tent)

    def printable(self):
        matrix = []
        for i in range(self.length):
            row = []
            for tent in self.matrix[i]:
                row.append(int(str(tent)))
            matrix.append(row)
        return matrix
    def next_map(self, tenttype):
        temp = copy.deepcopy(self)
        tent_to_remove = temp.tentDict[tenttype].pop(0)
        temp.tentList.remove(tent_to_remove)


        return temp

    def euclidean_dist( self, x_source , y_source):
        distance = (x_source-self.entrance_xy[0])**2 +(y_source-self.entrance_xy[1])**2
        return distance
    def clean_to_decon(self):
        min_distance = -1
        min_xy = None
        for xy in self.cleanCluster:
            distance = self.euclidean_dist(xy[0],xy[1])
            if min_distance == -1:
                min_distance = distance
                min_xy = xy
            else:
                if distance <= min_distance:
                    min_distance = distance
                    min_xy = xy

        return min_xy






    def CSP(self):
        # if found_solution: COMMENTED OUT TO GET ALL SOLUTIONS,
        #     return True
        if(len(self.tentList) == 0):
            ## Change Nearest Clean to Decon

            x,y = self.clean_to_decon()
            self.matrix[x][y].unplace(x,y,self.matrix)
            deconTent = tents.DeconTent(12, length=4, breadth=4)
            deconTent.place(x, y, self.matrix)
            for row in self.printable():
                print(row)

            print("Mess Cluster: ", self.messCluster)
            print("Decon Cluster: ", self.cleanCluster)
            print("Medical Cluster: ", self.medicalCluster)
            found_solution = True

            input("More Solutions?")
            return self

        for tenttype in self.placing_order :
            for i in range(self.length):
                for j in range(self.breadth):

                    if len(self.tentDict[tenttype]) != 0:
                        # print(tenttype, i, j)
                        # if(tenttype == "MedicalTent") and  i ==8 and j == 56:
                        #     print(self.medicalCluster)
                        #     input("")
                        # print(self.tentDict[tenttype][0].place_possible(i, j, self))
                        if self.tentDict[tenttype][0].place_possible(i, j, self):
                            # print("possible")
                            if issubclass( self.tentDict[tenttype][0].__class__, tents.BigClusterTent):

                                self.tentDict[tenttype][0].add_to_cluster(i, j, self)

                            # self.tentDict[tenttype][0].add_to_cluster(i, j, self)
                            self.tentDict[tenttype][0].place(i,j , self.matrix)
                            tempmap = self.next_map(tenttype)

                            for row in self.printable():
                                print(row)

                            print()

                            print(self.tentList)
                            found_solution = tempmap.CSP()
                            # Here is return once solution is found, should return a list of coords ah , as fabian requested
                            if found_solution :
                                return found_solution

                            ## if come out of this recursive call, set to 0 and remove from cluster
                            self.tentDict[tenttype][0].unplace(i,j , self.matrix)

                            if issubclass( self.tentDict[tenttype][0].__class__, tents.BigClusterTent):
                                self.tentDict[tenttype][0].remove_from_cluster(i,j,self)


        return False