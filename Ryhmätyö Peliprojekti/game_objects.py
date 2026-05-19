import pygame
import random
from config import W, H, TREE_W, TREE_H

def load_player_animations():
    """Загружает списки картинок для анимации игрока"""
    walk_right = [
        pygame.transform.smoothscale(pygame.image.load('pictures/goright/playerGoright1.png'), (W, H)),
        pygame.transform.smoothscale(pygame.image.load('pictures/goright/playerGoright2.png'), (W, H)),
        pygame.transform.smoothscale(pygame.image.load('pictures/goright/playerGoright3.png'), (W, H)),
    ]
    walk_left = [
        pygame.transform.smoothscale(pygame.image.load('pictures/goleft/playerGoleft1.png'), (W, H)),
        pygame.transform.smoothscale(pygame.image.load('pictures/goleft/playerGoleft2.png'), (W, H)),
        pygame.transform.smoothscale(pygame.image.load('pictures/goleft/playerGoleft3.png'), (W, H)),
    ]
    walk_stay = [
        pygame.transform.smoothscale(pygame.image.load('pictures/gostay/playerGostay1.png'), (W, H)),
    ]
    return walk_right, walk_left, walk_stay

def load_tree_image():
    """Загружает и скейлит картинку дерева"""
    derevo = pygame.image.load('pictures/derevo.png')
    return pygame.transform.smoothscale(derevo, (TREE_W, TREE_H))

def spawn_tree(derevo_img):
    """Создает новый pygame.Rect для дерева в случайном месте"""
    new_x = random.randint(-150, 1500)
    return derevo_img.get_rect(topleft=(new_x, 220))