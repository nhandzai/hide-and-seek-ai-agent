def read_map(path) :
    with open(path, "r") as file:
        n, m = file.readline().split()
        n = int(n)
        m = int(m)
        mapData = []

        for _ in range(n):
            row = list(map(int, file.readline().split()))
            mapData.append(row)
            
    return mapData

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