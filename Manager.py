import config
import ComputeHMap

class Manager():
    # static variables
    # precomputed heuristic maps for every possible cell
    hmaps = dict()
    # precomputed seeker's pov maps for every possible cell
    seeker_povs = dict()
    # precomputed hiders' pov maps for every possible cell
    hider_povs = dict()
    def __init__(self, seeker, hiders, map_data):
        self.seeker = seeker
        self.hiders = hiders
        self.pings = []
        self.precompute_hmaps(map_data)
        self.precompute_viewable_maps(map_data, config.SEEKER_VIEW_RANGE)
        if config.HIDER_CAN_MOVE:
            self.precompute_viewable_maps(map_data, config.HIDER_VIEW_RANGE)
        
    def precompute_hmaps(self, map_data):
        for i in range(1, len(map_data) - 1):
            for j in range(1, len(map_data[0]) - 1):
                if map_data[i][j] == 1:
                    continue
                Manager.hmaps[(i, j)] = ComputeHMap.compute_h_map(map_data, (i, j))
    
    def precompute_viewable_maps(self, map_data, view_range):
        rows = len(map_data)
        cols = len(map_data[0]) if rows > 0 else 0  
        
        for q in range(1, len(map_data) - 1):
            for p in range(1, len(map_data[0]) - 1):
                
                min_i = max(0, q - view_range)
                max_i = min(len(map_data), q + view_range + 1)
                min_j = max(0, p - view_range)
                max_j = min(len(map_data[0]), p + view_range + 1)
                viewable_map = [[False] * cols for _ in range(rows)]
                
                for i in range(rows):
                    for j in range(cols):
                        if map_data[i][j] == 1:
                            viewable_map[i][j] = True
                            continue
                        
                        # raycasting
                        if min_i <= i < max_i and min_j <= j < max_j:
                            dx = i - q
                            dy = j - p
                            dist = max(abs(dx), abs(dy))
                            stepX = dx / dist if dist != 0 else 0
                            stepY = dy / dist if dist != 0 else 0
                            x = q
                            y = p
                            visible = True
                            for k in range(dist):
                                x += stepX
                                y += stepY
                                if not (0 <= round(x) < rows and 0 <= round(y) < cols):
                                    continue
                                if map_data[round(x)][round(y)] == 1:
                                    visible = False
                                    break

                            viewable_map[i][j] = visible
                
                if view_range == config.SEEKER_VIEW_RANGE:
                    Manager.seeker_povs[(q, p)] = viewable_map
                else:
                    Manager.hider_povs[(q, p)] = viewable_map