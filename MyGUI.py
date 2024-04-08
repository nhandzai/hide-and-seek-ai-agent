import pygame
import math
import Manager
import config

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

BG_COLOR = (160, 160, 160)
BLACK = (0, 0, 0, 200)
TEXT_COLOR = (255, 0, 0)
SEEKER_COLOR = (242, 75, 97, 160)
SEEKER_VISION_COLOR = (255, 96, 81, 160)
HIDER_COLOR = (139, 219, 88, 160)
HIDER_VISION_COLOR = (59, 50, 157, 160)
OVERLAP_VISION_COLOR = (200, 48, 109, 160)

class MyScreen():   
    def __init__(self, map_data):
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hide and seek, group 1")
        self.top = 0
        self.left = 0
        self.block_size = 0
        self.do_math(map_data)
        
        self.seeker_img = None
        self.hider_img = None
        self.wall_texture = None
        self.floor_texture = None
        self.obstacle_texture = None
        self.load_images()
        
        self.displaying_score = False
        
        self.window.blit(self.floor_texture, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))        
        
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
        
    def load_images(self):
        self.seeker_img = pygame.image.load('images\\seeker.png').convert_alpha()
        self.seeker_img = pygame.transform.scale(self.seeker_img, (self.block_size, self.block_size))
        self.hider_img = pygame.image.load('images\\hider.png').convert_alpha()
        self.hider_img = pygame.transform.scale(self.hider_img, (self.block_size, self.block_size))
        self.floor_texture = pygame.image.load('images\\floor_texture.png').convert()
        self.floor_texture = pygame.transform.scale(self.floor_texture, (self.block_size, self.block_size))
        self.wall_texture = pygame.image.load('images\\wall_texture.png').convert()
        self.wall_texture = pygame.transform.scale(self.wall_texture, (self.block_size, self.block_size))
        self.obstacle_texture = pygame.image.load('images\\obstacle.png').convert_alpha()
        self.obstacle_texture = pygame.transform.scale(self.obstacle_texture, (self.block_size, self.block_size))
        
    def seen_by_hider(self, map_data, i, j, manager: Manager.Manager):
        for hider in manager.hiders:
            hider_pov = hider.generate_viewable_map(map_data)
            if hider_pov[i][j]:
                return True
        return False
        
    def draw_map(self, map_data: list, manager: Manager.Manager):
        self.window.fill(BG_COLOR)
        row = len(map_data)
        col = len(map_data[0])
        
        # surface to draw transparent shapes
        trans_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # draw maps
        seeker_pos = manager.seeker.pos
        seeker_pov = manager.seeker.generate_viewable_map(map_data)
        for i in range(row):
            for j in range(col):
                if map_data[i][j] == 1:
                    self.window.blit(self.wall_texture, (j * self.block_size + self.left, i * self.block_size + self.top, self.block_size, self.block_size))                    
                
                else:
                    self.window.blit(self.floor_texture, (j * self.block_size + self.left, i * self.block_size + self.top, self.block_size, self.block_size))

                    if map_data[i][j] == 4:
                        trans_surface.blit(self.obstacle_texture, (j * self.block_size + self.left, i * self.block_size + self.top, self.block_size, self.block_size))
                        continue
                    
                    cell_color = None
                    seen_by_hider = self.seen_by_hider(map_data, i, j, manager)
                    
                    if seeker_pov[i][j] and seen_by_hider:
                        if map_data[i][j] != 2 and map_data[i][j] != 3:
                            cell_color = OVERLAP_VISION_COLOR
                        elif map_data[i][j] == 2:
                            cell_color = SEEKER_VISION_COLOR
                        else:
                            cell_color = HIDER_VISION_COLOR
                        drawing_rect = pygame.Rect(j * self.block_size + self.left, i * self.block_size + self.top, self.block_size, self.block_size)
                        pygame.draw.rect(trans_surface, cell_color, drawing_rect)  
                        
                    elif seeker_pov[i][j]:
                        if map_data[i][j] == 3:
                            cell_color = SEEKER_COLOR
                        else:
                            cell_color = SEEKER_VISION_COLOR
                        drawing_rect = pygame.Rect(j * self.block_size + self.left, i * self.block_size + self.top, self.block_size, self.block_size)
                        pygame.draw.rect(trans_surface, cell_color, drawing_rect)  
                    
                    elif seen_by_hider:
                        if map_data[i][j] == 2:
                            cell_color = HIDER_COLOR
                        else: 
                            cell_color = HIDER_VISION_COLOR
                        drawing_rect = pygame.Rect(j * self.block_size + self.left, i * self.block_size + self.top, self.block_size, self.block_size)
                        pygame.draw.rect(trans_surface, cell_color, drawing_rect)  
                        
        trans_surface.blit(self.seeker_img, pygame.Rect(seeker_pos[1] * self.block_size + self.left, seeker_pos[0] * self.block_size + self.top, self.block_size, self.block_size))
        for hider in manager.hiders:
            trans_surface.blit(self.hider_img, pygame.Rect(hider.pos[1] * self.block_size + self.left, hider.pos[0] * self.block_size + self.top, self.block_size, self.block_size))

        self.window.blit(trans_surface, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.flip()
        
    def display_score(self, map_data, manager, turns = 0, caught_number = 0, game_over = False):
        points = - turns + 20 * caught_number + config.DEFAULT_POINTS
        if game_over:
            font_size = config.GAME_OVER_FONT_SIZE
        else:
            font_size = config.IN_GAME_FONT_SIZE
        font = pygame.font.Font('fonts\\joystix monospace.ttf', font_size)
        
        game_points = font.render(f'GAME POINTS: {points}', True, TEXT_COLOR)
        game_points_rect = game_points.get_rect()
        
        caught = font.render(f'CAUGHT: {caught_number}', True, TEXT_COLOR)
        caught_rect = caught.get_rect()
        
        steps = font.render(f'STEPS TAKEN: {turns}', True, TEXT_COLOR)
        steps_rect = steps.get_rect()
        
        if game_over:
            game_points_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - font_size)
            caught_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            steps_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + font_size)
        else:
            game_points_rect.topleft = (0, 10)
            caught_rect.topleft = (0, 10 + font_size)
            steps_rect.topleft = (0, 10 + 2 * font_size)
        
        if game_over and self.displaying_score == False:
            self.displaying_score = True
            self.draw_map(map_data, manager)
            
        self.window.blit(game_points, game_points_rect)
        self.window.blit(caught, caught_rect)
        self.window.blit(steps, steps_rect)
        pygame.display.flip()

def create_screen_wrapper(map_data, manager: Manager.Manager):
    pygame.init()
    clock = pygame.time.Clock()
    
    screen = MyScreen(map_data)
    screen.draw_map(map_data, manager)
    pygame.display.flip()

    return screen, clock