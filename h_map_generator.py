def creat_h_map(pos, mapData):
    hmap = []
    for i in range(len(mapData)):
        rowData = []
        for j in range(len(mapData[i])):
            if mapData[i][j] == 1 or mapData[i][j] == 5:
                rowData.append((1, pos[0] * pos[1]))
            else:
                dist = max(abs(pos[0] - i), abs(pos[1] - j))
                rowData.append((mapData[i][j], dist))
        hmap.append(rowData)

    return hmap
