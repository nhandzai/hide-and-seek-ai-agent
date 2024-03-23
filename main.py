import Seeker
import ComputeHMap
import ReadMap

if __name__ == '__main__':
    mapData = ReadMap.read_map("map.txt")
    seeker = Seeker.Seeker(5, ReadMap.find_seeker(mapData))
      
    print(f"Map size: {len(mapData)} x {len(mapData[0])}")
    print("Map:")
    for row in mapData:
        print(row)
        
    hider_last_seen_pos = (0, 0)    
    hmap = []
    while True:
        choice = int(input("Continue: "))
        if choice == 0:
            break
        
        hider_pos = seeker.scan_target(mapData, target=2)
        if hider_pos == (-1, -1):
            seeker.explore()
        elif hider_last_seen_pos != hider_pos:
            hider_last_seen_pos = hider_pos
            hmap = ComputeHMap.compute_h_map(mapData, destination=hider_pos)

        seeker.chase(hmap, mapData)
        print("Map:")
        for row in mapData:
            print(row)