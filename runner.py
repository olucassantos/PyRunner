import pygame
from sys import exit

def display_score():
    current_time = pygame.time.get_ticks() - start_time

    color = (64, 64, 64)
    if current_time > 60000:
        color = '#FF6347'
    elif current_time > 90000:
        color = '#FF4500'
    elif current_time > 120000:
        color = '#FF0000'

    score_surf = pixel_type_font.render(f'Pontos: {current_time}', False, color)
    score_rect = score_surf.get_rect(center = (400, 50))
    tela.blit(score_surf, score_rect)

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

game_active = True

start_time = 0

# Carrega as imagens como superfícies
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_retangle = snail_surf.get_rect(midbottom = (600, 300))

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_retangle = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0 

# Tela de Início
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

titulo = pixel_type_font.render('Runner', False, (111, 196, 169))
titulo_rect = titulo.get_rect(center = (400, 80))

subtitulo = pixel_type_font.render('Pressione espaco para jogar', False, (111, 196, 169))
subtitulo_rect = subtitulo.get_rect(center = (400, 330))


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
                snail_retangle.left = 800
                start_time = pygame.time.get_ticks()

    if game_active:
        # Desenha as superfícies na tela
        tela.blit(sky_surf, (0, 0))
        tela.blit(ground_surf, (0, 300))

        display_score()
        
        # Movimenta o caracol para a esqueda
        snail_retangle.x -= 5
        if snail_retangle.right <= 0: snail_retangle.left = 800

        # Desenha o caracol
        tela.blit(snail_surf, snail_retangle)

        # Desenha o jogador
        player_gravity += 1
        player_retangle.y += player_gravity
        if player_retangle.bottom >= 300: player_retangle.bottom = 300

        tela.blit(player_surf, player_retangle)

        # Verifica se houve colisão entre o jogador e o caracol
        if player_retangle.colliderect(snail_retangle):
            game_active = False
    else:
        tela.fill((94, 129, 162))
        tela.blit(player_stand, player_stand_rect)

        tela.blit(titulo, titulo_rect)
        tela.blit(subtitulo, subtitulo_rect)

    # Atualiza a tela
    pygame.display.update()

    # Define o FPS (quantas vezes o loop será executado por segundo)
    relogio.tick(60)