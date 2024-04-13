import ReadMap
import MyGUI
import pygame
import Manager
import Seeker
import Hider
import ComputeHMap
import math
import Obstacle
import SetLevelMap

def main():
    config, map_path = SetLevelMap.choose_level()
    map_data,obsts_list = ReadMap.read_map(map_path)
    seeker = Seeker.Seeker(config["SEEKER_VIEW_RANGE"], ReadMap.find_seeker(map_data))
    hiders_pos = ReadMap.find_hiders(map_data)
    hiders = []
    id = 1
    for pos in hiders_pos:
        hiders.append(
            Hider.Hider(config["HIDER_VIEW_RANGE"], pos, config["HIDER_CAN_MOVE"], id)
        )
        id += 1

    manager = Manager.Manager(seeker, hiders, map_data,obsts_list)

    hider_last_seen_pos = (-1, -1)
    destination = (-1, -1)
    guessing_pos = (-1,-1)
    hmap = []
    turns = 1
    seeker_turn = True
    chasing = False
    pings = manager.pings
    hider_range={}
    cells_visited={}
    screen, clock = MyGUI.create_screen_wrapper(map_data, manager)
    running = True
    first_input = False

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                first_input = True

        if first_input == False:
            continue
        
        if len(manager.hiders) == 0 or turns == config["TIME_LIMIT"]:
            caught_number = id - 1 - len(hiders)
            screen.display_score(map_data, manager, config, turns, caught_number, True)
            continue

        pygame.time.delay(config["STEP_INTERVAL"])
        if seeker_turn:
            viewable_map = seeker.generate_viewable_map(map_data)
            destination = seeker.scan_target(map_data, 2, viewable_map)
            
            manager.delete_seen_pings(destination)

            if hider_last_seen_pos != (-1, -1) or destination != (-1, -1):
                chasing = True
                if destination != (-1,-1):
                    hider_last_seen_pos = destination

            if chasing == True:
                hmap = ComputeHMap.compute_h_map(map_data, hider_last_seen_pos)
            else:
                if turns < 5:
                    guessing_pos = seeker.find_pos_DFS(
                        ComputeHMap.compute_h_map(map_data, seeker.pos)
                    )
                else:
                    
                    if  len(pings) == 0 :
                        guessing_pos = seeker.find_pos_DFS(
                            ComputeHMap.compute_h_map(map_data, seeker.pos)
                        )
                    else:
                        if(len(hider_range)==0):
                            hider_range = {key: [-math.inf, math.inf, -math.inf, math.inf] for key in pings}
                            cells_visited={key:[] for key in pings}
                        guessing_pos = seeker.process_pings(pings, hider_range, map_data, cells_visited, config)
                
                hmap = ComputeHMap.compute_h_map(map_data, guessing_pos) 
                
            seeker.move_wrapper(hmap, map_data)
            
            if manager.check_hiders():
                chasing = False
                hider_last_seen_pos = (-1, -1)
                destination = (-1,-1)

            viewable_map = seeker.generate_viewable_map(map_data)
            destination = seeker.scan_target(map_data, 2, viewable_map)

            #manager.delete_seen_pings(destination)
            manager.delete_seen_hider( viewable_map,map_data,hider_range,cells_visited)

            if hider_last_seen_pos != (-1, -1) or destination != (-1, -1):
                chasing = True
                if destination != (-1,-1):
                    hider_last_seen_pos = destination

            seeker_turn = False
            
        else:
            # ping
            if turns % 5 == 0:
                manager.hiders_ping(map_data, config)
        
            if config["HIDER_CAN_MOVE"]:
                manager.move_hiders(map_data)
            
            seeker_turn = True
            turns += 1

        # update the screen
        screen.draw_map(map_data, manager)
        screen.draw_ping(pings)
        screen.display_score(map_data, manager, config, turns, id - 1 - len(hiders))

if __name__ == "__main__":
    main()