

from quatro_em_linha_motor_45741 import novo_jogo
from quatro_em_linha_motor_45741 import ha_espaco
from quatro_em_linha_motor_45741 import jogar
from quatro_em_linha_motor_45741 import valor
from quatro_em_linha_motor_45741 import terminou
from quatro_em_linha_motor_45741 import quem_ganhou
from quatro_em_linha_motor_45741 import get_linha_vitoria
from quatro_em_linha_agente import jogada_agente

# importar o módulo pygame
# se a execução deste import em python 3 der algum erro é porque o pygame
# não está bem instalado
import pygame

# inicialização do módulo pygame
# o funcionamento do módulo pygame depende da placa gráfica, das
# fontes de texto disponíveis no sistema, etc. A inicialização do
# módulo define os recurssos a usar.
pygame.init()
pygame.display.set_caption('Connect 4 - Alice Fernandes Nº45741')
pygame.mixer.init(48000)

# criação de uma janela
LARGURA = 800
ALTURA  = 600
tamanho = (LARGURA, ALTURA)
janela  = pygame.display.set_mode(tamanho)

# número de imagens por segundo
frame_rate = 24
t = 0

# relógio para controlo do frame rate
clock = pygame.time.Clock()


logo = pygame.image.load("assets/logo.png")
lua = pygame.image.load("assets/lua.png")

peca_amarela = pygame.image.load("assets/a.png")
peca_vermelha = pygame.image.load("assets/v.png")
peca_dourada = pygame.image.load("assets/d.png")
peca_trasparente = pygame.image.load("assets/pt.png")
peca_metade = pygame.image.load("assets/d-metade.png")

tabuleiro = pygame.image.load("assets/t.png")
ficheiro_musica_jogo = "assets/music.mp3"
ficheiro_musica_ganhar = "assets/win.mp3"
ficheiro_musica_perder = "assets/lost.mp3"

playlist = (ficheiro_musica_jogo, ficheiro_musica_ganhar, ficheiro_musica_perder)
musica_jogo = 0
musica_ganhar = 1
musica_perder = 2

debounce = 0
debounce_max_frame = 5




# ecrãs 
ECRA_INICIAL = 1
ECRA_SELECAO_JOGO = 2
ECRA_SELECAO_CORES = 3
ECRA_SELECAO_ORDEM = 4
ECRA_JOGO          = 5
ECRA_FIM           = 6
# ecrã atual
ecra = ECRA_INICIAL

# eventos
fim             = False # porque o jogador não quer jogar mais ou porque fechou a janela
posicao_mouse_x = None
posicao_mouse_y = None
mouse_click     = False

# frame a desenha na janela
nova_frame = None

# escolhas do jogador 
cor_escolhida   = None
ordem_escolhida = None

# cores
AZUL     = (0, 0, 255)
BRANCO   = (255, 255, 255)
VERMELHO = (255, 0, 0)
AMARELO  = (255, 255, 0)
PRETO  = (0, 0, 0)

# texto a usar nos botões
texto_cor      = PRETO
texto_tamanho  = 18 # altura em pixels
fonte_ficheiro = "assets/font.ttf" # None = pygame default font (existe sempre em quaquer computador que tenha pygame)
texto_fonte    = pygame.font.Font(fonte_ficheiro, texto_tamanho) 

# cor de fundo
cor_fundo = PRETO

# jogo 4 em linha
jogo          = None
jogador       = None
cor_jogador_1 = None
cor_jogador_2 = None
musica_a_tocar = 0

# função auxiliar para debug
def print_ecra():
    if ecra == 1:
        print('ecra = ECRA_SELECAO_CORES')
    elif ecra == 2:
        print('ecra = ECRA_SELECAO_ORDEM')
    elif ecra == 3:
        print('ecra = ECRA_JOGO')
    else:
        print('ecrã inválido:', ecra)


def tocar_musica(index):
    '''
    Função para tocar musica
    Argumentos:
        index (int): Index da playlist para tocar
    '''
    global musica_a_tocar
    musica_a_tocar = index
    musica = playlist[index]
    
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play()

tocar_musica(musica_jogo)

# função auxiliar para debug
def print_eventos():
    print('eventos')
    print('fim = ', fim)
    print('posicao_mouse_x = ', posicao_mouse_x)
    print('posicao_mouse_y = ', posicao_mouse_y)
    print('mouse_click = ', mouse_click)

# função auxiliar para debug
def print_aux():
    print_ecra()
    print()
    print_eventos()
    print()

def processar_eventos_pygame():

    global fim
    global mouse_click
    global posicao_mouse_x
    global posicao_mouse_y

    mouse_click = False

    # ciclo para processar os eventos pygame
    for event in pygame.event.get():

        # evento fechar a janela gráfica
        if event.type == pygame.QUIT:
            fim = True

        # evento mouse click botão esquerdo (código = 1)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            mouse_click = True

    # obter a posição do mouse (independentemente dos eventos)
    (posicao_mouse_x, posicao_mouse_y) = pygame.mouse.get_pos()

def botao_texto(texto,centro, acao, cor = PRETO):
    global nova_frame
    resultado = False

    texto_surface     = texto_fonte.render(texto, True, cor)
    texto_rect        = texto_surface.get_rect()
    texto_rect.center = centro
    nova_frame.blit(texto_surface, texto_rect)
    largura = texto_rect.width
    altura  = texto_rect.height
    posicao_x = int(centro[0] - largura /2)
    posicao_y = int(centro[1] - altura/2)

    if (posicao_x < posicao_mouse_x < posicao_x + largura) and (posicao_y < posicao_mouse_y < posicao_y + altura):
        nova_frame.blit(peca_metade, (posicao_x - 30,posicao_y - 2))
        nova_frame.blit(peca_metade, ((posicao_x + largura) + 10,posicao_y - 2))
        if mouse_click == True:
            acao()

    return resultado

def get_centro(numero_linhas, numero_colunas, linha, coluna):
    '''Esta função server para dividir o ecrã num certo número de linhas e
    de colunas e obter a coordenada do centro do rectângulo na linha e
    coluna desejados.'''
    
    largura_colunas = LARGURA / numero_colunas
    centro_x = int((coluna - 1) * largura_colunas + largura_colunas / 2)

    altura_linhas = ALTURA / numero_linhas
    centro_y = int((linha - 1) * altura_linhas + altura_linhas / 2)

    return (centro_x, centro_y)

def get_centro_grelha(numero_linhas, numero_colunas, linha, coluna):

    largura_colunas = (LARGURA -  (LARGURA - 465)) / numero_colunas
    centro_x = int((coluna - 1) * largura_colunas + largura_colunas / 2)

    altura_linhas = (ALTURA - (ALTURA - 460)) / numero_linhas
    centro_y = int((linha - 1) * altura_linhas + altura_linhas / 2)

    return (centro_x + int((LARGURA - 464)/2),
            centro_y + int((ALTURA  - 518)/2))

def desenha_texto(texto, centro):

    texto_surface     = texto_fonte.render(texto, True, texto_cor)
    texto_rect        = texto_surface.get_rect()
    texto_rect.center = centro
    nova_frame.blit(texto_surface, texto_rect)

def desenha_texto_branco(texto, centro):

    texto_surface     = texto_fonte.render(texto, True, BRANCO)
    texto_rect        = texto_surface.get_rect()
    texto_rect.center = centro
    nova_frame.blit(texto_surface, texto_rect)

def accao_coin():

    global ecra

    # prosseguir para o próximo ecrã
    ecra = ECRA_SELECAO_JOGO

    #print_aux()

def accao_jogador_pc():

    global ecra

    # prosseguir para o próximo ecrã
    ecra = ECRA_SELECAO_CORES

    #print_aux()

def accao_botao_vermelhas():

    global cor_escolhida
    global ecra

    cor_escolhida = VERMELHO
    # prosseguir para o próximo ecrã
    ecra = ECRA_SELECAO_ORDEM

    #print_aux()

def accao_botao_amarelas():

    global cor_escolhida
    global ecra

    cor_escolhida = AMARELO
    # prosseguir para o próximo ecrã
    ecra = ECRA_SELECAO_ORDEM

    #print_aux()

def accao_botao_primeiro():

    global ordem_escolhida
    global ecra

    ordem_escolhida = 1
    comecar_jogo()

    # prosseguir para o próximo ecrã
    ecra = ECRA_JOGO

def accao_botao_segundo():

    global ordem_escolhida
    global ecra

    ordem_escolhida = 2
    comecar_jogo()

    # prosseguir para o próximo ecrã
    ecra = ECRA_JOGO

def acao_botao_sim():

    global ecra
    global musica_a_tocar

    if(musica_a_tocar != musica_jogo):
        tocar_musica(musica_jogo)

    comecar_jogo()
    ecra = ECRA_JOGO

def acao_botao_nao():
    global fim
    fim = True

def construir_frame_inicio():

    global nova_frame

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill(cor_fundo)

    frame_numero_linhas  = 6
    frame_numero_colunas = 3
    nova_frame.blit(lua, (0 ,0))
    nova_frame.blit(logo, (210,67))
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 5, 2)

    if(t % 40 >= 0 and t % 40 <= 20):
        botao_texto('INSERT COIN TO START', centro,accao_coin, PRETO)
    if mouse_click == True:
        accao_coin()
    
def construir_frame_selecao_jogo():

    global nova_frame

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill(cor_fundo)

    frame_numero_linhas  = 20
    frame_numero_colunas = 3
    nova_frame.blit(lua, (0 ,0))
    nova_frame.blit(logo, (210,67))
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 15, 2)
    botao_texto('PLAYER VS COMPUTER', centro,accao_jogador_pc)
    
    '''
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 17, 2)
    botao_texto('PLAYER   VS   PLAYER', centro,accao_jogador_pc)
    '''
    
def construir_frame_selecao_cores():

    global nova_frame
    global mouse_click
    global debounce
    global debounce_max_frame
    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)
    
    #Debounce
    if(debounce <= debounce_max_frame):
        mouse_click = False
        debounce = debounce + 1


    # cor de fundo
    nova_frame.fill(cor_fundo)

    frame_numero_linhas  = 20
    frame_numero_colunas = 3
    nova_frame.blit(lua, (0 ,0))
    nova_frame.blit(logo, (210,67))

    nova_frame.blit(logo, (210,67))
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 15, 2)
    botao_texto('Yellow Piece', centro,accao_botao_amarelas)

    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 17, 2)
    botao_texto('Red Piece', centro,accao_botao_vermelhas)

def construir_frame_selecao_ordem():

    global nova_frame

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill(cor_fundo)

    frame_numero_linhas  = 20
    frame_numero_colunas = 3
    nova_frame.blit(lua, (0 ,0))
    nova_frame.blit(logo, (210,67))

    frame_numero_linhas  = 20
    frame_numero_colunas = 3
    nova_frame.blit(lua, (0 ,0))
    nova_frame.blit(logo, (210,67))

    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 15, 2)
    botao_texto('First', centro,accao_botao_primeiro)

    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 17, 2)
    botao_texto('Second', centro,accao_botao_segundo)
            
def construir_frame_jogo():

    # a frame de jogo é sempre construída para o jogador humano. O
    # computador joga imediatamente a seguir ao jogador humano no
    # evento da jogada do jogador humano.
    global nova_frame

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill(cor_fundo)

    frame_numero_linhas  = 6
    frame_numero_colunas = 3
    nova_frame.blit(lua, (0 ,0 )) #x, y
    nova_frame.blit(tabuleiro, ( (LARGURA - 496) / 2 ,(ALTURA -430) / 2))
    centro = get_centro_grelha(frame_numero_linhas, frame_numero_colunas, 5, 2)

    linha        = 1
    coluna_mouse = get_coluna_mouse()
    peca         = ordem_escolhida

    if ha_espaco(jogo, coluna_mouse):
        desenha_peca_jogo(linha, coluna_mouse, peca)

    for l in range(6):
        for c in range(7):
            peca = valor(jogo, l+1, c+1)
            desenha_peca_jogo(l+1+1, c+1, peca)

    # processar jogada
    if mouse_click == True:
        processar_jogada() 

def construir_frame_fim():

    # a frame de jogo é sempre construída para o jogador humano. O
    # computador joga imediatamente a seguir ao jogador humano no
    # evento da jogada do jogador humano.
    global nova_frame
    global musica_a_tocar

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill((255,255,0))

    frame_numero_linhas  = 6
    frame_numero_colunas = 3
    nova_frame.blit(lua, (0 ,0 )) #x, y
    nova_frame.blit(tabuleiro, ( (LARGURA - 496) / 2 ,(ALTURA -430) / 2))

    #Desenhar grelha
    for l in range(6):
        for c in range(7):
            peca = valor(jogo, l+1, c+1)
            desenha_peca_jogo(l+1+1, c+1, peca)
    
    #Desenhar a linha vencedora em cima da grelha
    vencedor = quem_ganhou(jogo)
    if vencedor == None:
        texto = 'It\'s a Draw!'
    elif vencedor == ordem_escolhida:
        texto = 'You won!'
        linha = get_linha_vitoria(jogo)
        desenha_linha_vitoria(linha)
        if(musica_a_tocar != musica_ganhar):
            tocar_musica(musica_ganhar)
    else:
        texto = 'You lost!'
        linha = get_linha_vitoria(jogo)
        desenha_linha_vitoria(linha)
        if(musica_a_tocar != musica_perder):
            tocar_musica(musica_perder)

    texto = texto + ' Play again?'

    
    frame_numero_linhas  = 7
    frame_numero_colunas = 7
    (centro_x, centro_y) = get_centro(frame_numero_linhas,frame_numero_colunas, 1, 2)
    centro_x = centro_x + int(LARGURA / frame_numero_colunas / 2)
    centro = (centro_x, centro_y)
    desenha_texto_branco(texto, centro)
    
        
    # botão "Sim"
    texto       = 'Yes'
    centro      = get_centro(frame_numero_linhas, frame_numero_colunas, 1, 5)
    botao_texto(texto, centro,acao_botao_sim, BRANCO)

    # botão "Não"
    texto       = 'No'
    centro      = get_centro(frame_numero_linhas, frame_numero_colunas, 1, 6)
    botao_texto(texto, centro,acao_botao_nao, BRANCO)

def get_a_outra_cor(cor):
    
    if cor == VERMELHO:
        return AMARELO
    else:
        return VERMELHO

def set_cores_jogadores():

    global cor_jogador_1
    global cor_jogador_2

    if ordem_escolhida == 1:
        cor_jogador_1 = cor_escolhida
        cor_jogador_2 = get_a_outra_cor(cor_escolhida)
    else:
        cor_jogador_2 = cor_escolhida
        cor_jogador_1 = get_a_outra_cor(cor_escolhida)

def get_ordem_agente():

    if ordem_escolhida == 1:
        return 2
    else:
        return 1

def comecar_jogo():

    global jogo
    global jogador
    set_cores_jogadores()

    jogo = novo_jogo()
    jogador = 1

    if ordem_escolhida == 2:
        jogada = jogada_agente(jogo, get_ordem_agente())
        jogo = jogar(jogo, jogada)

def get_cor_peca(valor):
    if valor == 0:
        return BRANCO
        
    elif valor == 1:
        return cor_jogador_1

    elif valor == 2:
        return cor_jogador_2

def desenha_peca(linha, coluna, valor):

    frame_numero_linhas  = 7
    frame_numero_colunas = 7
    peca = None
    centro = get_centro_grelha(frame_numero_linhas, frame_numero_colunas, linha,coluna)
    #desenha_texto(str(valor), centro)

    cor = get_cor_peca(valor)
    if(cor == BRANCO):
        peca = peca_trasparente


    if(cor == VERMELHO):
        peca = peca_vermelha

    if(cor == AMARELO):
        peca = peca_amarela

    if(valor == 4):
        peca = peca_dourada

    nova_frame.blit(peca,(centro[0]-27, centro[1]-27))

def desenha_peca_jogo(linha, coluna, valor):
    desenha_peca(linha, coluna, valor)

def desenha_peca_vitoria(linha, coluna):
    valor = 4
    desenha_peca(linha+1, coluna, valor)

def get_coluna_mouse():
    rato_x = posicao_mouse_x
    
    x_minimo = (LARGURA - 496) / 2
    x_maximo = x_minimo + 496

    frame_numero_colunas = 7


    if rato_x > x_minimo and rato_x < x_maximo:
        largura_coluna = 496 / 7
        coluna_mouse = int(rato_x / largura_coluna)
        coluna_mouse = coluna_mouse - 1
        if(coluna_mouse > 7):
            coluna_mouse = 7
        if(coluna_mouse < 1):
            coluna_mouse = 1
        return coluna_mouse 
    elif rato_x < x_minimo:
         return 1
    elif rato_x > x_maximo:
         return frame_numero_colunas


    '''
    #largura_coluna = LARGURA / frame_numero_colunas
    largura_coluna =  ((LARGURA - 465) + 240) / frame_numero_colunas

    coluna_mouse = int(posicao_mouse_x / largura_coluna) + 1
    if(coluna_mouse > frame_numero_colunas):
        return frame_numero_colunas
    print(coluna_mouse)
    '''

def processar_jogada():

    # a jogada é sempre do jogador humano. O computador joga
    # imediatamente a seguir ao jogador humano no evento da jogada do
    # jogador humano.

    global jogo
    global ecra

    coluna_mouse = get_coluna_mouse()
    if ha_espaco(jogo, coluna_mouse):

        jogo = jogar(jogo, coluna_mouse)

        if terminou(jogo):
            ecra = ECRA_FIM

        else:
            # jogada do computador
            coluna = jogada_agente(jogo, get_ordem_agente())

            jogo = jogar(jogo, coluna)

            if terminou(jogo):
                ecra = ECRA_FIM

def desenha_linha_vitoria(linha):
    for par in linha:
        indice_linha  = par[0]
        indice_coluna = par[1]
        desenha_peca_vitoria(indice_linha, indice_coluna)

def construir_nova_frame():
    if ecra == ECRA_INICIAL:
        construir_frame_inicio()
    if ecra == ECRA_SELECAO_JOGO:
        construir_frame_selecao_jogo()
    if ecra == ECRA_SELECAO_CORES:
        construir_frame_selecao_cores()
    elif ecra == ECRA_SELECAO_ORDEM:
        construir_frame_selecao_ordem()
    elif ecra == ECRA_JOGO:
        construir_frame_jogo()
    elif ecra == ECRA_FIM:
        construir_frame_fim()

# ciclo principal
while not(fim):
    t = t + 2
    processar_eventos_pygame()

    construir_nova_frame()

    # actualizar pygame com a nova imagem
    janela.blit(nova_frame, (0, 0))
    pygame.display.flip()

    # esperar o tempo necessário para cumprir o frame rate
    # só deve ser chamado uma vez por frame
    clock.tick(frame_rate)

    #print_aux()

# fechar a janela. pygame.quit() só é necessário para fechar a janela
# quando o programa é executado a partir do IDLE (porque o IDLE guarda
# uma referência para a janela aberta e sem esta instrução a
# janela não fecha quando o programa termina. Só fecha quando o IDLE
# termina).  
pygame.quit()
