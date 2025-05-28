import pygame
import random

# Inicializa pygame e mixer de áudio para sons
pygame.init()
pygame.mixer.init()

pygame.key.set_repeat(0)

# Constantes e variáveis principais do jogo
NADA = 1
dificuldadedojogo = 1
maxscore = 0

# Boost (dash) parâmetros
DASH_VELOCIDADE_MULTIPLICADOR = 1.5
DASH_DURACAO_MS = 2000  # duração do dash em milissegundos
DASH_COOLDOWN_MS = 5000  # cooldown entre dashes

dash = 1.0
permissao_dash = True
invencibilidade = False
tempo_ultimo_dash = -DASH_COOLDOWN_MS  # inicializado para permitir dash imediato

# Penalidade cone
cone_penalidade_ativo = False
cone_penalidade_timer = 0
CONE_PENALIDADE_DURACAO_MS = 3000  # 3 segundos

# Carrega músicas do menu e do jogo
musicamenu = pygame.mixer.Sound("Downloads2\\Audio-Musicas\\OMORI OST - 103 Gator Gambol.mp3")
musicajogo = pygame.mixer.Sound("Downloads2\\Audio-Musicas\\Deltarune Chapter 2 OST_ 35 - Knock You Down !!.mp3")

# Flags para controlar estados das telas e pausa
menuactive = True
tutorialactive = False
dificuldadeactive = False
gameactive = False
paused = False  # Controla pausa no jogo

# Variáveis para tempo, pontuação e fonte de texto
ms_total = 0
second = 0
score = 0
score_timer = 0
fonte = pygame.font.SysFont(None, 36)  # Fonte para exibir pontuação

# Configura o clock para manter o jogo a 60 FPS
clock = pygame.time.Clock()

# Carrega e redimensiona imagens dos botões do menu
botao_menu_jogo = pygame.image.load("Downloads2\\Images-Menus\\Botao_Jogar.png")
botao_menu_jogo = pygame.transform.scale(botao_menu_jogo, (200, 80))

botao_menu_tutorial = pygame.image.load("Downloads2\\Images-Menus\\Botao_Tutorial.png")
botao_menu_tutorial = pygame.transform.scale(botao_menu_tutorial, (200, 80))

botao_dificuldade_easy = pygame.image.load("Downloads2\\Images-Menus\\Botao_Dificuldade_EasyV1.png")
botao_dificuldade_easy = pygame.transform.scale(botao_dificuldade_easy, (256, 256))

botao_dificuldade_hard = pygame.image.load("Downloads2\\Images-Menus\\Botao_Dificuldade_HardV1.png")
botao_dificuldade_hard = pygame.transform.scale(botao_dificuldade_hard, (256, 256))

# Easter egg: imagem do mago
mago_eastergg = pygame.image.load("Downloads2\\Images-Sprites\\The Mage (IDK).png")
mago_eastergg = pygame.transform.scale(mago_eastergg, (128, 128))

# Carrega e ajusta imagens de planos de fundo
backgroundsize = (1024, 512)
menu = pygame.image.load("Downloads2\\Images-Menus\\Overdrift_Menu.png")
menu = pygame.transform.scale(menu, backgroundsize)

mapa = pygame.image.load("Downloads2\\Images-Menus\\Overdriftmap_VF.png")
mapa = pygame.transform.scale(mapa, backgroundsize)

dificuldade = pygame.image.load("Downloads2\\Images-Menus\\Overdrift_dificulty_V0.png")
dificuldade = pygame.transform.scale(dificuldade, backgroundsize)

tutorial = pygame.image.load("Downloads2\\Images-Menus\\menu_question.png")
tutorial = pygame.transform.scale(tutorial, backgroundsize)

# Carrega sprites dos veículos e explosão, redimensionando conforme necessário
carro_mc = pygame.image.load("Downloads2\\Images-Sprites\\Carro_MC_V2.png")
carro_mc = pygame.transform.scale(carro_mc, (36, 54))

carro_obstaculo_ciano = pygame.image.load("Downloads2\\Images-Sprites\\Carro_Obstaculo_(Ciano).png")
carro_obstaculo_ciano = pygame.transform.scale(carro_obstaculo_ciano, (28, 46))
carro_obstaculo_ciano = pygame.transform.flip(carro_obstaculo_ciano, False, True)  # Espelha verticalmente

onibus_obstaculo_azul = pygame.image.load("Downloads2\\Images-Sprites\\Onibus_Obstaculo(Azul).png")
onibus_obstaculo_azul = pygame.transform.scale(onibus_obstaculo_azul, (44, 108))

explosao = pygame.image.load("Downloads2\\Images-Sprites\\Explosão_derrota.png")
explosao = pygame.transform.scale(explosao, (128, 128))

bolha_invencibilidade = pygame.image.load("Downloads2\\Images-Sprites\\Bolha_Invincibilidade.png")
bolha_invencibilidade = pygame.transform.scale(bolha_invencibilidade, (75, 75))

powerup_token = pygame.image.load("Downloads2\\Images-Sprites\\EXP_Token.png")
powerup_token = pygame.transform.scale(powerup_token, (36, 36))  # Ajuste tamanho se quiser

# Sprite do cone
obstaculo_cone = pygame.image.load("Downloads2\\Images-Sprites\\Obstaculo_Cone.png")
obstaculo_cone = pygame.transform.scale(obstaculo_cone, (28, 46))

# Configura tela do jogo
largura_tela = 1024
altura_tela = 512
display_surface = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_icon(carro_mc)  # Ícone da janela
pygame.display.set_caption('OverDrift.exe')

# Função para reiniciar o jogo, posicionar obstáculos e resetar pontuação
def resetar_jogo():
    global carro_rect, obstaculos, musicajatocando, score, score_timer, maxscore
    score = 0
    score_timer = 0
    carro_rect = carro_mc.get_rect(center=(512, 400))
    obstaculos = []
    for _ in range(10 * dificuldadedojogo):
        tipo = random.choice(["carro", "onibus", "cone"])
        if tipo == "carro":
            obstaculo = carro_obstaculo_ciano.get_rect(topleft=(random.randint(0, largura_tela - 64), random.randint(-600, -64)))
        elif tipo == "onibus":
            obstaculo = onibus_obstaculo_azul.get_rect(topleft=(random.randint(0, largura_tela - 64), random.randint(-600, -128)))
        else:  # cone
            obstaculo = obstaculo_cone.get_rect(topleft=(random.randint(0, largura_tela - 64), random.randint(-600, -64)))
        obstaculos.append((tipo, obstaculo))
    musicajatocando = False

resetar_jogo()

# Variáveis para controle de estado do dash
dash_ativo = False
dash_timer = 0

# Variáveis controle power-up
powerups = []
MAX_POWERUPS = 1
POWERUP_SPAWN_INTERVAL_MS = 5000  # intervalo para spawnar powerup
powerup_spawn_timer = 0

# Loop principal do jogo
running = True
musicajatocando = False

while running:
    ms = clock.tick(60)  # Tempo em ms desde último frame
    ms_total += ms
    tecla = pygame.key.get_pressed()

    # Controla música conforme estado do jogo
    if not gameactive and not musicajatocando:
        pygame.mixer.stop()
        pygame.mixer.music.set_volume(0.0001)
        musicamenu.play(-1)
        musicajatocando = True
    elif gameactive and not musicajatocando:
        pygame.mixer.stop()
        musicajogo.play(-1)
        musicajatocando = True

    # Exibe telas conforme estado
    if menuactive:
        hitboxbotaomenujogo = botao_menu_jogo.get_rect(topleft=(250, 300))
        hitboxbotaomenututorial = botao_menu_tutorial.get_rect(topleft=(575, 300))
        display_surface.blit(menu, (0, 0))
        display_surface.blit(botao_menu_jogo, (250, 300))
        display_surface.blit(botao_menu_tutorial, (575, 300))
        texto_maxscore = fonte.render(f"Max Score: {maxscore}", True, (255, 255, 255))
        display_surface.blit(texto_maxscore, (10, 10))

    elif tutorialactive:
        display_surface.blit(tutorial, (0, 0))

    elif dificuldadeactive:
        hitboxbotaodificuldadeeasy = botao_dificuldade_easy.get_rect(topleft=(180, 210))
        hitboxbotaodificuldadehard = botao_dificuldade_hard.get_rect(topleft=(595, 210))
        display_surface.blit(dificuldade, (0, 0))
        display_surface.blit(botao_dificuldade_easy, (180, 210))
        display_surface.blit(botao_dificuldade_hard, (595, 210))
        if tecla[pygame.K_m] and tecla[pygame.K_a] and tecla[pygame.K_g]:
            display_surface.blit(mago_eastergg, (largura_tela - 128, altura_tela - 128))
            pygame.display.set_caption('Mago da internet! Parabéns em achar um easter egg!')

    elif gameactive and not paused:
        display_surface.blit(mapa, (0, 0))

        # Atualiza penalidade cone
        if cone_penalidade_ativo:
            cone_penalidade_timer -= ms
            if cone_penalidade_timer <= 0:
                cone_penalidade_ativo = False

        # Calcula velocidade final com dash e penalidade cone
        velocidade = 7 * dash
        if cone_penalidade_ativo:
            velocidade *= 0.5

        second += ms / 1000
        score_timer += ms
        if score_timer >= 10:
            score += 1 * dificuldadedojogo
            score_timer = 0
        if score >= maxscore:
            maxscore = score

        if dash_ativo:
            dash_timer -= ms
            if dash_timer <= 0:
                dash_ativo = False
                dash = 1.0
                invencibilidade = False
            bolha_pos = (carro_rect.centerx - bolha_invencibilidade.get_width() // 2,
                         carro_rect.centery - bolha_invencibilidade.get_height() // 2)
            display_surface.blit(bolha_invencibilidade, bolha_pos)
        else:
            if not permissao_dash and (ms_total - tempo_ultimo_dash) >= DASH_COOLDOWN_MS:
                permissao_dash = True
            if permissao_dash:
                texto_boost = fonte.render("Aperte o Shift para ativar o boost!", True, (255, 255, 255))
                display_surface.blit(texto_boost, (10, altura_tela - 40))
                if (tecla[pygame.K_LSHIFT] or tecla[pygame.K_RSHIFT]) and not dash_ativo:
                    dash_ativo = True
                    dash_timer = DASH_DURACAO_MS
                    permissao_dash = False
                    tempo_ultimo_dash = ms_total
                    dash = DASH_VELOCIDADE_MULTIPLICADOR
                    invencibilidade = True

        if tecla[pygame.K_w]: carro_rect.y -= velocidade
        if tecla[pygame.K_s]: carro_rect.y += velocidade
        if tecla[pygame.K_a]: carro_rect.x -= velocidade
        if tecla[pygame.K_d]: carro_rect.x += velocidade
        carro_rect.clamp_ip(display_surface.get_rect())

        display_surface.blit(carro_mc, carro_rect.topleft)

        # Atualiza posição, desenha obstáculos e verifica colisões
        for i, (tipo, obstaculo) in enumerate(obstaculos):
            obstaculo.y += 5
            if tipo == "carro":
                display_surface.blit(carro_obstaculo_ciano, obstaculo.topleft)
            elif tipo == "onibus":
                display_surface.blit(onibus_obstaculo_azul, obstaculo.topleft)
            elif tipo == "cone":
                display_surface.blit(obstaculo_cone, obstaculo.topleft)

            if carro_rect.colliderect(obstaculo) and not dash_ativo:
                if tipo == "cone":
                    cone_penalidade_ativo = True
                    cone_penalidade_timer = CONE_PENALIDADE_DURACAO_MS
                    obstaculo.y = altura_tela + 100  # Remove cone temporariamente
                else:
                    display_surface.blit(explosao, carro_rect.topleft)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    gameactive = False
                    menuactive = True
                    resetar_jogo()
                    break

            if obstaculo.top > altura_tela:
                obstaculo.y = random.randint(-600, -64)
                obstaculo.x = random.randint(0, largura_tela - 64)

            obstaculos[i] = (tipo, obstaculo)

        #Gerar powerup
        powerup_spawn_timer += ms
        if powerup_spawn_timer >= POWERUP_SPAWN_INTERVAL_MS:
            if len(powerups) < MAX_POWERUPS:
                largura, altura = powerup_token.get_size()
                x = random.randint(0, largura_tela - largura)
                y = random.randint(0, altura_tela - altura)
                novo_rect = pygame.Rect(x, y, largura, altura)
                powerups.append(("bola_xp", novo_rect))
            powerup_spawn_timer = 0
        
        # Atualiza posição, desenha powerups e verifica colisões
        for i, (tipo, powerup_rect) in enumerate(powerups):
            if tipo == "bola_xp":
                display_surface.blit(powerup_token, powerup_rect.topleft)

            # Verifica colisão com o jogador
            if carro_rect.colliderect(powerup_rect):
                score += 500
                powerups.pop(i)  # ou del powerups[i]
                break

        texto_score = fonte.render(f"Score: {score}", True, (255, 255, 255))
        display_surface.blit(texto_score, (10, 10))

    else:
        texto_pause = fonte.render("PAUSADO - Aperte P ou ESC para voltar", True, (255, 255, 255))
        display_surface.blit(texto_pause, (260, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if tutorialactive:
                menuactive = True
                tutorialactive = False
            if dificuldadeactive and event.key == pygame.K_ESCAPE:
                menuactive = True
                dificuldadeactive = False
            if gameactive and event.key in [pygame.K_p, pygame.K_ESCAPE]:
                paused = not paused
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menuactive:
                if hitboxbotaomenujogo.collidepoint(event.pos):
                    menuactive = False
                    dificuldadeactive = True
                elif hitboxbotaomenututorial.collidepoint(event.pos):
                    menuactive = False
                    tutorialactive = True
            elif dificuldadeactive:
                if hitboxbotaodificuldadeeasy.collidepoint(event.pos):
                    gameactive = True
                    dificuldadeactive = False
                    dificuldadedojogo = 1
                    resetar_jogo()
                elif hitboxbotaodificuldadehard.collidepoint(event.pos):
                    gameactive = True
                    dificuldadeactive = False
                    dificuldadedojogo = 2
                    resetar_jogo()

    pygame.display.update()
