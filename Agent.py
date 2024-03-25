import math
from ordered_set import OrderedSet # pip install ordered-set

x_movement = [-1, -1, -1, 0, 0, 1, 1, 1]
y_movement = [-1, 0, 1, -1, 1, -1, 0, 1]

class Agent:
    def __init__(self, viewRange: int, pos: tuple):
        self.viewRange = viewRange
        self.pos = pos
        
    def move(self, map, dir):
        temp = map[self.pos[0]][self.pos[1]]
        map[self.pos[0]][self.pos[1]] = 0
        self.pos = (self.pos[0] + x_movement[dir], self.pos[1] + y_movement[dir])
        map[self.pos[0]][self.pos[1]] = temp
        
    def generate_viewable_map(self, mapData):
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(mapData), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(mapData[0]), self.pos[1] + self.viewRange + 1)
        viewable_map = []
        for i in range(len(mapData)):
            row = []
            for j in range(len(mapData[0])):
                if min_i <= i < max_i and min_j <= j < max_j:
                    row.append(mapData[i][j])
                elif mapData[i][j] == 1:
                    row.append(1)
                else:
                    row.append(5)
            viewable_map.append(row)
        return viewable_map
    
    # this hasn't considered obstacles yet    
    def scan_target(self, mapData, target) -> OrderedSet:
        targets = OrderedSet()
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(mapData), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(mapData[0]), self.pos[1] + self.viewRange + 1)
        
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                if mapData[i][j] == target:
                    targets.add((i, j))
                
        return targets
    
    def find_path(self, hmap):
        minPath = math.inf
        dir = -1
        for i in range(0, 8):
            h_value = hmap[self.pos[0] + x_movement[i]][self.pos[1] + y_movement[i]]
            if h_value != math.inf and minPath >= h_value:
                minPath = h_value
                dir = i
        return dir
