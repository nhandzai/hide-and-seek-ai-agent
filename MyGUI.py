import pygame
import math
import Manager
import config

WIDTH = 1368
HEIGHT = 768

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SEEKER_COLOR = (242, 75, 97)
SEEKER_VISION_COLOR = (223, 224, 171)
HIDER_COLOR = (139, 219, 88)
SPOTTED_HIDER_COLOR = (247, 181, 0)
HIDER_VISION_COLOR = (102, 228, 237)
INTERSECTION_VISION_COLOR = (69,96,69)
FOG_OF_WAR = (140, 164, 171)
WALL_COLOR = (73, 73, 92)

MAP_COLOR_LIST = [WHITE, WALL_COLOR, HIDER_COLOR, SEEKER_COLOR]

class MyScreen():   
    def __init__(self, map_data):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.top = 0
        self.left = 0
        self.block_size = 0
        self.do_math(map_data)
        self.seeker_img = pygame.image.load('images\\seeker.jpg').convert()
        self.seeker_img = pygame.transform.scale(self.seeker_img, (self.block_size, self.block_size))
        self.hider_img = pygame.image.load('images\\hider.jpg').convert()
        self.hider_img = pygame.transform.scale(self.hider_img, (self.block_size, self.block_size))

    def do_math(self, map_data: list):
        n = len(map_data)
        m = len(map_data[0])
        row = n
        col = m
        
        x = self.window.get_width()
        y = self.window.get_height()
        
        aspect_ratio_1 = x / y
        aspect_ratio_2 = m / n
        
        # scale maps' size to window's size
        if aspect_ratio_1 >= aspect_ratio_2:
            n = y
            m = n * aspect_ratio_2
            self.top = 0
            self.left = (x - m) / 2
        else:
            m = x
            n = m / aspect_ratio_2
            self.top = (self.window.get_height() - n) / 2
            self.left = 0

        self.block_size = int(math.sqrt((m * n) / (row * col)))

    def draw_map(self, map_data: list, manager: Manager.Manager):
        self.window.fill(WHITE)
        
        row = len(map_data)
        col = len(map_data[0])
        
        # draw maps
        seeker_pos = manager.seeker.pos
        seeker_pov = manager.seeker.generate_viewable_map(map_data)
        for i in range(row):
            for j in range(col):
                cell_color = MAP_COLOR_LIST[map_data[i][j]]
                if seeker_pov[i][j]:
                    if map_data[i][j] == 2:
                        cell_color = SPOTTED_HIDER_COLOR
                    elif map_data[i][j] == 0:
                        cell_color = SEEKER_VISION_COLOR
                        
                if config.HIDER_CAN_MOVE:
                    for hider in manager.hiders:
                        hider_pov = hider.generate_viewable_map(map_data)
                        if hider_pov[i][j] and seeker_pov[i][j] and map_data[i][j] == 0:
                            cell_color = INTERSECTION_VISION_COLOR
                            break 
                        elif hider_pov[i][j] and map_data[i][j] == 0:
                            cell_color = HIDER_VISION_COLOR
                            break

                            
                normal_map = pygame.Rect(j * self.block_size + self.left, i * self.block_size + self.top, self.block_size, self.block_size)
                if(cell_color != INTERSECTION_VISION_COLOR):
                    pygame.draw.rect(self.window, cell_color, normal_map)
                    pygame.draw.rect(self.window, BLACK, normal_map, 1)
                else:
                    draw_intersection_cell(self, normal_map)
                
        self.window.blit(self.seeker_img, pygame.Rect(seeker_pos[1] * self.block_size + self.left, seeker_pos[0] * self.block_size + self.top, self.block_size, self.block_size))
        for hider in manager.hiders:
            self.window.blit(self.hider_img, pygame.Rect(hider.pos[1] * self.block_size + self.left, hider.pos[0] * self.block_size + self.top, self.block_size, self.block_size))
        pygame.display.flip()

def draw_intersection_cell(self, cell_rect:pygame.Rect):
    # Draw left half with HIDER_VISION_COLOR
    left_half = cell_rect.copy()
    left_half.width /= 2
    pygame.draw.rect(self.window, HIDER_VISION_COLOR, left_half)
    
    
    # Draw right half with SEEKER_VISION_COLOR
    right_half = cell_rect.copy()
    right_half.width /= 2
    right_half.left += right_half.width
    pygame.draw.rect(self.window, SEEKER_VISION_COLOR, right_half)

    pygame.draw.rect(self.window, BLACK, cell_rect, 1)

def create_screen_wrapper(map_data, manager: Manager.Manager):
    pygame.init()
    clock = pygame.time.Clock()
    
    screen = MyScreen(map_data)
    screen.draw_map(map_data, manager)
    pygame.display.flip()

    return screen, clock