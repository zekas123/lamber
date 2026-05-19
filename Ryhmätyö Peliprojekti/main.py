import pygame
import random 

pygame.init()
time = pygame.time.Clock() 

screen = pygame.display.set_mode((1518, 704))
pygame.display.set_caption("Lumber Simulator") 
icon = pygame.image.load('pictures/main.png') 
pygame.display.set_icon(icon) 

bg = pygame.image.load('pictures/bg.png').convert() 

W, H = 100, 150 
TREE_W, TREE_H = 150, 300  
derevo = pygame.image.load('pictures/derevo.png')
derevo = pygame.transform.smoothscale(derevo, (TREE_W, TREE_H))

# Анимации
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

# Список для хранения объектов pygame.Rect каждого заспавненного дерева
derevo_list = []

player_anim_count = 0   
bg_x = 0  

player_speed = 5  
player_x = 150  
player_y = 380

is_jump = False 
jump_count = 7

bg_sound = pygame.mixer.Sound('sound/bgsound.mp3') 
derevo_sound = pygame.mixer.Sound('sound/derevo.mp3')
bg_sound.play() 

running = True 

# Настройка таймера спавна 1000 мс = 1 с
derevo_timer = pygame.USEREVENT + 1
pygame.time.set_timer(derevo_timer, 10000)

while running:
    # 1. ОБРАБОТКА СОБЫТИЙ 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Спавн нового дерева по таймеру
        if event.type == derevo_timer:
            # Выбираем рандомный X прямо в момент спавна!
            new_x = random.randint(-150, 1500)
            # Создаем рект для нового дерева и добавляем в список
            new_tree_rect = derevo.get_rect(topleft=(new_x, 220))
            derevo_list.append(new_tree_rect)

    keys = pygame.key.get_pressed()

    # Смещение фона и ВСЕХ деревьев в списке при ходьбе
    if keys[pygame.K_LEFT]:
        bg_x += 10  
        for tree_rect in derevo_list:
            tree_rect.x += 10
    elif keys[pygame.K_RIGHT]:
        bg_x -= 10  
        for tree_rect in derevo_list:
            tree_rect.x -= 10

    # Бесшовная прокрутка фона
    if bg_x <= -1518:
        bg_x += 1518
    elif bg_x >= 1518:
        bg_x -= 1518

    # 2. ОТРИСОВКА ФОНА (самый нижний слой)
    screen.blit(bg, (bg_x, 0))
    if bg_x < 0:
        screen.blit(bg, (bg_x + 1518, 0))
    else:
        screen.blit(bg, (bg_x - 1518, 0))

    # Обновляем хитбокс игрока для проверки коллизий
    player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))


    # 3. ОТРИСОВКА ДЕРЕВЬЕВ И ПРОВЕРКА КОЛЛИЗИЙ (поверх фона)
    if derevo_list:
        for tree_rect in derevo_list:
            screen.blit(derevo, tree_rect) # Рисуем дерево
            
            # Если игрок подошел к дереву и нажал ПРОБЕЛ
            if player_rect.colliderect(tree_rect) and keys[pygame.K_SPACE]:
                print("Дерево срублено!")
                derevo_sound.play()
                derevo_list.remove(tree_rect) # Удаляем этот конкретный хитбокс из списка
                break # Обязательно выходим из цикла, чтобы не поломать перебор списка

    # 4. ЛОГИКА И ОТРИСОВКА ПЕРСОНАЖА (поверх деревьев)
    if keys[pygame.K_LEFT]: 
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
        if player_x > 50:
            player_x -= player_speed
    elif keys[pygame.K_RIGHT]:  
        screen.blit(walk_right[player_anim_count], (player_x, player_y))
        if player_x < 500:
            player_x += player_speed
    else: 
        screen.blit(walk_stay[0], (player_x, player_y))

    # Логика прыжка
    if not is_jump:                         
        if keys[pygame.K_UP]:
            is_jump = True 
    else:
        if jump_count >= -7:
            if jump_count > 0:
                player_y -= (jump_count ** 2) / 2 
            else:  
                player_y += (jump_count ** 2) / 2 
            jump_count -= 1 
        else:
            is_jump = False
            jump_count = 7   

    # Анимация
    if player_anim_count == 2: 
        player_anim_count = 0 
    else:
        player_anim_count += 1 

    pygame.display.update()
    time.tick(10)

pygame.quit()