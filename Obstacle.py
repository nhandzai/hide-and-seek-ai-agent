import Agent
import Manager


class Obstacle:
    def __init__(self, obst_raw):
        self.topLeft = (obst_raw[0], obst_raw[1])
        self.height = obst_raw[2] - obst_raw[0] + 1
        self.width = obst_raw[3] - obst_raw[1] + 1
        self.is_connect = False
        self.pos_mover = (0, 0)

    def connecting(self, mapData, manager):
        min_i = max(0, self.topLeft[0] - 1)
        max_i = min(len(mapData), self.topLeft[0] + self.height + 1)
        min_j = max(0, self.topLeft[1] - 1)
        max_j = min(len(mapData[0]), self.topLeft[1] + self.width + 1)

        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                if mapData[i][j] in [3, 2]:
                    if self.isWantConnect(
                        manager.AgentInThisPos((i, j), mapData, mapData[i][j])
                    ):
                        self.is_connect = True
                        self.pos_mover = (i, j)
                        return True
        return False

    def isWantConnect(self, agent):
        return agent.want_connecting

    def __str__(self):
        return f"Obstacle: topLeft={self.topLeft}, height={self.height}, width={self.width}, is_connect={self.is_connect}, pos_mover={self.pos_mover}"
