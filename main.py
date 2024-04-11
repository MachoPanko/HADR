# This is a sample Python script.
import tents
import numpy as np
from global_var import found_solution
import maps


area_length = 7
area_width = 9
area_available = area_width * area_length
entrance_xy = [20,0]
tents_requested = [tents.SentryTent(15, entrance_xy=entrance_xy), tents.MessTent(1), tents.MessTent(1), tents.MessTent(1), tents.MedicalTent(3), tents.LogisticsTent(13), tents.CommunityTent(13), tents.MessTent(2), tents.MedicalTent(4) , tents.MessTent(1), tents.MedicalTent(3), tents.MessTent(2), tents.MedicalTent(4) , tents.RestTent(6), tents.RestTent(7), tents.RestTent(8), tents.RestTent(9), tents.RestTent(10), tents.K9Tent(5), tents.K9Tent(5), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12),tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12)]
xy_out_of_bounds = [[0,0], [0,1],[16,16],[23,23],[22,23], [21,23], [20,23], [18,23], [16,23]]
# xy_out_of_bounds =[]
if __name__ == '__main__':

    print("number of tents: " + str(len(tents_requested)))

    mapy = maps.Map(30, 30, tents_requested, entrance_xy, xy_out_of_bounds)

    print(mapy.CSP())







