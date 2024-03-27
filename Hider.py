import Agent
import random
import math
import config

class Hider(Agent.Agent):
    def __init__(self, view_range, pos: tuple, can_move: bool):
        super().__init__(view_range, pos)
        self.can_move = can_move
        self.is_caught = False
        
    def move_wrapper(self, map, hmap, run_away: bool, ban_list: list = None):
        self.move(map, self.find_path(ban_list, hmap, run_away))
    
    def ping(self, mapData):
        min_i = max(0, self.pos[0] - config.HIDER_PING_RANGE)
        max_i = min(len(mapData) - 1, self.pos[0] + config.HIDER_PING_RANGE)
        min_j = max(0, self.pos[1] - config.HIDER_PING_RANGE)
        max_j = min(len(mapData[0]) - 1, self.pos[1] + config.HIDER_PING_RANGE)

        while True:
            rand_i = random.randint(min_i, max_i)
            rand_j = random.randint(min_j, max_j)
            if mapData[rand_i][rand_j] != 1 and (rand_i, rand_j) != self.pos:
                return (rand_i, rand_j)
        
    def find_path(self, ban_list: list, hmap, max = False):
        dir = -1
        if(not max):
            minPath = math.inf
            for i in range(8):
                h_value = hmap[self.pos[0] + Agent.x_movement[i]][self.pos[1] + Agent.y_movement[i]]
                if h_value != math.inf and minPath >= h_value:
                    minPath = h_value
                    dir = i
        else:
            maxPath = hmap[self.pos[0]][self.pos[1]]
            for i in range(8):
                new_x = self.pos[0] + Agent.x_movement[i]
                new_y = self.pos[1] + Agent.y_movement[i]
                h_value = hmap[new_x][new_y]
                if h_value != math.inf and maxPath < h_value:
                    maxPath = h_value
                    dir = i            
        return dir
    
