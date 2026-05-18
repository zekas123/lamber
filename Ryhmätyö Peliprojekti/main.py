import pygame


pygame.init()
time = pygame.time.Clock() # иниц время 
# указал екран 
screen = pygame.display.set_mode((1518, 704))
pygame.display.set_caption("Lumber Simulator") # название 
icon = pygame.image.load('pictures/main.png') # иконка 
pygame.display.set_icon(icon) 

bg = pygame.image.load('pictures/bg.png') # задний фон 

W, H = 100, 150 # размері перса

# анимки 
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

player_anim_count = 0   # сч'тчик для анимок 
bg_x = 0  # координата по х  фона 

player_speed = 5  # скорость 
player_x = 150  # координата по х  игрока
player_y = 380

is_jump = False 

jump_count = 7

bg_sound = pygame.mixer.Sound('sound/bgsound.mp3') # музон 
bg_sound.play() #  вкл музон 

running = True # основеной цикл 
while running:

    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT]:
        bg_x += 10  # Движение влево
    elif keys[pygame.K_RIGHT]:
        bg_x -= 10  # Движение вправо

    # Умная бесшовная прокрутка фона в обе стороны
    if bg_x <= -1518:
        bg_x += 1518
    elif bg_x >= 1518:
        bg_x -= 1518

    # Рисуем основной фон
    screen.blit(bg, (bg_x, 0))
    # Рисуем второй фон ДОПОЛНИТЕЛЬНО: если bg_x ушел в минус, рисуем его справа (+1518),
    # а если bg_x ушел в плюс, рисуем его слева (-1518)
    if bg_x < 0:
        screen.blit(bg, (bg_x + 1518, 0))
    else:
        screen.blit(bg, (bg_x - 1518, 0))


    # --- ЛОГИКА И ОТРИСОВКИ ПЕРСОНАЖА ---
    if keys[pygame.K_LEFT]: # в лево 
        screen.blit(walk_left[player_anim_count], (player_x, player_y))
        if player_x > 50:
            player_x -= player_speed

    elif keys[pygame.K_RIGHT]:  # в право 
        screen.blit(walk_right[player_anim_count], (player_x,player_y))
        if player_x < 500:
            player_x += player_speed

    else: # стоит 
        screen.blit(walk_stay[0], (player_x, player_y))

    if not is_jump:
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            is_jump = True 
    else:
        if jump_count >= -7:
            if jump_count > 0:
                player_y -= (jump_count ** 2 ) / 2 
            else: 
                player_y += (jump_count ** 2 ) / 2 
            jump_count -= 1 
        else:
            is_jump = False
            jump_count = 7 

    # --- АНИМАЦИЯ --- 
    if player_anim_count == 2: # тип листаются анимки и если 2 показало тип 0 1 2 потом сразу врубает 0 анимку 
        player_anim_count = 0 
    else:
        player_anim_count += 1 


    pygame.display.update()

    # --- ОБРАБОТКА СОБЫТИЙ ---  
    for event in pygame.event.get(): # крч кнопка ливнуть из игрі 
        if event.type == pygame.QUIT:
            running = False

    time.tick(10)

# Корректное закрытие игры вне цикла while
pygame.quit()