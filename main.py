import Seeker
import ComputeHMap
import ReadMap
from ordered_set import OrderedSet
import MyGUI
import pygame

def main():
    mapData = ReadMap.read_map("map.txt")
    pos = ReadMap.find_seeker(mapData)
    seeker = Seeker.Seeker(3, pos, len(mapData), len(mapData[0]))
    hiders_count = ReadMap.count_hiders(mapData)
    
    viewable_map = seeker.generate_viewable_map(mapData)

    hider_last_seen_pos = (0, 0)    
    hiders_set = OrderedSet()
    caught_hiders = OrderedSet()
    chased_hiders = OrderedSet()
    destination = (-1, -1)
    exploring = (0, 0)
    hmap = []
    explored = seeker.fill_explored(viewable_map, mapData)
    
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
                # reset
                if hider_last_seen_pos == seeker.pos:
                    hider_last_seen_pos = (0, 0)
                    destination = (-1, -1)
                
                # scan hiders, remove duplicate hiders by checking which hider is being chased
                # and which hiders are already caught
                hiders_set = hiders_set.union(seeker.scan_target(mapData, target=2))
                for duplicate in hiders_set.intersection(caught_hiders.union(chased_hiders)):
                    hiders_set.remove(duplicate)
                if destination == (-1, -1) and len(hiders_set) > 0:
                    destination = hiders_set.pop(0)
                    chased_hiders.add(destination)
                    if exploring != (0, 0):
                        exploring = (0, 0)
                
                # if seeker doesnt see any hider
                if destination == (-1, -1):
                    skip = False
                    # if seeker is exploring a cell
                    if exploring != (0, 0):
                        # if seeker finds out what lies at exploring cell
                        if viewable_map[exploring[0]][exploring[1]] != 5:
                            # IF HIDER, CHASE
                            if viewable_map[exploring[0]][exploring[1]] == 2:
                                destination = exploring
                                hider_last_seen_pos = exploring
                            # re-assign destination, choose a new cell to explore
                            else:
                                destination = (-1, -1)
                        
                        # if seeker hasnt found out what lies at exploring cell
                        else:
                            skip = True
                    
                    if skip == False and destination == (-1, -1):
                        # choose a random unexplored cell
                        # this is not optimal
                        exploring = seeker.explore(mapData, viewable_map, explored)
                        hmap = ComputeHMap.compute_h_map(mapData, destination=exploring)
                    
                elif hider_last_seen_pos != destination:
                    hider_last_seen_pos = destination
                    hmap = ComputeHMap.compute_h_map(mapData, destination=destination)

                # move the seeker
                if seeker.move_wrapper(hmap, mapData, target=2):
                    hiders_count -= 1
                    caught_hiders.add(seeker.pos)
                    destination = (-1, -1)
                    
                viewable_map = seeker.generate_viewable_map(mapData)
                # update explored
                seeker.update_explored(viewable_map, explored)
                
                # update the map
                screen.draw_map(mapData, viewable_map)

if __name__ == '__main__':
    main()