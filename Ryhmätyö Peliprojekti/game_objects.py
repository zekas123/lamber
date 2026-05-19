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

# --- ВОТ ЭТОТ КУСОК ДЛЯ СЛУЧАЙНЫХ ДЕРЕВЬЕВ ---

def get_random_tree():
    """Выбирает случайное дерево, загружает его и скейлит"""
    derevo_files = ['pictures/derevo.png', 'pictures/derevo1.png', 'pictures/derevo2.png']
    
    # Случайно выбираем один из файлов
    random_file = random.choice(derevo_files) 
    
    # Загружаем и сразу подгоняем под размер TREE_W, TREE_H
    img = pygame.image.load(random_file)
    return pygame.transform.smoothscale(img, (TREE_W, TREE_H))

def spawn_tree(derevo_img):
    """Создает новый pygame.Rect для конкретного дерева"""
    new_x = random.randint(-150, 1500)
    return derevo_img.get_rect(topleft=(new_x, 450)) # Твоя высота 450