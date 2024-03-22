def creat_h_map(row, col, mapData):
    hmap = []
    for i in range(len(mapData)):
        rowData = []
        for j in range(len(mapData[i])):
            if mapData[i][j] == 1 or mapData[i][j] == 5 :
                rowData.append((1, 99))
            else:
                dist = max(abs(row - i), abs(col - j))
                rowData.append((mapData[i][j], dist))
        hmap.append(rowData)

    return hmap
