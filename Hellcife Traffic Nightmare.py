import pygame
from sys import exit
import os
import random

# Inicializa Pygame e configura o display e nome do jogo
pygame.init()
screen = pygame.display.set_mode((600, 900))
pygame.display.set_caption("Hellcife Traffic Nightmare")
clock = pygame.time.Clock()

# Configura o diretorio de trabalho como o mesmo do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
            pygame.image.load(os.path.join('graficos', 'clio_1.6.png')).convert_alpha(), (100, 150))
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
            super().__init__((80, 120), os.path.join('graficos', 'kwid.png'), 5, x+10, y)
        elif tipo == 'Uno':
            super().__init__((80, 110), os.path.join('graficos', 'Uno.png'), 4, x+10, y) 
        elif tipo == 'Polo':
            super().__init__((90, 110), os.path.join('graficos', 'Polo.png'), 4, x, y)

class Bus(Obstaculo):
    def __init__(self, tipo, x, y):
        if tipo == 'amarelo':
            super().__init__((120, 300), os.path.join('graficos', 'amarelinho.png'), 6, x, y)
        elif tipo == 'azul':
            super().__init__((120, 300), os.path.join('graficos', 'azulao.png'), 6, x, y)
class Buraco(Obstaculo):
    def __init__ (self, x, y):
        super().__init__((70, 100), os.path.join('graficos', 'buraco.png'), 7, x, y)

# criação de variaveis  e grupos necesária antes do inicio do loop
player = pygame.sprite.GroupSingle()
player.add(Player())

FAIXAS = [100, 200, 300, 400]
TIPOS_OB = {'Carros': ["kwid", "Uno", "Polo"], 'Bus': ["amarelo", "azul"], 'Buraco': "buraco"}
obs_ativos = pygame.sprite.Group()
spawn_timer = 0
spawn_delay = 30
ultima_faixa = None
#função de colisões com objetos
def colisao_obstaculos():
    player_sprite = player.sprite
    
    # Cria máscaras de colisão que contornam os pixeis da supeficie
    player_mask = pygame.mask.from_surface(player_sprite.image)
    
    for obstaculo in obs_ativos:
        obstaculo_mask = pygame.mask.from_surface(obstaculo.image)
        
        # Calcula o offset entre os sprites
        offset_x = obstaculo.rect.left - player_sprite.rect.left
        offset_y = obstaculo.rect.top - player_sprite.rect.top
        
        # Verifica colisão 
        if player_mask.overlap(obstaculo_mask, (offset_x, offset_y)):
            print("Bateu num kwid kkkkkkkkkkkkkkkkk")
            obstaculo.kill()
       
#def score (): # calcula o score por ticks
# 
# 
#def velocidade (score):
#  


#game loop
running = True
while running:
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
        tipo_obstaculo = random.choices(["Carros", "Bus", "Buraco"], weights=[60, 20, 20], k=1)[0]
        
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
            novo_OBS = Bus(subtipo, faixa-10, -100)
        elif tipo_obstaculo == "Buraco":
            novo_OBS = Buraco(faixa+15, -100)
        
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

    colisao_obstaculos()
    pygame.display.update()
    clock.tick(60)
