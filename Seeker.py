import Agent
class Seeker(Agent.Agent):
    def __init__(self, view_range, pos):
        super().__init__(view_range, pos)
        
    def explore(self):
        print("Kill me")
    
    def move_wrapper(self, hmap, mapData):
        next_direction = self.find_path(hmap)
        self.move(mapData, next_direction)