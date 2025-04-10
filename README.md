Nome do Jogo: Hellcife Traffic Nightmare

Desenvolvedores: hgfs, ktn, pgsa2

Ideia: O objetivo deste projeto foi desenvolver um minigame arcade em Python utilizando a biblioteca Pygame, no qual o jogador deve desviar de obstáculos no trânsito caótico de uma cidade fictícia chamada Hellcife. O jogador deve sobreviver o maior tempo possível enquanto coleta itens e evita colisões.

Descrição: O jogador controla um carro que se move horizontalmente entre faixas de uma rodovia. Durante o jogo, diversos obstáculos surgem aleatoriamente e se movimentam na direção do jogador. Além dos obstáculos, há também itens coletáveis.
Coletáveis: O coração aparece com menor frequência e somente se o jogador estiver com menos de 3 vidas. Ao coletar adiciona +1 vida (limitado a 3). A estrela aparece com uma frequência um pouco maior e caso coletada adiciona +100 pontos a pontuação total.

Obstáculos: Carros: Colisão reduz 1 vida. Ônibus: Tamanho maior, mesma penalidade. Buraco: Também reduz 1 vida.

Interface: A interface mostra a quantidade de vidas restantes usando ícones de coração. A pontuação é exibida ao lado do ícone de estrela no topo da tela.

Divisão de tarefas: pgsa2 : ficou responsável pelos modelos dos carros e do cenário, dos movimentos e das interações, também fez os designs e modelos do jogo.

hgfs: responsável pelos coletáveis, como a frequência que eles aparecem e o limite que podem aparecer, além da interação entre personagem e coletáveis

ktn: responsável pela exibição dos coletáveis no final do jogo, aperfeiçoamento de alguns modelos do cenário e a tela final de game over.

Desafios: Aprender a utilizar pygame e orientação de objetos, e utilizar isso em um curto período de tempo, enfrentamos pequenos desafios também na divisão de tarefas que ficou um pouco confusa no processo. 

Lições aprendidas: 

 
