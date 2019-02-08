

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

# criação de uma janela
LARGURA = 600
ALTURA  = 400
tamanho = (LARGURA, ALTURA)
janela  = pygame.display.set_mode(tamanho)

# número de imagens por segundo
frame_rate = 10
# relógio para controlo do frame rate
clock = pygame.time.Clock()

# ecrãs 
ECRA_SELECAO_CORES = 1
ECRA_SELECAO_ORDEM = 2
ECRA_JOGO          = 3
ECRA_FIM           = 4
# ecrã atual
ecra = ECRA_SELECAO_CORES

# eventos
fim             = False # porque o jogador não quer jogar mais ou
                        # porque fechou a janela
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

# texto a usar nos botões
texto_cor      = BRANCO
texto_tamanho  = int(ALTURA / 10) # altura em pixels
fonte_ficheiro = None # None = pygame default font (existe sempre em
                      # quaquer computador que tenha pygame)
texto_fonte    = pygame.font.Font(fonte_ficheiro, texto_tamanho) 

# cor de fundo
cor_fundo = AZUL

# jogo 4 em linha
jogo          = None
jogador       = None
cor_jogador_1 = None
cor_jogador_2 = None





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





def botao(texto, centro_x, centro_y, largura, altura, cor_inativo, cor_ativo,
           acao):

    resultado = False

    posicao_x = int(centro_x - largura/2)
    posicao_y = int(centro_y - altura/2)

    if (posicao_x < posicao_mouse_x < posicao_x + largura) \
       and (posicao_y < posicao_mouse_y < posicao_y + altura):

        # o mouse está dentro do retângulo do botão

        pygame.draw.rect(nova_frame, cor_ativo,
                         (posicao_x, posicao_y, largura, altura))

        if mouse_click == True:
            acao()

    else:
        
        # o mouse está fora do retângulo do botão
        pygame.draw.rect(nova_frame, cor_inativo,
                         (posicao_x, posicao_y, largura, altura))

    desenha_texto(texto, (centro_x, centro_y))

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





def desenha_texto(texto, centro):

    texto_surface     = texto_fonte.render(texto, True, texto_cor)
    texto_rect        = texto_surface.get_rect()
    texto_rect.center = centro
    nova_frame.blit(texto_surface, texto_rect)





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





def construir_frame_selecao_cores():

    global nova_frame

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill(cor_fundo)

    frame_numero_linhas  = 4
    frame_numero_colunas = 3

    # texto "4 em linha"
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 1, 2)
    desenha_texto('4 em linha MDP', centro)

    # texto "escolha"
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 2, 2)
    desenha_texto('escolha', centro)

    # botão "vermelhas"
    texto       = 'vermelhas'
    centro      = get_centro(frame_numero_linhas, frame_numero_colunas, 3, 1)
    largura     = int(LARGURA / frame_numero_colunas)
    altura      = int(ALTURA / frame_numero_linhas)
    cor_inativo = AZUL
    cor_ativo   = VERMELHO
    botao(texto, centro[0], centro[1], largura, altura, cor_inativo,
          cor_ativo, accao_botao_vermelhas)

    # texto "ou"
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 3, 2)
    desenha_texto('ou', centro)
    
    # botão "amarelas"
    texto       = 'amarelas'
    centro      = get_centro(frame_numero_linhas, frame_numero_colunas, 3, 3)
    largura     = int(LARGURA / frame_numero_colunas)
    altura      = int(ALTURA / frame_numero_linhas)
    cor_inativo = AZUL
    cor_ativo   = AMARELO
    botao(texto, centro[0], centro[1], largura, altura, cor_inativo,
          cor_ativo, accao_botao_amarelas)





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




    
def construir_frame_selecao_ordem():

    global nova_frame

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill(cor_fundo)

    frame_numero_linhas  = 4
    frame_numero_colunas = 3

    # texto "4 em linha"
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 1, 2)
    desenha_texto('4 em linha MDP', centro)

    # texto "escolha"
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 2, 2)
    desenha_texto('escolha', centro)

    # botão "primeiro"
    texto       = 'primeiro'
    centro      = get_centro(frame_numero_linhas, frame_numero_colunas, 3, 1)
    largura     = int(LARGURA / frame_numero_colunas)
    altura      = int(ALTURA / frame_numero_linhas)
    cor_inativo = AZUL
    cor_ativo   = cor_escolhida
    botao(texto, centro[0], centro[1], largura, altura, cor_inativo,
          cor_ativo, accao_botao_primeiro)

    # texto "ou"
    centro = get_centro(frame_numero_linhas, frame_numero_colunas, 3, 2)
    desenha_texto('ou', centro)
    
    # botão "segundo"
    texto       = 'segundo'
    centro      = get_centro(frame_numero_linhas, frame_numero_colunas, 3, 3)
    largura     = int(LARGURA / frame_numero_colunas)
    altura      = int(ALTURA / frame_numero_linhas)
    cor_inativo = AZUL
    cor_ativo   = cor_escolhida
    botao(texto, centro[0], centro[1], largura, altura, cor_inativo,
          cor_ativo, accao_botao_segundo)





def get_cor_peca(valor):

    if valor == 0:
        return BRANCO
        
    elif valor == 1:
        return cor_jogador_1

    elif valor == 2:
        return cor_jogador_2





def desenha_peca(linha, coluna, valor, raio):

    frame_numero_linhas  = 7
    frame_numero_colunas = 7

    centro = get_centro(frame_numero_linhas, frame_numero_colunas, linha,
                        coluna)
    #desenha_texto(str(valor), centro)

    cor = get_cor_peca(valor)

    pygame.draw.circle(nova_frame, cor, centro, raio)





def desenha_peca_jogo(linha, coluna, valor):

    raio = int(min(ALTURA, LARGURA) / 8 / 2)

    desenha_peca(linha, coluna, valor, raio)





def desenha_peca_vitoria(linha, coluna):

    valor = 0

    raio = int(min(ALTURA, LARGURA) / 6 / 2)

    desenha_peca(linha+1, coluna, valor, raio)





def get_coluna_mouse():

    frame_numero_colunas = 7

    largura_coluna = LARGURA / frame_numero_colunas

    coluna_mouse = int(posicao_mouse_x / largura_coluna) + 1

    return coluna_mouse





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
        
    
        
        

def construir_frame_jogo():

    # a frame de jogo é sempre construída para o jogador humano. O
    # computador joga imediatamente a seguir ao jogador humano no
    # evento da jogada do jogador humano.

    global nova_frame

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill(cor_fundo)

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





def acao_botao_sim():

    global ecra

    comecar_jogo()

    ecra = ECRA_JOGO





def acao_botao_nao():

    global fim

    fim = True





def desenha_linha_vitoria(linha):
    for par in linha:
        indice_linha  = par[0]
        indice_coluna = par[1]
        desenha_peca_vitoria(indice_linha, indice_coluna)





def construir_frame_fim():

    global nova_frame

    # criar uma nova frame
    nova_frame = pygame.Surface(tamanho)

    # cor de fundo
    nova_frame.fill(cor_fundo)

    vencedor = quem_ganhou(jogo)
    if vencedor == None:
        texto = 'Empate!'
    elif vencedor == ordem_escolhida:
        texto = 'Vitória!'
        linha = get_linha_vitoria(jogo)
        desenha_linha_vitoria(linha)
    else:
        texto = 'Derrota!'
        linha = get_linha_vitoria(jogo)
        desenha_linha_vitoria(linha)

    for l in range(6):
        for c in range(7):
            
            peca = valor(jogo, l+1, c+1)
            desenha_peca_jogo(l+1+1, c+1, peca)

    texto = texto + ' Outro jogo?'
    frame_numero_linhas  = 7
    frame_numero_colunas = 7
    (centro_x, centro_y) = get_centro(frame_numero_linhas,
                                      frame_numero_colunas, 1, 2)
    centro_x = centro_x + int(LARGURA / frame_numero_colunas / 2)
    centro = (centro_x, centro_y)
    desenha_texto(texto, centro)
        
    # botão "Sim"
    texto       = 'Sim'
    centro      = get_centro(frame_numero_linhas, frame_numero_colunas, 1, 5)
    largura     = int(LARGURA / frame_numero_colunas)
    altura      = int(ALTURA / frame_numero_linhas)
    cor_inativo = AZUL
    cor_ativo   = cor_escolhida
    botao(texto, centro[0], centro[1], largura, altura, cor_inativo,
          cor_ativo, acao_botao_sim)

    # botão "Não"
    texto       = 'Não'
    centro      = get_centro(frame_numero_linhas, frame_numero_colunas, 1, 6)
    largura     = int(LARGURA / frame_numero_colunas)
    altura      = int(ALTURA / frame_numero_linhas)
    cor_inativo = AZUL
    cor_ativo   = cor_escolhida
    botao(texto, centro[0], centro[1], largura, altura, cor_inativo,
          cor_ativo, acao_botao_nao)





def construir_nova_frame():

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
