import pygame
import os
from config import SCREEN_W, SCREEN_H, FONT_SIZE, FONT_COLOR  # Добавили импорт FONT_SIZE, FONT_COLOR
from game_objects import load_player_animations, get_random_tree, spawn_tree, load_menu

# Определяем путь к текущей папке
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Инициализация Pygame и окна
pygame.init()
time = pygame.time.Clock() 
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Lumber Simulator") 

try:
    pygame.display.set_icon(pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'main.png')))
except:
    print("Иконка не найдена")

# Загрузка ресурсов
try:
    bg = pygame.image.load(os.path.join(CURRENT_DIR, 'pictures', 'bg.png')).convert()
except:
    bg = pygame.Surface((SCREEN_W, SCREEN_H))
    bg.fill((100, 150, 50))

walk_right, walk_left, walk_stay = load_player_animations()

# Звуки
try:
    bg_sound = pygame.mixer.Sound(os.path.join(CURRENT_DIR, 'sound', 'bgsound.mp3'))
    derevo_sound = pygame.mixer.Sound(os.path.join(CURRENT_DIR, 'sound', 'derevo.mp3'))
    bg_sound.play()
except:
    print("Звуки не загружены")

# Игровые переменные 
derevo_list = []
player_anim_count = 0   
bg_x = 0   
player_speed = 5  
player_x = 150  
player_y = 500
is_jump = False 
jump_count = 7

## money 

# score 
num5 = 1 ## множитель 
score = 0 
font = pygame.font.Font(None, FONT_SIZE)  # Используем FONT_SIZE из config

menu_open = False 

# Таймер
derevo_timer = pygame.USEREVENT + 1
pygame.time.set_timer(derevo_timer, 10000)

running = True 


    

def draw_score():
    """Рисует очки в правом верхнем углу"""
    # Создаем текст с очками
    score_text = font.render(f"score: {score}", True, FONT_COLOR)
    
    # Получаем размеры текста
    text_rect = score_text.get_rect()
    
    # Позиция в правом верхнем углу с отступом
    text_rect.topright = (SCREEN_W - 20, 20)
    
    # Рисуем полупрозрачный фон для лучшей читаемости
    bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, 
                         text_rect.width + 20, text_rect.height + 10)
    s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))  # Полупрозрачный черный
    screen.blit(s, bg_rect)
    
    # Рисуем текст поверх фона
    screen.blit(score_text, text_rect)

def handle_input():
    """Функция для движения камеры при ходьбе"""
    global bg_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        bg_x += 10  
        for tree_img, tree_rect in derevo_list:
            tree_rect.x += 10
    elif keys[pygame.K_RIGHT]:
        bg_x -= 10  
        for tree_img, tree_rect in derevo_list:
            tree_rect.x -= 10




def update_logic():
    """Вся физика: прыжки, бесшовный фон, анимация и рубка деревьев"""
    global bg_x, player_x, player_y, is_jump, jump_count, player_anim_count, score
    
    # Бесшовная прокрутка фона
    if bg_x <= -SCREEN_W: 
        bg_x += SCREEN_W
    elif bg_x >= SCREEN_W: 
        bg_x -= SCREEN_W

    keys = pygame.key.get_pressed()
    player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

    # Рубка деревьев
    for tree_tuple in derevo_list[:]:
        if player_rect.colliderect(tree_tuple[1]) and keys[pygame.K_SPACE]:
            print("The tree has been felled!")
            score += num5  # Теперь переменная score доступна для изменения

            try:
                derevo_sound.play()
            except:
                pass
            derevo_list.remove(tree_tuple)
            break 

    # Движение игрока по экрану
    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 500:
        player_x += player_speed

    # Логика прыжка
    if not is_jump:                         
        if keys[pygame.K_UP]: 
            is_jump = True 
    else:
        if jump_count >= -7:
            modifier = 1 if jump_count > 0 else -1
            player_y -= (jump_count ** 2) / 2 * modifier
            jump_count -= 1 
        else:
            is_jump = False
            jump_count = 7   

    # Кадры анимации
    player_anim_count = 0 if player_anim_count == 2 else player_anim_count + 1

def draw_screen():
    """Только отрисовка всего на экран"""
    # Рисуем фон
    screen.blit(bg, (bg_x, 0))
    if bg_x < 0:
        screen.blit(bg, (bg_x + SCREEN_W, 0))
    else:
        screen.blit(bg, (bg_x - SCREEN_W, 0))

    # Рисуем деревья
    for tree_img, tree_rect in derevo_list:
        screen.blit(tree_img, tree_rect)

    # Рисуем игрока в зависимости от нажатой кнопки
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
    elif keys[pygame.K_RIGHT]:  
        screen.blit(walk_right[player_anim_count], (player_x, player_y))
    else: 
        screen.blit(walk_stay[0], (player_x, player_y))

    # Рисуем очки поверх всего
    draw_score()

    pygame.display.update()

# ГЛАВНЫЙ ЦИКЛ ИГРЫ 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == derevo_timer:
            current_tree_img = get_random_tree() 
            current_tree_rect = spawn_tree(current_tree_img)
            derevo_list.append((current_tree_img, current_tree_rect))
        if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_b:
                # 1. Записываем то, что вернуло меню
                shop_choice = load_menu()
                
                # 2. Проверяем, что именно выбрал игрок
                if shop_choice == "x2":
                    if score >= 2: 
                        print("player use x2 ")
                        num5 = 2 
                        score -= 2 
                    else:
                        print ("u dont have money") ## потом ч'т придумать 


 
    handle_input()
    update_logic()
    draw_screen()
    
    time.tick(10)

pygame.quit()