# This is a sample Python script.
import tents
import numpy as np

import maps

area_length = 50
area_breadth = 32
area_given = area_length * area_breadth
estimated_minarea_required = 0
entrance_xy = [20, 0]
tents_requested = [tents.SentryTent(15, entrance_xy=entrance_xy), tents.MessTent(1), tents.MessTent(1),
                   tents.POLTent(16), tents.MaintenanceTent(17), tents.EnsuiteDuoTent(18), tents.EnsuiteDuoTent(18),
                   tents.EnsuiteDuoTent(18), tents.MessTent(1), tents.MedicalTent(3), tents.LogisticsTent(13),
                   tents.CommunityTent(13), tents.MessTent(2), tents.MedicalTent(4), tents.MessTent(1),
                   tents.MedicalTent(3), tents.MessTent(2), tents.MedicalTent(4), tents.RestTent(6), tents.RestTent(7),
                   tents.RestTent(8), tents.RestTent(9), tents.RestTent(10), tents.RestTent(6), tents.RestTent(7),
                   tents.RestTent(8), tents.RestTent(9), tents.RestTent(10), tents.K9Tent(5), tents.K9Tent(5),tents.K9Tent(5), tents.K9Tent(5),
                   tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12),
                   tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12),
                   tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12), tents.CleanTent(12)]
xy_out_of_bounds = [[0, 0], [0, 1], [16, 16], [23, 23], [22, 23], [21, 23], [20, 23], [18, 23], [16, 23]]

####
placing_order_init = ["SentryTent"]
tents_requested_init = []
for tent in tents_requested:
    if tent.__class__.__name__ in placing_order_init:
        tents_requested_init.append(tent)

####
####
placing_order_dirty = ["LogisticsTent", "MaintenanceTent", "POLTent", "EnsuiteDuoTent", "CleanTent"]
tents_requested_dirty = []
for tent in tents_requested:
    if tent.__class__.__name__ in placing_order_dirty:
        tents_requested_dirty.append(tent)

tents_area_dirty = 0
for tents in tents_requested_dirty:
    tents_area_dirty += tents.length * tents.breadth
####
####
placing_order_clean_operations = ["UCCTent", "MedicalTent"]
tents_requested_clean_operations = []
for tent in tents_requested:
    if tent.__class__.__name__ in placing_order_clean_operations:
        tents_requested_clean_operations.append(tent)

tents_area_clean_operations = 0
for tents in tents_requested_clean_operations:
    tents_area_clean_operations += tents.length * tents.breadth
####
####
placing_order_clean_admin = ["CommunityTent", "MessTent", "RestTent", "K9Tent"]
tents_requested_clean_admin = []
for tent in tents_requested:
    if tent.__class__.__name__ in placing_order_clean_admin:
        tents_requested_clean_admin.append(tent)

tents_area_clean_admin = 0
for tents in tents_requested_clean_admin:
    tents_area_clean_admin += tents.length * tents.breadth
####

tents_area_total = tents_area_clean_admin + tents_area_clean_operations + tents_area_dirty
tents_percentage_dirty = tents_area_dirty / tents_area_total
tents_percentage_clean_operations = tents_area_clean_operations / tents_area_total
tents_percentage_clean_admin = tents_area_clean_admin / tents_area_total

print(tents_percentage_clean_admin, tents_percentage_clean_operations, tents_percentage_dirty)
# placing_order = ["SentryTent", "LogisticsTent", "CommunityTent" , "MaintenanceTent", "POLTent", "UCCTent", "EnsuiteDuoTent", "MedicalTent", "MessTent", "RestTent", "K9Tent", "CleanTent"]
# xy_out_of_bounds =[]
ret_tent_list = []
ret_zones = []


if __name__ == '__main__':
    for tent in tents_requested:
        estimated_minarea_required += tent.length*tent.breadth
    if estimated_minarea_required < area_given:
        print("number of tents: " + str(len(tents_requested)))

        mapy_init = maps.Map(area_length, area_breadth, tents_requested_init, entrance_xy, xy_out_of_bounds,
                             placing_order=placing_order_init)
        mapy_init = mapy_init.CSP()
        ret_tent_list.extend(mapy_init.btm_left_xy)
        ret_zones.append(mapy_init.topleftbottomright)
        ####
        mapy_dirty = maps.Map(area_length, area_breadth, tents_requested_dirty, entrance_xy, xy_out_of_bounds,
                              placing_order=placing_order_dirty)
        mapy_dirty.matrix = mapy_init.matrix
        mapy_dirty = mapy_dirty.CSP()
        ret_tent_list.extend(mapy_dirty.btm_left_xy)
        ret_zones.append(mapy_dirty.topleftbottomright)
        ####
        mapy_clean_operations = maps.Map(area_length, area_breadth, tents_requested_clean_operations, entrance_xy,
                                         xy_out_of_bounds, placing_order=placing_order_clean_operations)
        mapy_clean_operations.matrix = mapy_dirty.matrix
        mapy_clean_operations = mapy_clean_operations.CSP()
        ret_tent_list.extend(mapy_clean_operations.btm_left_xy)
        ret_zones.append(mapy_clean_operations.topleftbottomright)
        ####
        mapy_clean_admin = maps.Map(area_length, area_breadth, tents_requested_clean_admin, entrance_xy, xy_out_of_bounds,
                                    placing_order=placing_order_clean_admin)

        mapy_clean_admin.matrix = mapy_clean_operations.matrix
        mapy_clean_admin = mapy_clean_admin.CSP()
        ret_tent_list.extend(mapy_clean_admin.btm_left_xy)
        ret_zones.append(mapy_clean_admin.topleftbottomright)
        ##
        ## TENT LIST AND COORDINATES
        print(ret_tent_list)
        ## ZONE XYXY from top left to bottom right
        print(ret_zones)
    else:
        print("Not enough space!")