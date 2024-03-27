import math
from collections import deque

def compute_h_map(mapData, destination):
    rows = len(mapData)
    cols = len(mapData[0]) if rows > 0 else 0  
    map = [[0] * cols for _ in range(rows)]
   
    queue = deque([destination])

    while queue:
        x, y = queue.popleft()
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) != destination:
             if mapData[new_x][new_y] != 1  :
                if map[x][y]+1 < map[new_x][new_y] or map[new_x][new_y] == 0:
                    map[new_x][new_y] = map[x][y] + 1
                    queue.append((new_x,new_y))
                    
             else:
                if mapData[new_x][new_y] == 1:
                    map[new_x][new_y] = math.inf
                else:
                    map[new_x][new_y] = math.inf
                   
    return map