import Agent
import math
import random
import ComputeHMap
import config
import copy
class Seeker(Agent.Agent):
    def __init__(self, view_range, pos):
        super().__init__(view_range, pos)

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

    def process_pings(self,pings, hider_range, map_data, cells_visited):
        # kiem tra xem co bao nhieu key trong pings 
        #khoi tao hider_range`
       
        for key in pings:
            for value in pings[key]:
                hider_range[key][0] = max(0, value[0] - config.HIDER_PING_RANGE,hider_range[key][0])
                hider_range[key][1] = min(len(map_data), value[0] + config.HIDER_PING_RANGE + 1, hider_range[key][1])
                hider_range[key][2] = max(0, value[1] - config.HIDER_PING_RANGE, hider_range[key][2])
                hider_range[key][3] = min(len(map_data[0]), value[1] + config.HIDER_PING_RANGE + 1, hider_range[key][3])
        min_key = -1
        min_val_ping=math.inf
        min_cell_ping=(-1,-1)
        cop_pings=copy.deepcopy(pings)
        hmap=ComputeHMap.compute_h_map(map_data, self.pos)
        for key in cop_pings:
            for i, value in enumerate(cop_pings[key]):
                if(self.pos==value):
                    if hider_range[key][0]<=value[0] and hider_range[key][1]>=value[0] or hider_range[key][2]<=value[1] or hider_range[key][3]>=value[1]:
                        if(value not in cells_visited[key]): 
                            cells_visited[key].append(value)
                    cop_pings[key].remove(value)
                    pings[key].remove(value)
                    i-=1
                    continue
          
                if hider_range[key][0]>value[0] or hider_range[key][1]<value[0] or hider_range[key][2]>value[1] or hider_range[key][3]<value[1]:
                    min_val = math.inf
                    min_cell =(-1,-1)
                    #  for x2 in range(min_i, max_i):
            #for y2 in range(min_j, max_j):
                    for x in range(hider_range[key][0], hider_range[key][1]):
                        for y in range(hider_range[key][2], hider_range[key][3]):
                            if hmap[x][y] < min_val and hmap[x][y]!=0 and (x,y) not in cells_visited[key]:
                                min_val = hmap[x][y]
                                min_cell = (x,y)
                    if min_val != math.inf :
                        cop_pings[key][i] = min_cell
                        value=min_cell
                else:
                    if (value[0],value[1]) in cells_visited[key]:
                        min_val = math.inf
                        min_cell =(-1,-1)
                        for x in range(hider_range[key][0], hider_range[key][1]):
                            for y in range(hider_range[key][2], hider_range[key][3]):
                                if hmap[x][y] < min_val and hmap[x][y]!=0 and (x,y) not in cells_visited[key]:
                                    min_val = hmap[x][y]
                                    min_cell = (x,y)
                        if min_val != math.inf :
                            cop_pings[key][i] = min_cell
                            value=min_cell
                        
                        
                if hmap[value[0]][value[1]] < min_val_ping  and hmap[value[0]][value[1]]!= 0  :
                    min_val_ping = hmap[value[0]][value[1]]
                    min_cell_ping = value
                    min_key = key
      #neu turn tiep theo den diem nay   
        if(min_val_ping==1):
            cells_visited[min_key].append(value)
        return min_cell_ping