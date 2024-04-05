class GenericTent:

    def __init__(self, id, length=1, breadth=1):
        self.length = length
        self.breadth = breadth
        self.tent_type = self.__class__.__name__
        self.id = id

    def __str__(self):
        return str(self.id)

    def place_possible(self, x, y, map):
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


class LogisticsTent(BigTent):
    def __init__(self, id, length=4, breadth=4):
        super().__init__(id, length, breadth)


class CommunityTent(BigTent):
    def __init__(self, id, length=4, breadth=4):
        super().__init__(id, length, breadth)


class SentryTent(BigTent):
    def __init__(self, id, length=4, breadth=4, entrance_xy: list = None):
        super().__init__(id, length, breadth)
        if entrance_xy is None:
            entrance_xy = [20, 11]
        self.entrance_xy = entrance_xy
    def place_possible(self, x, y, map):
        if not super().place_possible(x ,y ,map):
            return False
        if x not in range(self.entrance_xy[0]-self.length, self.entrance_xy[0] + self.length) or y not in range(self.entrance_xy[1]-self.breadth, self.entrance_xy[1] +self.breadth):
            return False
        return True


class BigClusterTent(BigTent):
    def getCluster(self, map):
        return map.messCluster

    # def condition_sanity(self,tents_present: list):  ## Beside each other (vertically or horizontally) the idea is that if x or y is aligned then the other one will be diffed by length
    #     for tents in tents_present:
    #         if tents.__name__ == 'BigClusterTent':
    #             if tents.x == self.x:
    #                 if tents.y + self.breadth == self.y or tents.y - self.breadth == self.y:
    #                     return True
    #             if tents.y == self.y:
    #                 if tents.x + self.length == self.x or tents.x - self.length == self.x:
    #                     return True
    #     return False

    def add_to_cluster(self, x, y, map):
        self.getCluster(map).append([x, y])

    def remove_from_cluster(self, x, y, map):
        self.getCluster(map).pop()

    def place_possible(self, x, y, map):
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
    def getCluster(self, map):
        return map.messCluster


class MedicalTent(BigClusterTent):
    def __init__(self, id, length=2, breadth=4):
        super().__init__(id, length, breadth)

    def getCluster(self, map):
        return map.medicalCluster


class SpacedOutClusterTent(BigClusterTent):
    def __init__(self, id, length=4, breadth=4):
        super().__init__(id, length, breadth)
        self.spacing = 4
        self.cluster_tent_names = ["DeconTent"]

    def getCluster(self, map):
        return map.deconCluster

    def place_possible(self, x, y, map, ):
        if not super(SpacedOutClusterTent, self).place_possible(x, y, map):
            # print("1")
            return False
        ## Cleaniness 4-Metre Rule. Here we take 1 slot in the matrix = 1m^2 in real life
        x_topleft = max(0, x - self.spacing)
        y_topleft = max(0, y - self.spacing)
        x_btmright = min(x + 1 + self.length + self.spacing, map.length)
        y_btmright = min(y + 1 + self.breadth + self.spacing, map.breadth)
        for i in range(x_topleft, x_btmright):
            for j in range(y_topleft, y_btmright):
                # print(map.matrix[i][j], type(map.matrix[i][j]))
                if type(map.matrix[i][j]) == int:
                    if map.matrix[i][j] != 0:
                        # print("2")
                        return False
                    else:
                        continue
                else:

                    if map.matrix[i][j].tent_type not in self.cluster_tent_names:
                        # print("3")
                        return False
        return True


class DeconTent(SpacedOutClusterTent):
    def getCluster(self, map):
        return map.deconCluster

    def __init__(self, id, length=4, breadth=4):
        super().__init__(id, length, breadth)
        self.spacing = 4
        self.cluster_tent_names = ["DeconTent"]

    def place_possible(self, x, y, map):
        return super(DeconTent, self).place_possible(x, y, map)


class SpacedOutSmallClusterTent(SpacedOutClusterTent):
    def __init__(self, id, length=1, breadth=1):
        super().__init__(id, length, breadth)
        self.spacing = 2
        self.cluster_tent_names = ["K9Tent"]

    def getCluster(self, map):
        return map.restCluster


class K9Tent(SpacedOutSmallClusterTent):
    def place_possible(self, x, y, map):
        return super(K9Tent, self).place_possible(x, y, map)

    def getCluster(self, map):
        return map.K9Cluster


class RestTent(SmallClusterTent):
    def getCluster(self, map):
        return map.restCluster
