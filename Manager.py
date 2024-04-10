import Hider
import Seeker
import ComputeHMap
import Obstacle

class Manager:
    def __init__(
        self,
        seeker: Seeker,
        hiders: list[Hider.Hider],
        map_data,
        obsts: list[Obstacle.Obstacle],
    ):
        self.seeker = seeker
        self.hiders = hiders
        self.pings = dict()
        self.obsts = obsts
        self.initialize_pings()

    def initialize_pings(self):
        for hider in self.hiders:
            self.pings[hider.id] = []

    def hiders_ping(self, map_data, config):
        for hider in self.hiders:
            self.pings[hider.id].append(hider.ping(map_data, config))
        return self.pings

    def move_hiders(self, map_data):
        for hider in self.hiders:
            viewable_map = hider.generate_viewable_map(map_data)
            seeker_pos = hider.scan_target(map_data, 3, viewable_map)
            if seeker_pos != (-1, -1):
                hmap = ComputeHMap.compute_h_map(map_data, self.seeker.pos)
                hider.move_wrapper(map_data, hmap)

    def check_hiders(self):
        for hider in self.hiders:
            if self.seeker.pos == hider.pos:
                del self.pings[hider.id]
                self.hiders.remove(hider)
                return True

    def delete_seen_pings(self, destination):
        if destination != (-1, -1):
            for hider in self.hiders:
                if hider.pos == destination:
                    self.pings[hider.id] = []
                    break

    def delete_seen_hider(self, seeker_pov, map_data, hider_range, cells_visited):
        min_i = max(0, self.seeker.pos[0] - self.seeker.viewRange)
        max_i = min(len(seeker_pov), self.seeker.pos[0] + self.seeker.viewRange + 1)
        min_j = max(0, self.seeker.pos[1] - self.seeker.viewRange)
        max_j = min(len(seeker_pov[0]), self.seeker.pos[1] + self.seeker.viewRange + 1)
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                if seeker_pov[i][j] and map_data[i][j] == 2:
                    for hider in self.hiders:
                        if hider.pos == (i, j):
                            self.pings[hider.id] = []
                            if len(hider_range) != 0:
                                hider_range[hider.id] = [
                                    max(0, hider.pos[0] - 1),
                                    min(len(map_data), hider.pos[0] + 1),
                                    max(0, hider.pos[1] - 1),
                                    min(len(map_data[0]), hider.pos[1] + 1),
                                ]
                                cells_visited[hider.id] = []

    def AgentInThisPos(self, pos, mapData, target):
        if mapData[pos[0]][pos[1]] == target:
            if target == 3:
                return self.seeker
            elif target == 2:
                for hider in self.hiders:
                    if hider.pos == mapData[pos[0]][pos[1]]:
                        return hider