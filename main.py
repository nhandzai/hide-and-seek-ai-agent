import Seeker
import ReadMap
import MyGUI
import pygame
import Manager
import Hider
import config

def main():
    map_data = ReadMap.read_map("map.txt")
    seeker = Seeker.Seeker(config.SEEKER_VIEW_RANGE, ReadMap.find_seeker(map_data))
    hiders_pos = ReadMap.find_hiders(map_data)
    hiders = []
    for pos in hiders_pos:
        hiders.append(Hider.Hider(config.HIDER_VIEW_RANGE, pos, config.HIDER_CAN_MOVE))
        
    manager = Manager.Manager(seeker, hiders, map_data)

    hider_last_seen_pos = (0, 0)    
    destination = (-1, -1)
    hmap = []
    
    screen, clock = MyGUI.create_screen_wrapper(map_data, manager)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            clock.tick(60)
            
            if len(manager.hiders) == 0:
                continue
            
            if event.type == pygame.KEYDOWN:
                destination = seeker.scan_target(map_data, 2)
                if destination == (-1, -1):
                    seeker.explore()
                    continue
                elif hider_last_seen_pos != destination:
                    hider_last_seen_pos = destination
                    hmap = Manager.Manager.hmaps[destination]

                # move the seeker
                seeker.move_wrapper(hmap, map_data)
                               
                # update the map
                screen.draw_map(map_data, manager)

if __name__ == '__main__':
    main()