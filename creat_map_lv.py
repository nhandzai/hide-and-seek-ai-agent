def create_map_and_save(size, mapName):
    mapData = [[0 for _ in range(size[1])] for _ in range(size[0])]
    for i in range(size[0]):
        for j in range(size[1]):
            if i == 0 or i == size[0] - 1 or j == 0 or j == size[1] - 1:
                mapData[i][j] = 1
    with open(mapName, "w") as file:
        file.write(f"{size[0]} {size[1]}\n")
        for row in mapData:
            file.write(" ".join(map(str, row)) + "\n")
    return mapData


size = (10, 10)
create_map_and_save(size, "maptroll.txt")
