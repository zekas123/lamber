import pygame

# Заменили load_tree_image на get_random_tree
from config import SCREEN_W, SCREEN_H
from game_objects import load_player_animations, get_random_tree, spawn_tree

# Инициализация Pygame и окна
pygame.init()
time = pygame.time.Clock() 
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Lumber Simulator") 
pygame.display.set_icon(pygame.image.load('pictures/main.png')) 

# Загрузка ресурсов
bg = pygame.image.load('pictures/bg.png').convert() 

walk_right, walk_left, walk_stay = load_player_animations()

bg_sound = pygame.mixer.Sound('sound/bgsound.mp3') 
derevo_sound = pygame.mixer.Sound('sound/derevo.mp3')
bg_sound.play() 

# Игровые переменные 

derevo_list = []
player_anim_count = 0   
bg_x = 0   
player_speed = 5  
player_x = 150  
player_y = 500
is_jump = False 
jump_count = 7

# Таймер
derevo_timer = pygame.USEREVENT + 1
pygame.time.set_timer(derevo_timer, 10000)

running = True 

#  ФУНКЦИИ ИГРОВОГО ЦИКЛА 

def handle_input():
    """Функция для движения камеры при ходьбе"""
    global bg_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        bg_x += 10  
        # Распаковываем картинку и рект, двигаем только рект
        for tree_img, tree_rect in derevo_list:
            tree_rect.x += 10
    elif keys[pygame.K_RIGHT]:
        bg_x -= 10  
        for tree_img, tree_rect in derevo_list:
            tree_rect.x -= 10

def update_logic():
    """Вся физика: прыжки, бесшовный фон, анимация и рубка деревьев"""
    global bg_x, player_x, player_y, is_jump, jump_count, player_anim_count
    
    # Бесшовная прокрутка фона
    if bg_x <= -SCREEN_W: bg_x += SCREEN_W
    elif bg_x >= SCREEN_W: bg_x -= SCREEN_W

    keys = pygame.key.get_pressed()
    player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

    # Рубка деревьев
    for tree_tuple in derevo_list:
        # tree_tuple[1] — это рект дерева
        if player_rect.colliderect(tree_tuple[1]) and keys[pygame.K_SPACE]:
        
            print(f"Дерево срублено!")
            derevo_sound.play()
            derevo_list.remove(tree_tuple)
            break 

    # Движение игрока по экрану
    if keys[pygame.K_LEFT] and player_x > 50:
        player_x -= player_speed
    elif keys[pygame.K_RIGHT] and player_x < 500:
        player_x += player_speed

    # Логика прыжка
    if not is_jump:                         
        if keys[pygame.K_UP]: is_jump = True 
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

    # Рисуем деревья (у каждого своя собственная картинка и свой рект)
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

    handle_input()   # 1. Управление камерой
    update_logic()   # 2. Расчет физики и коллизий
    draw_screen()    # 3. Вывод на экран
    
    time.tick(10)

pygame.quit()