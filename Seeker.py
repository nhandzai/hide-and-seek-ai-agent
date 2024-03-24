import Agent
class Seeker(Agent.Agent):
    def __init__(self, viewRange, pos, m, n):
        super().__init__(viewRange, pos)
        
    def explore(self, mapData, viewable_map, explored):
        m = len(mapData)
        n = len(mapData[0])
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                if explored[i][j] == False:
                    return (i, j)
        # we should never reach this
        return (-1, -1)
    
    def move_wrapper(self, hmap, mapData, target):
        next_direction = self.find_path(hmap)
        next_pos = (self.pos[0] + Agent.x_movement[next_direction], self.pos[1] + Agent.y_movement[next_direction])
        caught = (mapData[next_pos[0]][next_pos[1]] == target)
        self.move(mapData, next_direction)
        return caught
        
    def fill_explored(self, viewable_map, mapData):
        explored = []
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(mapData), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(mapData[0]), self.pos[1] + self.viewRange + 1)
        
        for i in range(len(mapData)):
            row = []
            for j in range(len(mapData[0])):
                if min_i <= i < max_i and min_j <= j < max_j and viewable_map[i][j] != 5 or mapData[i][j] == 1:
                    row.append(True)
                else:
                    row.append(False)
            explored.append(row)
            
        return explored
            
    def update_explored(self, viewable_map, explored):
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(viewable_map), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(viewable_map[0]), self.pos[1] + self.viewRange + 1)
        
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                if viewable_map[i][j] != 5:
                    explored[i][j] = True