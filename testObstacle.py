import ReadMap
import MyGUI
import pygame
import Manager
import config
import Seeker
import Hider
import ComputeHMap
import math
import Obstacle

map_data, obsts_list_raw = ReadMap.read_map("map.txt")
seeker = Seeker.Seeker(config.SEEKER_VIEW_RANGE, ReadMap.find_seeker(map_data))
hiders_pos = ReadMap.find_hiders(map_data)
hiders = []
obsts_list = []
id = 1
for pos in hiders_pos:
    hiders.append(Hider.Hider(config.HIDER_VIEW_RANGE, pos, config.HIDER_CAN_MOVE, id))
    id += 1

# cách gắn vật cản vào manager
for obst in obsts_list_raw:
    obsts_list.append(Obstacle.Obstacle(obst))

    
manager = Manager.Manager(seeker, hiders, map_data,obsts_list)

hider_last_seen_pos = (-1, -1)
destination = (-1, -1)
guessing_pos = (-1, -1)
hmap = []
turns = 1
seeker_turn = True
chasing = False
pings = manager.pings
hider_range = {}
cells_visited = {}
running = True




#test cơ bản thôi

seeker.want_connecting = True
for row in map_data:
    print(row)
for obst in manager.obsts:
    if obst.is_connect==False and obst.connecting(map_data,manager):
        seeker.myObst = obst
    print(obst)
    
print("Seeker dang dinh voi ",seeker.myObst)    




