import Agent
import random
import math

class Hider(Agent.Agent):
    def __init__(self, view_range, pos: tuple, can_move: bool, id):
        super().__init__(view_range, pos)
        self.can_move = can_move
        self.id = id
        
    def move_wrapper(self, map, hmap):
        self.move(map, self.find_path(map, hmap))
    
    def ping(self, mapData, config):
        min_i = max(0, self.pos[0] - config["HIDER_PING_RANGE"])
        max_i = min(len(mapData) - 1, self.pos[0] + config["HIDER_PING_RANGE"])
        min_j = max(0, self.pos[1] - config["HIDER_PING_RANGE"])
        max_j = min(len(mapData[0]) - 1, self.pos[1] + config["HIDER_PING_RANGE"])

        while True:
            rand_i = random.randint(min_i, max_i)
            rand_j = random.randint(min_j, max_j)
            if mapData[rand_i][rand_j] != 1 and (rand_i, rand_j) != self.pos:
                return (rand_i, rand_j)
        
    def find_path(self, map, hmap):
        dir = -1
        maxPath = -1
        for i in range(9):
            new_x = self.pos[0] + Agent.x_movement[i]
            new_y = self.pos[1] + Agent.y_movement[i]
            # i = 8 is when the hider stands still (prepare to get caught)
            if new_x >= 0 and new_x < len(map) and new_y >= 0 and new_y < len(map[0]):
                if map[new_x][new_y] == 2 and i < 8:
                    continue
                h_value = hmap[new_x][new_y]
                if h_value != math.inf and maxPath < h_value:
                    maxPath = h_value
                    dir = i            
        return dir
