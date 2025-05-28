def spawn_powerup():
    if len(powerups) >= POWERUP_MAX:
        return
    w, h = powerup_token.get_size()
    tentativas = 0
    while tentativas < 100:
        x = random.randint(0, largura_tela - w)
        y = random.randint(0, altura_tela - h)
        novo_rect = pygame.Rect(x, y, w, h)

        colisao = False
        # Evita spawnar em cima do carro e dos obstáculos
        if carro_rect.colliderect(novo_rect):
            colisao = True
        for _, obst_rect in obstaculos:
            if obst_rect.colliderect(novo_rect):
                colisao = True
                break

        # Evita spawnar em cima de outro powerup
        for _, pu_rect in powerups:
            if pu_rect.colliderect(novo_rect):
                colisao = True
                break

        if not colisao:
            powerups.append(("xp_bola", novo_rect))
            break
        tentativas += 1
