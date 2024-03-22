def create_map_and_save(size, mapName):
    mapData = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i == 0 or i == size - 1 or j == 0 or j == size - 1:
                mapData[i][j] = 1
    with open(mapName, "w") as file:
        file.write(str(size) + "\n")
        for row in mapData:
            file.write(" ".join(map(str, row)) + "\n")
    return mapData

create_map_and_save(10,"maptroll.txt")