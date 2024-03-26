import Agent
import random
import math

class Hider(Agent.Agent):
    def __init__(self, view_range, pos: tuple, can_move: bool):
        super().__init__(view_range, pos)
        self.can_move = can_move
        self.is_caught = False
        
    def move_wrapper(self, map, hmap, run_away: bool):
        self.move(map, self.find_path(hmap, run_away))
    
    def ping(self, mapData):
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(mapData), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(mapData[0]), self.pos[1] + self.viewRange + 1)

        while True:
            rand_i = random.randint(min_i, max_i)
            rand_j = random.randint(min_j, max_j)
            if mapData[rand_i][rand_j] != 1 and (rand_i, rand_j) != self.pos:
                return (rand_i, rand_j)
        
    def find_path(self, hmap, max = False):
        dir = -1
        if(not max):
            minPath = math.inf
            for i in range(8):
                h_value = hmap[self.pos[0] + Agent.x_movement[i]][self.pos[1] + Agent.y_movement[i]]
                if h_value != math.inf and minPath >= h_value:
                    minPath = h_value
                    dir = i
        else:
            maxPath = -1
            for i in range(8):
                h_value = hmap[self.pos[0] + Agent.x_movement[i]][self.pos[1] + Agent.y_movement[i]]
                if h_value != math.inf and maxPath < h_value:
                    maxPath = h_value
                    dir = i            
        return dir