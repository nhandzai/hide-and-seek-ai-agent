import Agent
import math
import random
import PingPosHandle


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
