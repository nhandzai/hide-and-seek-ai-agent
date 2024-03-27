import math
import Manager

x_movement = [-1, -1, -1, 0, 0, 1, 1, 1]
y_movement = [-1, 0, 1, -1, 1, -1, 0, 1]

class Agent:
    def __init__(self, viewRange: int, pos: tuple):
        self.viewRange = viewRange
        self.pos = pos
        
    def move(self, map, dir):
        if( dir >= 0):
            temp = map[self.pos[0]][self.pos[1]]
            map[self.pos[0]][self.pos[1]] = 0
            self.pos = (self.pos[0] + x_movement[dir], self.pos[1] + y_movement[dir])
            map[self.pos[0]][self.pos[1]] = temp
    
    def scan_target(self, map_data, target):
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(map_data), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(map_data[0]), self.pos[1] + self.viewRange + 1)
        
        # get pov at this position
        if target == 2:
            viewable_map = Manager.Manager.seeker_povs[(self.pos[0], self.pos[1])]
        else:
            viewable_map = Manager.Manager.hider_povs[(self.pos[0], self.pos[1])]
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                if viewable_map[i][j] and map_data[i][j] == target:
                    return (i, j)
                
        return (-1, -1)
