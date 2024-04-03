import Agent
import math
import random
import ComputeHMap
import config

class Seeker(Agent.Agent):
    def __init__(self, view_range, pos):
        super().__init__(view_range, pos)

    def explore(self):
        print("Kill me")

    def move_wrapper(self, hmap, mapData):
        next_direction = self.find_path(hmap)
        self.move(mapData, next_direction)

    def find_path(self, hmap):
        minPath = math.inf
        dir = -1
        for i in range(0, 8):
            h_value = hmap[self.pos[0] + Agent.x_movement[i]][
                self.pos[1] + Agent.y_movement[i]
            ]
            if h_value != math.inf and minPath >= h_value:
                minPath = h_value
                dir = i
        return dir

    def find_pos_DFS(self, map_data):
        list_pos_dfs = []
        for i in range(0, len(map_data)):
            for j in range(0, len(map_data[0])):
                if map_data[i][j] == 5:
                    list_pos_dfs.append((i, j))
        return random.choice(list_pos_dfs)

    def find_pos_ping(self, pings: dict,map_data,viewable_map):
        first_key = next(iter(pings))
        first_value = pings[first_key]

        if len(first_value) == 0:
            return (0, 0)
        elif len(first_value) == 1:
            return first_value[0]
        else:
            a = PingPosHandle.final_destination(first_value,map_data,viewable_map)
            if not a:
                return 0,0
            # cho nay chua biet lam j nen cu lam v 
            return a[0]
    def process_pings(self,pings, hider_range, map_data, viewable_map):
        # kiem tra xem co bao nhieu key trong pings 
        #khoi tao hider_range`
       
        for key in pings:
            
            for value in pings[key]:
                hider_range[key][0] = max(0, value[0] - config.HIDER_PING_RANGE,hider_range[key][0])
                hider_range[key][1] = min(len(map_data), value[0] + config.HIDER_PING_RANGE + 1, hider_range[key][1])
                hider_range[key][2] = max(0, value[1] - config.HIDER_PING_RANGE, hider_range[key][2])
                hider_range[key][3] = min(len(map_data[0]), value[1] + config.HIDER_PING_RANGE + 1, hider_range[key][3])
        
        for key in pings:
            hmap=ComputeHMap.compute_h_map(map_data, self.pos)
            min_val_ping=math.inf
            min_cell_ping=(-1,-1)
            
            for i, value in enumerate(pings[key]):
                if(self.pos==value):
                    pings[key].remove(value)
                    i-=1
                    continue
                if hider_range[key][0]<=value[0] or hider_range[key][1]>=value[0] or hider_range[key][2]<=value[0] or hider_range[key][3]>=value[0]:
                    min_val = math.inf
                    min_cell =(-1,-1)
                    #  for x2 in range(min_i, max_i):
            #for y2 in range(min_j, max_j):
                    for x in range(hider_range[key][0], hider_range[key][1]):
                        for y in range(hider_range[key][2], hider_range[key][3]):
                            if hmap[x][y] < min_val and hmap[x][y]!=0:
                                min_val = hmap[x][y]
                                min_cell = (x,y)
                    if min_val != math.inf and min_cell not in pings[key]:
                        pings[key][i] = min_cell
                    
                        
                if hmap[value[0]][value[1]] < min_val_ping  and hmap[value[0]][value[1]]!= 0:
                    min_val_ping = hmap[value[0]][value[1]]
                    min_cell_ping = value
                
        return min_cell_ping
                
            
                   
            
            
                
              
