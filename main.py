import ReadMap
import MyGUI
import pygame
import Manager
import config
import Seeker
import Hider
import ComputeHMap

def main():
    map_data = ReadMap.read_map("map.txt")
    seeker = Seeker.Seeker(config.SEEKER_VIEW_RANGE, ReadMap.find_seeker(map_data))
    hiders_pos = ReadMap.find_hiders(map_data)
    hiders = []
    id = 1
    for pos in hiders_pos:
        hiders.append(Hider.Hider(config.HIDER_VIEW_RANGE, pos, config.HIDER_CAN_MOVE, id))
        id += 1
        
    manager = Manager.Manager(seeker, hiders, map_data)

    hider_last_seen_pos = (0, 0)    
    destination = (-1, -1)
    hmap = []
    turns = 1
    seeker_turn = True
    pings = manager.pings
    pos_dfs = (-1,-1)
    
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
                if seeker_turn:          
                    viewable_map = seeker.generate_viewable_map(map_data)
                    destination = seeker.scan_target(map_data, 2, viewable_map)
                    
                    if turns == 1 and destination == (-1, -1):
                        pos_dfs = seeker.find_pos_DFS(ComputeHMap.compute_h_map(map_data, seeker.pos))
                    if destination == (-1, -1):
                        if turns < 5:
                            hmap = ComputeHMap.compute_h_map(map_data, pos_dfs)

                    elif hider_last_seen_pos != destination:
                        hider_last_seen_pos = destination
                        hmap = ComputeHMap.compute_h_map(map_data, destination)

                    # move the seeker
                    seeker.move_wrapper(hmap, map_data)
                    manager.check_hiders()
                    
                    seeker_turn = False
                else:
                    # ping
                    if(turns % 5 == 0):
                        manager.hiders_ping(map_data)
                        print(pings)
                    
                    if config.HIDER_CAN_MOVE:
                        manager.move_hiders(map_data)
                    
                    seeker_turn = True
                    turns += 1
                    
                # update the map
                screen.draw_map(map_data, manager)
                turns += 1

if __name__ == '__main__':
    main()
