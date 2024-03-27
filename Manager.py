import config
import ComputeHMap
import Hider
import Seeker
class Manager():
    # static variables
    # precomputed heuristic maps for every possible cell
    hmaps = dict()
    # precomputed seeker's pov maps for every possible cell
    seeker_povs = dict()
    # precomputed hiders' pov maps for every possible cell
    hider_povs = dict()
    def __init__(self, seeker: Seeker, hiders: list[Hider.Hider], map_data):
        self.seeker = seeker
        self.hiders = hiders
        self.pings = dict()
        self.precompute_hmaps(map_data)
        self.precompute_viewable_maps(map_data, config.SEEKER_VIEW_RANGE)
        if config.HIDER_CAN_MOVE:
            self.precompute_viewable_maps(map_data, config.HIDER_VIEW_RANGE)
        self.initialize_pings()
        
    def initialize_pings(self):
        for hider in self.hiders:
            self.pings[hider.id] = []
        
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
                
                for i in range(min_i, max_i):
                    for j in range(min_j, max_j):
                        if map_data[i][j] == 1:
                            viewable_map[i][j] = True
                            continue
                        
                        # raycasting
                        dx = abs(i - q)
                        dy = abs(j - p)
                        
                        x = q
                        y = p
                        
                        n = 1 + dx + dy
                        
                        stepX = 1 if (i > q) else -1
                        stepY = 1 if (j > p) else -1
                        
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
                            
                        viewable_map[i][j] = visible

                if view_range == config.SEEKER_VIEW_RANGE:
                    Manager.seeker_povs[(q, p)] = viewable_map
                else:
                    Manager.hider_povs[(q, p)] = viewable_map
                    
    def hiders_ping(self, map_data):
        for hider in self.hiders:
            self.pings[hider.id].append(hider.ping(map_data))
        return self.pings           

    def move_hiders(self, map_data):
        for hider in self.hiders:
            seeker_pos = hider.scan_target(map_data, 3)
            if (seeker_pos != (-1, -1)):
                hider.move_wrapper(map_data, self.hmaps[self.seeker.pos], True)
            #hider moves away from the last ping of it when the seeker is not in sight
            elif (self.pings[hider.id] != []):
                hider.move_wrapper(map_data, self.hmaps[self.pings[hider.id][len(self.pings[hider.id]) - 1]], True)

    def check_hiders(self):
        for hider in self.hiders:
            if (self.seeker.pos == hider.pos):
               self.hiders.remove(hider)
