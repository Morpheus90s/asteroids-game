import pygame
import random
import time

tempo_inicial = time.time()

pygame.init()

WIDTH, HEIGHT = 660, 660
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Taca Poze Asteroids")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (50, 50))
player2_img = pygame.image.load('player2.png')
player2_img = pygame.transform.scale(player2_img, (50, 50))
player3_img = pygame.image.load('player3.png')
player3_img = pygame.transform.scale(player3_img, (50, 50))
asteroid_img = pygame.image.load('asteroid.png')
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

def carregar_mapa(filename):
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]
    
def criar_asteroides(mapa):
    for row_index, row in enumerate(mapa):
        for col_index, col in enumerate(row):
            if col == 'A':
                asteroid_rect = asteroid_img.get_rect()
                asteroid_rect.x = col_index * 50  
                asteroid_rect.y = row_index * 50
                asteroid_speed = random.randint(asteroid_speed_min, asteroid_speed_max)
                asteroids.append({'rect': asteroid_rect, 'speed': asteroid_speed})
mapa = carregar_mapa('mapa.txt')

pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

music_level_2 = 'musica2.mp3'
music_level_3 = 'musica3.mp3'

player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
player_speed = 5
player_life = 200
score = 0

bg_y = 0
bg_speed = 2
bg_img = pygame.image.load('cenario.png').convert()
bg_img2 = pygame.image.load('cenario2.png').convert()
bg_img3 = pygame.image.load('cenario3.png').convert()

laser_speed = 12
lasers = []

asteroids = []
asteroid_spawn_rate = 100
next_asteroid_spawn = 0

asteroid_speed_min = 3
asteroid_speed_max = 7

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 60)

show_bug_img = False
bug_timer = pygame.time.get_ticks()

level = 1
show_level_timer = 0
show_level_duration = 5000
current_level = 0

def draw_border():
    pygame.draw.rect(screen, WHITE, (0, 0, 10, 10))                   
    pygame.draw.rect(screen, WHITE, (WIDTH - 10, 0, 10, 10))          
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 10, 10, 10))         
    pygame.draw.rect(screen, WHITE, (WIDTH - 10, HEIGHT - 10, 10, 10))

def reset_game():
    global player_life, score, asteroids, lasers, game_over, level, restart_requested, game_paused
    
    player_life = 200
    score = 0
    asteroids.clear()
    lasers.clear()
    game_over = False
    level = 1
    restart_requested = False
    game_paused = False
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(-1)

restart_requested = False
game_paused = False

clock = pygame.time.Clock()
running = True
game_over = False
while running:
    screen.fill(BLACK)
    
    draw_border()

    if show_level_timer > 0 and current_level != 0:
        level_text = big_font.render(f'Nível {current_level}', True, WHITE)
        text_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(level_text, text_rect)
        show_level_timer -= clock.get_time()
    elif game_over:
        game_over_text = big_font.render(game_result, True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

        restart_text = font.render("Aperte espaço para recomeçar", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)
    else:
        current_level = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_paused:
            laser_rect = pygame.Rect(player_rect.centerx - 2, player_rect.top, 4, 20)
            lasers.append({'rect': laser_rect})

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not game_paused:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and not game_paused:
        player_rect.y += player_speed
    if keys[pygame.K_LEFT] and not game_paused:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and not game_paused:
        player_rect.x += player_speed

    player_rect.x = max(min(player_rect.x, WIDTH - 50), 0)
    player_rect.y = max(min(player_rect.y, HEIGHT - 50), 0)

    if level == 1:
        screen.blit(bg_img, (0, bg_y))
        screen.blit(bg_img, (0, bg_y - HEIGHT))
    elif level == 2:
        screen.blit(bg_img2, (0, bg_y))
        screen.blit(bg_img2, (0, bg_y - HEIGHT))
    elif level == 3:
        screen.blit(bg_img3, (0, bg_y))
        screen.blit(bg_img3, (0, bg_y - HEIGHT))
    bg_y += bg_speed
    if bg_y >= HEIGHT:
        bg_y = 0
        
    if score >= 200 and level == 1 and not game_paused:
        player_rect = player2_img.get_rect(center=player_rect.center)
        level = 2
        current_level = 2
        show_level_timer = show_level_duration
        asteroid_spawn_rate = 150
        pygame.mixer.music.load(music_level_2)
        pygame.mixer.music.play(-1)
    elif score >= 400 and level == 2 and not game_paused:
        player_rect = player3_img.get_rect(center=player_rect.center)
        level = 3
        current_level = 3
        show_level_timer = show_level_duration
        pygame.mixer.music.load(music_level_3)
        pygame.mixer.music.play(-1)
        asteroid_spawn_rate = 100

    if pygame.time.get_ticks() > next_asteroid_spawn and not game_paused:
        next_asteroid_spawn = pygame.time.get_ticks() + asteroid_spawn_rate
        asteroid_rect = asteroid_img.get_rect()
        asteroid_rect.x = random.randint(0, WIDTH - 50)
        asteroid_rect.y = random.randint(-50, 0)
        asteroid_speed = random.randint(asteroid_speed_min, asteroid_speed_max)
        asteroids.append({'rect': asteroid_rect, 'speed': asteroid_speed})
    for asteroid in asteroids[:]:
        if player_rect.colliderect(asteroid['rect']):
            player_life -= 50
            asteroids.remove(asteroid)

    for asteroid in asteroids:
        asteroid['rect'].y += asteroid['speed']
        asteroid['rect'].x += random.randint(-1, 1)
        screen.blit(asteroid_img, asteroid['rect'])

    for laser in lasers[:]:
        laser['rect'].y -= laser_speed
        pygame.draw.rect(screen, WHITE, laser['rect'])
        for asteroid in asteroids[:]:
            if laser['rect'].colliderect(asteroid['rect']):
                score += 1 # Se estiver demorando muito, coloque 'score += 10', você estará ganhando pontos em 10 em 10
                lasers.remove(laser)
                asteroids.remove(asteroid)
                break

    if level == 1:
        screen.blit(player_img, player_rect)
    elif level == 2:
        screen.blit(player2_img, player_rect)
    elif level == 3:
        screen.blit(player3_img, player_rect)

    life_text = font.render(f'Life: {player_life}', True, RED)
    screen.blit(life_text, (10, 10))

    score_text = font.render(f'Score: {score}', True, RED)
    screen.blit(score_text, (WIDTH - 120, 10))

    if player_life <= 0 and not game_paused:
        game_over = True
        game_result = "Derrota"
        game_paused = True

    elif score >= 600 and not game_paused:
        game_over = True
        game_result = "Vitória"
        game_paused = True

        tempo_vitoria = time.time() - tempo_inicial
        minutos = int(tempo_vitoria // 60)
        segundos = int(tempo_vitoria % 60)

        tempo_formatado = f"{minutos:02d}:{segundos:02d}"

        with open('resultado.txt', 'w') as file:
            file.write(f"Vitória\nTempo de vitória: {tempo_formatado} segundos")

    if game_over and not restart_requested and game_paused:
        game_over_text = big_font.render(game_result, True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

        restart_text = font.render("Aperte espaço para recomeçar", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            restart_requested = True
    elif restart_requested:
        reset_game()
        restart_requested = False
        game_paused = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
