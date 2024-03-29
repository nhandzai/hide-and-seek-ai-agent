import Hider
import Seeker
import ComputeHMap

class Manager():
    def __init__(self, seeker: Seeker, hiders: list[Hider.Hider], map_data):
        self.seeker = seeker
        self.hiders = hiders
        self.pings = dict()
        self.initialize_pings()
        
    def initialize_pings(self):
        for hider in self.hiders:
            self.pings[hider.id] = []
                    
    def hiders_ping(self, map_data):
        for hider in self.hiders:
            self.pings[hider.id].append(hider.ping(map_data))
        return self.pings           

    def move_hiders(self, map_data):
        for hider in self.hiders:
            viewable_map = hider.generate_viewable_map(map_data)
            seeker_pos = hider.scan_target(map_data, 3, viewable_map)
            if (seeker_pos != (-1, -1)):
                hmap = ComputeHMap.compute_h_map(map_data, self.seeker.pos)
                hider.move_wrapper(map_data, hmap)

    def check_hiders(self):
        for hider in self.hiders:
            if (self.seeker.pos == hider.pos):
               self.hiders.remove(hider)
