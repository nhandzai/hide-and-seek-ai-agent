from agent import Agent
from h_map_generator import creat_h_map


with open("map.txt", "r") as file:
    size_tuple = tuple(map(int, file.readline().split()))
    size = size_tuple[0]
    mapData = []

    for _ in range(size):
        row = list(map(int, file.readline().split()))
        mapData.append(row)

s1 = Agent(3, size, mapData)
print("Map Size:", s1.mapSize)
print("Map Data:")
for row in s1.mapData:
    print(row)
x = 1
while x != 0:
    s1.generate_viewable_map()
    s1.find_hider()
    print("Seeker pos: ", s1.pos)
    print("Viewable map: ")
    for row in s1.viewableMap:
        print(row)
    print("Hider pos: ", s1.opponentPos)
    hmap = creat_h_map(s1.opponentPos, s1.mapSize, s1.viewableMap)
    print("Hmap: ")
    for row in hmap:
        print(row)

    move = s1.find_path(hmap)
    print("move: ", move)

    mapData = s1.move_agent(move)

    print("Continue: ")
    x = int(input())
print("Map Data:")
for row in mapData:
    print(row)
