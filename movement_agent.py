class Movement:

    pos = (0, 0)
    movePos = [
        [1, pos[0] + 1, pos[1] - 1],
        [2, pos[0] + 1, pos[1]],
        [3, pos[0] + 1, pos[1] + 1],
        [4, pos[0], pos[1] - 1],
        [6, pos[0], pos[1] + 1],
        [7, pos[0] - 1, pos[1] - 1],
        [8, pos[0] - 1, pos[1]],
        [9, pos[0] - 1, pos[1] + 1],
    ]

    def update_movePos(self, pos):
        self.movePos = [
            [1, pos[0] + 1, pos[1] - 1],
            [2, pos[0] + 1, pos[1]],
            [3, pos[0] + 1, pos[1] + 1],
            [4, pos[0], pos[1] - 1],
            [6, pos[0], pos[1] + 1],
            [7, pos[0] - 1, pos[1] - 1],
            [8, pos[0] - 1, pos[1]],
            [9, pos[0] - 1, pos[1] + 1],
        ]

    # dir: 1-↙ 2-↓ 3-↘ 4-← 6-→ 7-↖ 8-↑ 9-↗
    # pos(,): tuple contain position
    def move_agent(self, map, agent, pos, dir):
        self.update_movePos(pos)
        newPos = pos
        for move in self.movePos:
            if move[0] == dir:
                newPos = (move[1], move[2])
        map[newPos[0]][newPos[1]] = agent
        map[pos[0]][pos[1]] = 0
        return newPos

    def find_path(self, hmap, pos):
        minPath = hmap[pos[0]][pos[1]+1][1]
        minPathPos = (pos[0],pos[1]+1)
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i,j) != pos:
                    if(minPath > hmap[pos[0]+i][pos[1]+j][1]):
                        minPath = hmap[pos[0]+i][pos[1]+j][1]
                        minPathPos = (pos[0]+i,pos[1]+j)
        self.update_movePos(pos)
        for move in self.movePos:
            if move[1] == minPathPos[0] and move[2] == minPathPos[1]:
                return move[0]
        return 5
