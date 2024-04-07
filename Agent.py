import math
import ComputeHMap
import Obstacle

# the final movement is only used by hider
x_movement = [-1, -1, -1, 0, 0, 1, 1, 1, 0]
y_movement = [-1, 0, 1, -1, 1, -1, 0, 1, 0]

class Agent:
    
    def __init__(self, viewRange: int, pos: tuple):
        self.viewRange = viewRange
        self.pos = pos
        self.want_connecting = False
        
    def move(self, map, dir):
        if( dir >= 0):
            temp = map[self.pos[0]][self.pos[1]]
            map[self.pos[0]][self.pos[1]] = 0
            self.pos = (self.pos[0] + x_movement[dir], self.pos[1] + y_movement[dir])
            map[self.pos[0]][self.pos[1]] = temp
            
    def generate_viewable_map(self, map_data):
        rows = len(map_data)
        cols = len(map_data[0])
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(map_data), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(map_data[0]), self.pos[1] + self.viewRange + 1)
        viewable_map = [[False] * cols for _ in range(rows)]
        
        for x2 in range(min_i, max_i):
            for y2 in range(min_j, max_j):
                if map_data[x2][y2] == 1:
                    viewable_map[x2][y2] = True
                    continue
                
                # raycasting
                x = self.pos[0]
                y = self.pos[1]
                
                dx = abs(x2 - x)
                dy = abs(y2 - y)
            
                n = 1 + dx + dy
                
                stepX = 1 if (x2 > x) else -1
                stepY = 1 if (y2 > y) else -1
                
                error = dx - dy
                
                dx *= 2
                dy *= 2
                
                visible = True
                
                while n > 0:
                    if map_data[x][y] == 1:
                        visible = False
                        break
                    
                    if (error > 0):
                        x += stepX
                        error -= dy
                        
                    elif (error < 0):
                        y += stepY
                        error += dx
                        
                    elif (error == 0):
                        x += stepX
                        y += stepY
                        error -= dy
                        error += dx
                        n -= 1
                    n -= 1
                    
                viewable_map[x2][y2] = visible
        
        return viewable_map
    
    def scan_target(self, map_data, target, viewable_map):
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(map_data), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(map_data[0]), self.pos[1] + self.viewRange + 1)
        
        # get pov at this position
        if target == 2:
            list_agent: list[tuple[int, int]] = []
            for i in range(min_i, max_i):
                for j in range(min_j, max_j):
                    if viewable_map[i][j] and map_data[i][j] == target:
                        list_agent.append((i, j))
            
            min_dis:int = math.inf
            min_pos = (-1, -1)
            for pos in list_agent:
                distance = ComputeHMap.compute_h_map(map_data, pos)
                x: int = distance[self.pos[0]][self.pos[1]]
               
                if x < min_dis:
                    min_dis = x
                    min_pos = pos
            return min_pos
        else:
            for i in range(min_i, max_i):
                for j in range(min_j, max_j):
                    if viewable_map[i][j] and map_data[i][j] == target:
                        return (i, j)
                
        return (-1, -1)