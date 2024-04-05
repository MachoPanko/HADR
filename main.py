# This is a sample Python script.
import tents
import numpy as np
from global_var import found_solution
import maps
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
area_length = 7
area_width = 9
area_available = area_width * area_length
tents_requested = [tents.SentryTent(15),tents.MessTent(1), tents.MessTent(1), tents.MessTent(1), tents.MedicalTent(3), tents.LogisticsTent(13), tents.CommunityTent(13), tents.MessTent(2), tents.MedicalTent(4) , tents.MessTent(1), tents.MedicalTent(3), tents.MessTent(2), tents.MedicalTent(4) , tents.RestTent(6), tents.RestTent(7), tents.RestTent(8), tents.RestTent(9), tents.RestTent(10), tents.K9Tent(5), tents.K9Tent(5), tents.DeconTent(12), tents.DeconTent(12)]




# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    mapy = maps.Map(20,20, tents_requested)

    print(mapy.CSP())







