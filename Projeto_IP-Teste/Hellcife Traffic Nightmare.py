import pygame
from sys import exit
import os
import random

# Inicializa Pygame e configura o display e nome do jogo
pygame.init()
screen = pygame.display.set_mode((600, 900))
pygame.display.set_caption("Hellcife Traffic Nightmare")
clock = pygame.time.Clock()
fonte = pygame.font.Font(None, 36)

# Configura o diretorio de trabalho como o mesmo do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#carrega e formata fundo do menu
fundo_menu = pygame.transform.scale(pygame.image.load(os.path.join('graficos', 'fundo_menu.png')), (600, 900))
img_estrela = pygame.transform.scale(pygame.image.load(os.path.join('graficos', 'star.png')), (32, 32))
img_colisao = pygame.transform.scale(pygame.image.load(os.path.join('graficos', 'buraco.png')), (32, 32))
img_vida = pygame.transform.scale(pygame.image.load(os.path.join('graficos', 'heart.png')), (32, 32))

# Carrega e formata a imagem de fundo
background = pygame.image.load(os.path.join('graficos', 'background.png'))
background = pygame.transform.scale(background, (600, 900*2))
fundo_pos_y = 0
fundo_pos_y2 = -900
vel_back = 7
#classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join('graficos', 'clio_1.6.png')).convert_alpha(), (110, 160))
        self.rect = self.image.get_rect(bottomleft =(300, 850))
        self.mask = pygame.mask.from_surface(self.image)
        self.vel = 5
    
    def player_input(self): #controles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 90:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT] and self.rect.right < 510:
            self.rect.x += self.vel
    
    def update(self):
        self.player_input()

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, escala, caminho, vel, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(caminho).convert_alpha(), escala)
        self.rect = self.image.get_rect(bottomleft =(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = vel
    
    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > 900:
            self.kill()

class Carros(Obstaculo):
    def __init__(self, tipo, x, y):
        if tipo == 'kwid':
            super().__init__((100, 120), os.path.join('graficos', 'kwid.png'), 5, x+10, y)
        elif tipo == 'Uno':
            super().__init__((80, 110), os.path.join('graficos', 'Uno.png'), 4, x+10, y) 
        elif tipo == 'Polo':
            super().__init__((90, 110), os.path.join('graficos', 'Polo.png'), 4, x, y)

class Bus(Obstaculo):
    def __init__(self, tipo, x, y):
        if tipo == 'amarelo':
            super().__init__((140, 300), os.path.join('graficos', 'amarelinho.png'), 6, x, y)
        elif tipo == 'azul':
            super().__init__((140, 300), os.path.join('graficos', 'azulao.png'), 6, x, y)
class Buraco(Obstaculo):
    def __init__ (self, x, y):
        super().__init__((70, 100), os.path.join('graficos', 'buraco.png'), 7, x, y)
        
class Coletaveis(Obstaculo):
    def __init__(self, tipo, x, y):
        self.tipo = tipo
        if tipo == "Coração":
            super().__init__((40, 40), os.path.join('graficos', 'heart.png'), 5, x+15, y)
        elif tipo == "Estrela":
            super().__init__((50, 50), os.path.join('graficos', 'star.png'), 5, x+10, y)

# criação de variaveis  e grupos necesária antes do inicio do loop
player = pygame.sprite.GroupSingle()
player.add(Player())

FAIXAS = [100, 200, 300, 400]
TIPOS_OB = {'Carros': ["kwid", "Uno", "Polo"], 'Bus': ["amarelo", "azul"], 'Buraco': "buraco", 'Coletaveis': ["Coração", "Estrela"] }
obs_ativos = pygame.sprite.Group()
spawn_timer = 0
spawn_delay = 30
ultima_faixa = None
vidas = 3
vidas_coletadas = 0
estrelas_coletadas = 0
cont_colisoes = 0
pont_final = 0
#função de colisões com objetos
def colisao_obstaculos():
    player_sprite = player.sprite
    global vidas, vidas_coletadas, estrelas_coletadas, estado, cont_colisoes, pont_final
    
    # Cria máscaras de colisão que contornam os pixeis da supeficie
    player_mask = pygame.mask.from_surface(player_sprite.image)
    
    for obstaculo in obs_ativos:
        obstaculo_mask = pygame.mask.from_surface(obstaculo.image)
        
        # Calcula o offset entre os sprites
        offset_x = obstaculo.rect.left - player_sprite.rect.left
        offset_y = obstaculo.rect.top - player_sprite.rect.top
        
        # Verifica colisão 
        if player_mask.overlap(obstaculo_mask, (offset_x, offset_y)):
            if isinstance(obstaculo, Coletaveis):
                if obstaculo.tipo == "Coração":
                    if vidas < 3:
                        vidas += 1
                        vidas_coletadas += 1
                    obstaculo.kill()
                elif obstaculo.tipo == "Estrela":
                    estrelas_coletadas += 1
                    obstaculo.kill()
            else:
                vidas -= 1
                cont_colisoes += 1
                pont_final = pontuacao
                obstaculo.kill()
                if vidas == 0:
                    estado = "game over"

            
       
def score (stars): # calcula o score por ticks, A cada 1s, é dado 10 pontos
    global start_time
    pontos = (pygame.time.get_ticks() // 100) + (stars * 100) - (start_time // 100)
    return pontos
#aumenta a velocidade do jogo de acordo com  a pontuação, deixando mais dificil com o passar do tempo
def velocidade (pontos):
    if pontos < 500:
         clock.tick(60)
    else:
        fps = 60 + (pontos // 100)
        clock.tick(fps)

def hud ():
    hud_rect = pygame.Rect(0, 0, 600, 50)
    s = pygame.Surface((600, 70), pygame.SRCALPHA)
    s.fill((150, 200, 220, 0))  # Preto com 50% de transparência
    screen.blit(s, hud_rect)
    hud_coracao = pygame.transform.scale(pygame.image.load(os.path.join("graficos", "heart.png")).convert_alpha(), (35, 35))
    hud_estrela = pygame.transform.scale(pygame.image.load(os.path.join("graficos", "star.png")).convert_alpha(), (40, 40))
    for i in range(vidas):
        screen.blit(hud_coracao, (20 + i * 40, 20))
    screen.blit(hud_estrela, (500, 20))
    screen.blit(fonte.render(str(pontuacao), True, (255, 255, 0)), (540, 30))                                                                                                          
                                                                   
start_time = 0                                                                                                        
estado = "menu"

def desenha_txt(texto, fonte, cor_texto, cor_sombra, posicao, deslocamento=(2, 2)):
    sombra = fonte.render(texto, True, cor_sombra)
    texto_principal = fonte.render(texto, True, cor_texto)
    screen.blit(sombra, (posicao[0] + deslocamento[0], posicao[1] + deslocamento[1]))
    screen.blit(texto_principal, posicao)

def gameover():
    global estado, start_time, vidas, vidas_coletadas, estrelas_coletadas, cont_colisoes, pontuacao, pont_final
    fonte_gameover = pygame.font.Font(None, 39)
    fundo_gameover = pygame.transform.scale(pygame.image.load(os.path.join('graficos', 'fundo_gameover.png')), (600, 900))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            vidas = 3
            pontuacao, vidas_coletadas, estrelas_coletadas, cont_colisoes = 0, 0, 0, 0
            start_time = pygame.time.get_ticks()
            return "jogo"

    screen.blit(fundo_gameover, (0, 0))

    # Quadrado central (tipo caixa de diálogo)
    pygame.draw.rect(screen, (5, 5, 39), (150, 400, 300, 170), border_radius=7)
    pygame.draw.rect(screen, (0, 0, 0), (150, 400, 300, 170), 5, border_radius=7)

    # Textos
    # Posições fixas
    icone_x = 170
    texto_x = 210

    # Y fixos por linha
    y_estrela = 430
    y_colisao = 470
    y_vida = 510

    screen.blit(img_estrela, (icone_x, y_estrela))
    screen.blit(img_colisao, (icone_x, y_colisao))
    screen.blit(img_vida, (icone_x, y_vida))
    desenha_txt("GAME OVER", fonte_gameover, (200, 0, 0), (0, 0, 0), (220, 300))
    desenha_txt(f"Pontuação: {pont_final}", fonte, (255, 255, 255), (0, 0, 0), (150, 370))
    desenha_txt(f"Estrelas: {estrelas_coletadas}", fonte, (255, 255, 255), (0, 0, 0), (texto_x, y_estrela))
    desenha_txt(f"Colisões: {cont_colisoes}", fonte, (255, 255, 255), (0, 0, 0), (texto_x, y_colisao))
    desenha_txt(f"Vidas coletadas: {vidas_coletadas}", fonte, (255, 255, 255), (0, 0, 0), (texto_x, y_vida))
    desenha_txt("Pressione qualquer tecla para reiniciar", fonte, (255, 255, 60), (0, 0, 0), (90, 750))

    pygame.display.update()
    clock.tick(60)

def menu():
    global vidas, pontuacao, vidas_coletadas, estrelas_coletadas, start_time, cont_colisoes
    vidas = 3
    pontuacao, vidas_coletadas, estrelas_coletadas, cont_colisoes = 0, 0, 0, 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            start_time = pygame.time.get_ticks()
            return "jogo"
    
    # Renderização do menu (fora do for, acontece sempre)
    screen.blit(fundo_menu, (0, 0))
    desenha_txt("Pressione qualquer tecla para começar", fonte, (255, 255, 60), (0, 0, 0), (90, 750))
    pygame.display.update()
    clock.tick(60)
    return "menu"
pontuacao = 0
restart_time = 0
running = True    
#game loop
while running:
    if estado == "menu":
        estado = menu()
    elif estado == "game over":
        novo_estado = gameover()
        if novo_estado is not None:
            estado = novo_estado
    elif estado == "jogo":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Update do player e do fundo
        player.update()
        fundo_pos_y += vel_back
        fundo_pos_y2 += vel_back

        # Sistema de spawn de obstaculos
        spawn_timer += 1
        if spawn_timer >= spawn_delay and len(obs_ativos) < 4:
            spawn_timer = 0
            tipo_obstaculo = random.choices(["Carros", "Bus", "Buraco", "Coletaveis"], weights=[50, 20, 20, 10], k=1)[0]
            
            # Seleção de faixa que evita repetição
            faixas_disponiveis = FAIXAS.copy()
            if ultima_faixa is not None and len(faixas_disponiveis) > 1:
                faixas_disponiveis.remove(ultima_faixa)
            
            faixa = random.choice(faixas_disponiveis)
            ultima_faixa = faixa
            
            if tipo_obstaculo == "Carros":
                subtipo = random.choice(TIPOS_OB['Carros'])
                novo_OBS = Carros(subtipo, faixa, -100)
            elif tipo_obstaculo == "Bus":
                subtipo = random.choice(TIPOS_OB['Bus'])
                novo_OBS = Bus(subtipo, faixa-15, -100)
            elif tipo_obstaculo == "Buraco":
                novo_OBS = Buraco(faixa+15, -100)
            elif tipo_obstaculo == "Coletaveis":
                if vidas >= 3:
                    subtipo = "Estrela"
                else:
                    subtipo = random.choice(TIPOS_OB['Coletaveis'])
                novo_OBS = Coletaveis(subtipo, faixa+20, -100)                                                                                                  
            
            obs_ativos.add(novo_OBS)

        # Reseta o background para cuntinuidade do efeito de paralax
        if fundo_pos_y > 900:
            fundo_pos_y = fundo_pos_y2 - 900
        if fundo_pos_y2 > 900:
            fundo_pos_y2 = fundo_pos_y - 900
        
        # Draw todas as superficies
        screen.blit(background, (0, fundo_pos_y))
        screen.blit(background, (0, fundo_pos_y2))
        obs_ativos.update()
        player.draw(screen)
        obs_ativos.draw(screen)
        hud()
        pontuacao = score(estrelas_coletadas)
    

        colisao_obstaculos()
        pygame.display.update()
        velocidade (pontuacao)