import Seeker
import ComputeHMap
import ReadMap
import MyGUI
import pygame

def main():
    mapData = ReadMap.read_map("map.txt")
    pos = ReadMap.find_seeker(mapData)
    seeker = Seeker.Seeker(5, pos, len(mapData), len(mapData[0]))
    hiders_count = ReadMap.count_hiders(mapData)
    
    viewable_map = seeker.generate_viewable_map(mapData)

    hider_last_seen_pos = (0, 0)    
    destination = (-1, -1)
    hmap = []
    
    screen, clock = MyGUI.create_screen_wrapper(mapData, viewable_map, seeker)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            clock.tick(60)
            if hiders_count == 0:
                continue
            if event.type == pygame.KEYDOWN:

                destination = seeker.scan_target(mapData, 2)
                if destination == (-1, -1):
                    seeker.explore()
                    continue
                elif hider_last_seen_pos != destination:
                    hider_last_seen_pos = destination
                    hmap = ComputeHMap.compute_h_map(mapData, destination=destination)

                # move the seeker
                seeker.move_wrapper(hmap, mapData)
                
                viewable_map = seeker.generate_viewable_map(mapData)
                
                # update the map
                screen.draw_map(mapData, viewable_map)

if __name__ == '__main__':
    main()