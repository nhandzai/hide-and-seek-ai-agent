from movement_agent import Movement


class Agent(Movement):
    viewRange = 5
    role = 0
    mapSize = 0
    mapData = []
    viewableMap = []
    pos = (0, 0)
    opponentPos = 0

    def __init__(self, role, mapSize, mapData):
        self.role = role
        if role == 3:
            self.viewRange = 5
        else:
            self.viewRange = 2
        self.mapSize = mapSize
        self.mapData = mapData
        self.find_positions()
        self.generate_viewable_map()
        self.find_hider()
    def updateMapdata(self,mapData):
        self.mapData = mapData
    
    def find_positions(self):
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                if self.mapData[i][j] == self.role:
                    self.pos = (i, j)

    def generate_viewable_map(self):
        self.viewableMap = []
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(self.mapSize, self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(self.mapSize, self.pos[1] + self.viewRange + 1)
        
        for i in range(self.mapSize):
            row = []
            for j in range(self.mapSize):
                if min_i <= i < max_i and min_j <= j < max_j:
                    row.append(self.mapData[i][j])
                else:
                    row.append(5)
            self.viewableMap.append(row)

    def find_hider(self):
        for i in range(len(self.viewableMap)):
            for j in range(len(self.viewableMap[i])):
                if self.viewableMap[i][j] == 2:
                    self.opponentPos = (i, j)
                    return self.opponentPos
