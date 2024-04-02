import maps


class GenericTent:

    def __init__(self, id, length=1, breadth=1):
        self.length = length
        self.breadth = breadth
        self.tent_type = self.__class__.__name__
        self.id = id

    def __str__(self):
        return str(self.id)

    def place_possible(self, x, y, map: maps.Map):
        ## too big for the matrix
        if x + self.length > map.length or y + self.breadth > map.breadth:
            return False
        ## too big for given space
        for i in range(self.length):
            for j in range(self.breadth):
                if map.matrix[x + i][y + j] != 0:  ## True equates to square already occupied
                    return False
        return True

    def place(self, x, y, matrix):
        for i in range(self.length):
            for j in range(self.breadth):
                placeholder = f"{self.tent_type} {self.id}"
                # matrix[x+i][y+j] = placeholder.ljust(12)
                matrix[x + i][y + j] = self

    def unplace(self, x, y, matrix):
        for i in range(self.length):
            for j in range(self.breadth):
                matrix[x + i][y + j] = 0


class BigTent(GenericTent):
    def __init__(self, id, length=4, breadth=4):
        super().__init__(id, length, breadth)


class BigClusterTent(BigTent):
    def getCluster(self, map: maps.Map):
        return map.messCluster

    def condition_sanity(self,
                         tents_present: list):  ## Beside each other (vertically or horizontally) the idea is that if x or y is aligned then the other one will be diffed by length
        for tents in tents_present:
            if tents.__name__ == 'BigClusterTent':
                if tents.x == self.x:
                    if tents.y + self.breadth == self.y or tents.y - self.breadth == self.y:
                        return True
                if tents.y == self.y:
                    if tents.x + self.length == self.x or tents.x - self.length == self.x:
                        return True
        return False

    def add_to_cluster(self, x, y, map: maps.Map):
        self.getCluster(map).append([x, y])

    def remove_from_cluster(self, x, y, map: maps.Map):
        self.getCluster(map).pop()

    def place_possible(self, x, y, map: maps.Map):
        if not super().place_possible(x, y, map):
            return False
        if len(self.getCluster(map)) == 0:

            return True
        else:
            for tent in self.getCluster(map):
                if tent[0] == x:
                    if tent[1] + self.breadth == y or tent[1] - self.breadth == y:
                        return True
                if tent[1] == y:
                    if tent[0] + self.length == x or tent[0] - self.length == x:
                        return True

            return False


class SmallClusterTent(BigClusterTent):
    def __init__(self, id, length=1, breadth=1):
        super().__init__(id, length, breadth)

class MessTent(BigClusterTent):
    def getCluster(self, map: maps.Map):
        return map.messCluster


class DeconTent(BigClusterTent):
    def getCluster(self, map: maps.Map):
        return map.deconCluster



class SpacedOutClusterTent(BigClusterTent):
    def __init__(self, id, length = 4  , breadth = 4):
        super().__init__(id , length, breadth)
        self.spacing = 4
        self.cluster_tent_names = ["MedicalTent" ]

    def getCluster(self, map: maps.Map):
        return map.medicalCluster
    def place_possible(self, x, y,  map: maps.Map, ):
        if not super(SpacedOutClusterTent, self).place_possible(x, y, map):
            return False
        ## Cleaniness 4-Metre Rule. Here we take 1 slot in the matrix = 1m^2 in real life
        x_topleft = max(0, x - self.spacing)
        y_topleft = max(0, y - self.spacing)
        x_btmright = min(x+1+self.length+self.spacing, map.length)
        y_btmright = min(y+1+self.breadth+self.spacing, map.breadth)
        for i in range (x_topleft, x_btmright):
            for j in range(y_topleft, y_btmright):
                if type(map.matrix[i][j]) == int:
                    if map.matrix[i][j] != 0:
                        return False
                    else:
                        continue
                else:

                    if map.matrix[i][j].tent_type not in self.cluster_tent_names:
                        return False
        return True

class MedicalTent(SpacedOutClusterTent):

    def place_possible(self, x, y, map: maps.Map):
        return super(MedicalTent, self).place_possible(x,y,map)


class SpacedOutSmallClusterTent(SpacedOutClusterTent):
    def __init__(self, id, length=1, breadth=1):
        super().__init__(id, length, breadth)
        self.spacing = 2
        self.cluster_tent_names = ["K9Tent", "RestTent"]

    def getCluster(self, map: maps.Map):
        return map.restCluster

class K9Tent(SpacedOutSmallClusterTent):
    def place_possible(self, x, y,  map: maps.Map):

        return super(K9Tent, self).place_possible(x,y,map)
    def getCluster(self, map: maps.Map):
        return map.restCluster

class RestTent(SmallClusterTent):
    def getCluster(self, map: maps.Map):
        return map.restCluster
