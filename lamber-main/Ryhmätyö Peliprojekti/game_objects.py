import pygame
import random
import os
from config import W, H, TREE_W, TREE_H, WINDOW_H, WINDOW_W, SCREEN_H, SCREEN_W 


# Определяем путь к текущей папке
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_menu():
    """Простое меню"""
    screen = pygame.display.get_surface()
    
    # Затемнение
    overlay = pygame.Surface((SCREEN_W, SCREEN_H))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Центр меню
    menu_x = (SCREEN_W - WINDOW_W) // 2
    menu_y = (SCREEN_H - WINDOW_H) // 2
    
    # Рамка меню
    pygame.draw.rect(screen, (50, 50, 80), (menu_x, menu_y, WINDOW_W, WINDOW_H), border_radius=15)
    pygame.draw.rect(screen, (100, 100, 150), (menu_x, menu_y, WINDOW_W, WINDOW_H), 3, border_radius=15)
    
    # Текст
    font = pygame.font.Font(None, 48)
    text = font.render("SHOP", True, (255, 215, 0))
    screen.blit(text, (menu_x + WINDOW_W//2 - text.get_width()//2, menu_y + 40))
    
    font2 = pygame.font.Font(None, 24)
    text2 = font2.render("Press B to exit", True, (200, 200, 200))
    screen.blit(text2, (menu_x + WINDOW_W//2 - text2.get_width()//2, menu_y + WINDOW_H - 50))

    ## Отрисовка бутылочки и создание её зоны клика (rect)
    bottle_img = pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'shop', 'x3.png'))
    bottle_img = pygame.transform.smoothscale(bottle_img, (200, 200))
    
    # Задаем координаты и размеры для кнопки
    bottle_x = menu_x + 50
    bottle_y = menu_y + 70
    screen.blit(bottle_img, (bottle_x, bottle_y))
    
    # Прямоугольник для отслеживания кликов мышкой
    bottle_rect = pygame.Rect(bottle_x, bottle_y, 200, 200)
    
    pygame.display.update()
    
    # Ждем нажатия B или клика мыши
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return

            # Проверяем клик левой кнопкой мыши
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Если курсор попал в прямоугольник бутылки
                if bottle_rect.collidepoint(event.pos):
                    return ("x2")
                    
                    
def load_player_animations():
    """Загружает списки картинок для анимации игрока"""
    try:
        walk_right = [
            pygame.transform.smoothscale(
                pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'goright', 'playerGoright1.png')), 
                (W, H)
            ),
            pygame.transform.smoothscale(
                pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'goright', 'playerGoright2.png')), 
                (W, H)
            ),
            pygame.transform.smoothscale(
                pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'goright', 'playerGoright3.png')), 
                (W, H)
            ),
        ]
        
        walk_left = [
            pygame.transform.smoothscale(
                pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'goleft', 'playerGoleft1.png')), 
                (W, H)
            ),
            pygame.transform.smoothscale(
                pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'goleft', 'playerGoleft2.png')), 
                (W, H)
            ),
            pygame.transform.smoothscale(
                pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'goleft', 'playerGoleft3.png')), 
                (W, H)
            ),
        ]
        
        walk_stay = [
            pygame.transform.smoothscale(
                pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'gostay', 'playerGostay1.png')), 
                (W, H)
            ),
        ]
        return walk_right, walk_left, walk_stay
    except pygame.error as e:
        print(f"Ошибка загрузки анимации игрока: {e}")
        # Создаем заглушки, если файлы не найдены
        dummy_surface = pygame.Surface((W, H))
        dummy_surface.fill((255, 0, 0))
        return [dummy_surface] * 3, [dummy_surface] * 3, [dummy_surface]

def get_random_tree():
    """Выбирает случайное дерево, загружает его и скейлит"""
    try:
        derevo_files = ['derevo.png', 'derevo1.png', 'derevo2.png']
        random_file = random.choice(derevo_files)
        img = pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', random_file))
        return pygame.transform.smoothscale(img, (TREE_W, TREE_H))
    except pygame.error:
        # Если не найдены файлы деревьев, создаем заглушку
        dummy_tree = pygame.Surface((TREE_W, TREE_H))
        dummy_tree.fill((0, 255, 0))
        return dummy_tree

def spawn_tree(derevo_img):
    """Создает новый pygame.Rect для конкретного дерева"""
    new_x = random.randint(-150, 1500)
    return derevo_img.get_rect(topleft=(new_x, 450))