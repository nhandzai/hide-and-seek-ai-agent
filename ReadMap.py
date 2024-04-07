def read_map(path):
    with open(path, "r") as file:
        n, m = file.readline().split()
        n = int(n)
        m = int(m)
        mapData = []
        obst = []
        for _ in range(n):
            row = list(map(int, file.readline().split()))
            mapData.append(row)
        for line in file:
            obst_row = list(map(int, line.split()))
            obst.append(obst_row)
        mapData = create_obstacles_to_map(mapData,obst)
    return mapData,obst

def find_seeker(mapData):
    for i in range(len(mapData)):
        for j in range(len(mapData[i])):
            if mapData[i][j] == 3:
                return (i, j)
    return (-1, -1)

def find_hiders(mapData) -> list:
    hiders = []
    for i in range(len(mapData)):
        for j in range(len(mapData[i])):
            if mapData[i][j] == 2:
                hiders.append((i, j))
    return hiders

def create_obstacles_to_map(mapData, obstacles):
    for obst in obstacles:
        top, left, bottom, right = obst
        for i in range(top, bottom + 1):
            for j in range(left, right + 1):
                mapData[i][j] = 4
    return mapData


