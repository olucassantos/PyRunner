import pygame
from sys import exit
from random import randint

def display_score():
    score = pygame.time.get_ticks() - start_time

    color = (64, 64, 64)
    if score > 35000:
        color = '#FF6347'
    elif score > 60000:
        color = '#FF4500'
    elif score > 90000:
        color = '#FF0000'

    score_surf = pixel_type_font.render(f'Pontos: {score}', False, color)
    score_rect = score_surf.get_rect(center = (400, 50))
    tela.blit(score_surf, score_rect)
    return score

def obstacle_movement(obstacle_list):
    # Checa se há obstáculos na lista
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: tela.blit(snail_surf, obstacle_rect)
            else: tela.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []
    
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False

    return True

# Inicializa o pygame
pygame.init()

# Cria a tela
tela = pygame.display.set_mode((800, 400))

# Define o título da janela
pygame.display.set_caption('Runner')

# Cria o relógio para controlar o FPS
relogio = pygame.time.Clock()

# Cria as fontes do jogo
pixel_type_font = pygame.font.Font('font/Pixeltype.ttf', 50)

game_active = False

start_time = 0

score = 0

# Carrega as imagens como superfícies
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Obstáculos
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

#Player
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_retangle = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0 

# Tela de Início
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = pixel_type_font.render('Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

instructions_text = pixel_type_font.render('Pressione espaco para jogar', False, (111, 196, 169))
instructions_rect = instructions_text.get_rect(center = (400, 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # Faz o jogador pular ao clicar nele
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_retangle.collidepoint(event.pos) and player_retangle.bottom >= 300:
                    player_gravity = -20

            # Faz o jogador pular ao apertar espaço
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_retangle.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))

    if game_active:
        # Desenha as superfícies na tela
        tela.blit(sky_surf, (0, 0))
        tela.blit(ground_surf, (0, 300))

        score = display_score()

        # Desenha o jogador
        player_gravity += 1
        player_retangle.y += player_gravity
        if player_retangle.bottom >= 300: player_retangle.bottom = 300

        tela.blit(player_surf, player_retangle)

        # Movimentos dos Obstáculos
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collisions
        game_active = collisions(player_retangle, obstacle_rect_list)
    else:
        tela.fill((94, 129, 162))
        tela.blit(player_stand, player_stand_rect)

        # Reseta o score
        obstacle_rect_list.clear()

        # Reposiciona o jogador
        player_retangle.midbottom = (80, 300)

        #limpa a gravidade
        player_gravity = 0

        score_text = pixel_type_font.render(f'Seus pontos: {score}', False, (111, 196, 169))
        score_text_rect = score_text.get_rect(center = (400, 365))

        tela.blit(game_name, game_name_rect)

        tela.blit(instructions_text, instructions_rect)

        if score > 0:
            tela.blit(score_text, score_text_rect)

    # Atualiza a tela
    pygame.display.update()

    # Define o FPS (quantas vezes o loop será executado por segundo)
    relogio.tick(60)