import copy

import tents
from global_var import found_solution
import numpy as np
import inspect
import sys

placing_order = [ "SentryTent", "LogisticsTent","CommunityTent" ,"MedicalTent","MessTent", "RestTent", "K9Tent", "DeconTent"]

class Map:
    def __init__(self, length, breadth, tentList):
        self.length = length
        self.breadth = breadth
        self.matrix = np.zeros((length,breadth)).astype(int).tolist()
        self.messCluster = []
        self.deconCluster = []
        self.medicalCluster = []
        self.restCluster = []
        self.K9Cluster = []
        self.tentList = tentList
        self.uniqueTents = [cls_name for cls_name, cls_obj in inspect.getmembers(sys.modules['tents']) if inspect.isclass(cls_obj)]
        self.tentDict = {}
        self.tentset = set()
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




    def CSP(self):
        global found_solution
        # if found_solution: COMMENTED OUT TO GET ALL SOLUTIONS,
        #     return True
        if(len(self.tentList) == 0):
            for row in self.printable():
                print(row)

            print("Mess Cluster: ", self.messCluster)
            print("Decon Cluster: ", self.deconCluster)
            print("Medical Cluster: ", self.medicalCluster)
            found_solution = True

            input("More Solutions?")
            return True

        for tenttype in placing_order :
            for j in range(self.breadth):
                for i in range(self.length):

                    if len(self.tentDict[tenttype]) != 0:

                        if self.tentDict[tenttype][0].place_possible(i, j, self):
                            if issubclass( self.tentDict[tenttype][0].__class__, tents.BigClusterTent):

                                self.tentDict[tenttype][0].add_to_cluster(i, j, self)

                            # self.tentDict[tenttype][0].add_to_cluster(i, j, self)
                            self.tentDict[tenttype][0].place(i,j , self.matrix)
                            tempmap = self.next_map(tenttype)

                            for row in self.printable():
                                print(row)

                            print()
                            tempmap.CSP()

                            ## if come out of this recursive call, set to 0 and remove from cluster
                            self.tentDict[tenttype][0].unplace(i,j , self.matrix)

                            if issubclass( self.tentDict[tenttype][0].__class__, tents.BigClusterTent):
                                self.tentDict[tenttype][0].remove_from_cluster(i,j,self)


