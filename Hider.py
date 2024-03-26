import Agent
import random

class Hider(Agent.Agent):
    def __init__(self, view_range, pos: tuple, can_move: bool):
        super().__init__(view_range, pos)
        self.can_move = can_move
        self.is_caught = False
    
    def ping(self, mapData):
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(len(mapData), self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(len(mapData[0]), self.pos[1] + self.viewRange + 1)

        while True:
            x = random.randint(min_i, max_i - 1)
            y = random.randint(min_j, max_j - 1)
            if mapData[x][y] == 1:
                continue
            return (x, y)