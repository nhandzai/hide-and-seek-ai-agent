import Agent
import math

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
            h_value = hmap[self.pos[0] + Agent.x_movement[i]][self.pos[1] + Agent.y_movement[i]]
            if h_value != math.inf and minPath >= h_value:
                minPath = h_value
                dir = i
        return dir