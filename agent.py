class Agent:
    viewRange = 5
    role = 0
    mapSize = ()
    mapData = []
    viewableMap = []
    pos = (0, 0)
    opponentPos = (0, 0)

    def __init__(self, role, mapSize, mapData):
        super().__init__()
        self.role = role
        if role == 3:
            self.viewRange = 5
        else:
            self.viewRange = 2
        self.mapSize = (mapSize, mapSize)
        self.mapData = mapData
        self.find_positions()
        self.generate_viewable_map()
        self.find_hider()

    def updateMapdata(self, mapData):
        self.mapData = mapData

    def find_positions(self):
        for i in range(self.mapSize[0]):
            for j in range(self.mapSize[1]):
                if self.mapData[i][j] == self.role:
                    self.pos = (i, j)

    def generate_viewable_map(self):
        self.viewableMap = []
        min_i = max(0, self.pos[0] - self.viewRange)
        max_i = min(self.mapSize[0], self.pos[0] + self.viewRange + 1)
        min_j = max(0, self.pos[1] - self.viewRange)
        max_j = min(self.mapSize[1], self.pos[1] + self.viewRange + 1)

        for i in range(self.mapSize[0]):
            row = []
            for j in range(self.mapSize[1]):
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

    # dir: 1-↙ 2-↓ 3-↘ 4-← 6-→ 7-↖ 8-↑ 9-↗
    # pos(,): tuple contain position
    def move_agent(self, dir):
        if dir == (0, 0):
            return self.mapData

        newPos = (self.pos[0] + dir[0],self.pos[1] + dir[1])
        self.mapData[newPos[0]][newPos[1]] = self.role
        self.mapData[self.pos[0]][self.pos[1]] = 0
        self.pos = newPos
        return self.mapData

    def find_path(self, hmap):
        minPathValue = hmap[self.pos[0]][self.pos[1] + 1][1]
        minPathPos = (self.pos[0], self.pos[1] + 1)

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != self.pos:
                    if minPathValue > hmap[self.pos[0] + i][self.pos[1] + j][1]:
                        minPathValue = hmap[self.pos[0] + i][self.pos[1] + j][1]
                        minPathPos = (self.pos[0] + i, self.pos[1] + j)
        dir = (minPathPos[0] - self.pos[0], minPathPos[1] - self.pos[1])
        return dir
