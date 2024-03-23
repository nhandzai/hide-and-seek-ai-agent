import math

def compute_h_map(map, destination):
    hmap = []
    for i in range(len(map)):
        rowData = []
        for j in range(len(map[i])):
            if map[i][j] == 1 or map[i][j] == 5 :
                rowData.append(math.inf)
            else:
                dist = max(abs(destination[0] - i), abs(destination[1] - j))
                rowData.append(dist)
        hmap.append(rowData)

    return hmap