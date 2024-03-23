import Agent
class Seeker(Agent.Agent):
    def __init__(self, viewRange, pos):
        super().__init__(viewRange, pos)
        
    def explore(self):
        print("Kill me")
        
    def chase(self, hmap, mapData):
        next_direction = self.find_path(hmap)
        self.move(mapData, next_direction)