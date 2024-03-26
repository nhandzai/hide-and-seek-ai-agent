import Seeker
import ComputeHMap
import ReadMap
import MyGUI
import pygame
import Manager

def main():
    map_data = ReadMap.read_map("map.txt")
    pos = ReadMap.find_seeker(map_data)
    seeker = Seeker.Seeker(5, pos, len(map_data), len(map_data[0]))
    hiders = ReadMap.find_hiders(map_data)
    manager = Manager.Manager(seeker, hiders, map_data)
    
    viewable_map = seeker.generate_viewable_map(map_data)

    hider_last_seen_pos = (0, 0)    
    destination = (-1, -1)
    hmap = []
    
    screen, clock = MyGUI.create_screen_wrapper(map_data, viewable_map, seeker)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            clock.tick(60)
            if manager.hiders == 0:
                continue
            if event.type == pygame.KEYDOWN:

                destination = seeker.scan_target(map_data, 2)
                if destination == (-1, -1):
                    seeker.explore()
                    continue
                elif hider_last_seen_pos != destination:
                    hider_last_seen_pos = destination
                    hmap = ComputeHMap.compute_h_map(map_data, destination=destination)

                # move the seeker
                seeker.move_wrapper(hmap, map_data)
                
                viewable_map = seeker.generate_viewable_map(map_data)
                
                # update the map
                screen.draw_map(map_data, viewable_map)

if __name__ == '__main__':
    main()