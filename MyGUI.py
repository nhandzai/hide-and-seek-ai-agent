import pygame
import ReadMap
import math
import Seeker

WIDTH = 1368
HEIGHT = 768

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SEEKER_COLOR = (242, 75, 97)
SEEKER_VISION_COLOR = (223, 224, 171)
SPOTTED_HIDER_COLOR = (247, 181, 0)
FOG_OF_WAR = (140, 164, 171)
HIDER_COLOR = (139, 219, 88)
WALL_COLOR = (73, 73, 92)

MAP_COLOR_LIST = [WHITE, WALL_COLOR, HIDER_COLOR, SEEKER_COLOR]

class MyScreen():   
    def __init__(self, mapData):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.top = 0
        self.left = 0
        self.block_size = 0
        self.do_math(mapData)
        pass

    def do_math(self, mapData: list):
        n = len(mapData)
        m = len(mapData[0])
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

    def draw_map(self, mapData: list, seeker_pov: list):
        self.window.fill(WHITE)
        
        row = len(mapData)
        col = len(mapData[0])
        
        # draw maps
        for i in range(row):
            for j in range(col):
                cell_color = MAP_COLOR_LIST[mapData[i][j]]
                if seeker_pov[i][j] != 5:
                    if mapData[i][j] == 2:
                        cell_color = SPOTTED_HIDER_COLOR
                    elif mapData[i][j] == 0:
                        cell_color = SEEKER_VISION_COLOR
                normal_map = pygame.Rect(j * self.block_size + self.left, i * self.block_size + self.top, self.block_size, self.block_size)
                pygame.draw.rect(self.window, cell_color, normal_map)
                pygame.draw.rect(self.window, BLACK, normal_map, 1)
                
        pygame.display.flip()

def create_screen_wrapper(mapData, viewable_map, seeker):
    pygame.init()
    clock = pygame.time.Clock()
    
    screen = MyScreen(mapData)
    screen.draw_map(mapData, viewable_map)
    pygame.display.flip()

    return screen, clock
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        clock.tick(60)