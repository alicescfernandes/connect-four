GRELHA = 0
FIM = 1
VENCEDOR = 2
JOGADOR = 3
LINHA_VITORIA = 4

def novo_jogo():
  '''
  Função que cria um jogo limpo
  
  Argumentos
    * Nenhum

  Retorna:
    (tuplo): Um novo jogo com a grelha limpa, e sem vencedores
  '''
 
  grelha = [
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0]
  ]

  '''
  #Grelha com empate
  grelha = [
    [1,0,0,2,1,2,1],
    [1,2,1,2,1,2,1],
    [1,2,1,2,1,2,1],
    [2,1,2,1,2,1,2],
    [2,1,2,1,2,1,2],
    [2,1,2,1,2,1,2]
  ]
  '''

  fim = False
  vencedor = None
  jogador = 1
  linha_vitoria = None
  jogo = (grelha,fim,vencedor,jogador,linha_vitoria) #Criar o jogo
  return jogo #Retornar o jogo


def valor(jogo,linha,coluna):
  '''
  Retorna um valor para uma determinada "cela" da grelha
  
  Argumentos
    * jogo (tuplo): Jogo para obter os valores
    * linha (int): Linha para obter o valor
    * coluna (int): Coluna para obter o valor

  Retorna:
    (int): Valor para uma dada "cela" do jogo 
  '''
  linha = linha - 1
  coluna = coluna - 1
  grelha =  jogo[GRELHA]
  return grelha[linha][coluna]


def ha_espaco(jogo,coluna):
  '''
  Verifica se para uma determinada coluna, existe espaço para colocar uma peça
  
  Argumentos
    * jogo (tuplo): Jogo para obter os valores
    * coluna (int): Coluna para ver se existe espaço

  Retorna:
    (bool): Returna True or False se houver ou não ouver espaço livre
  '''
  coluna = coluna - 1 # As linhas e colunas começam em 1
  grelha = jogo[GRELHA]
  existe_espaco = False

  for linha in range(len(grelha)-1, -1, -1):
    if grelha[linha][coluna] == 0:
      if(existe_espaco == False):
        existe_espaco = True;
  return existe_espaco
 

def get_linha_vazia(jogo,coluna):
  '''
  Retorna a ultima linha da coluna que esteja vazia. Esta função varre a coluna de baixo para cima, e retorna o primero elemento que encontrar que esteja vazio 
  
  Argumentos
    * jogo (tuplo): Jogo para obter os valores
    * coluna (int): Coluna para ver se existe espaço

  Retorna:
    (int): Retorna o index onde a coluna está vazia, None se não existir posições disponiveis
  '''
  coluna = coluna - 1 # As linhas e colunas começam em 1
  grelha = jogo[GRELHA]
  linha_vazia = None

  for linha in range(len(grelha)-1, -1, -1):
    if grelha[linha][coluna] == 0:
      if(linha_vazia == None):
        linha_vazia = linha;
  return linha_vazia


def jogar(jogo, coluna):
  '''
  Função que joga,e deteta se houve empates ou vitorias.

  Argumentos
    * jogo (tuplo): Jogo para obter os valores
    * coluna (int): Coluna para jogar

  Retorna:
    (tuplo): Jogo modificado, com a nova jogada, e se houver, a vitoria ou empate 
  '''

  # Esta funçao tem de fazer:
  # 1. Jogar
  # 2. Ver se alguem ganhou e terminar jogo
  # 3. Ver se o jogo empatou (sem lugares para jogar) e terminar o jogo
  # 4. Mudar o jogador

  linha = ha_espaco(jogo,coluna) #Perceber se existe espaço para jogar
  
  (grelha,fim,vencedor,jogador,linha_vitoria) = jogo #Desmembrar o jogo, para várias variaveis

  # Jogar
  if(linha != False):
    linha = get_linha_vazia(jogo, coluna)
    coluna = coluna - 1 #As linhas e colunas começam em 1
    grelha[linha][coluna] = jogador

  #Pesquisar por vitorias
  vencedor_1 = pesquisar_grelha(grelha,1)  
  vencedor_2 = pesquisar_grelha(grelha,2)

  #Ver se existe empate, ou vitoria
  if ha_empate(jogo):
    fim = True
    vencedor = None
    linha_vitoria= None
  elif(vencedor_1 != False):
    linha_vitoria = vencedor_1
    fim = True
    vencedor = 1
  elif(vencedor_2 != False):
    linha_vitoria = vencedor_2;
    fim = True
    vencedor = 2

  # Mudar o jogador
  if(jogador == 1):
    jogador = 2
  elif(jogador == 2):
    jogador = 1
  jogo = (grelha,fim,vencedor,jogador,linha_vitoria)
  return jogo  

def terminou(jogo):
  '''
  Função que retorna se o jogo acabou

  Argumentos
    * jogo (tuplo): Jogo para obter os valores

  Retorna:
    (bool): Se o jogo terminou ou não
  '''
  return jogo[FIM]

def quem_ganhou(jogo):
  '''
  Função que retorna se o jogador vencedors

  Argumentos
    * jogo (tuplo): Jogo para obter os valores

  Retorna:
    (int): O vencedor do jogo
  '''
  return jogo[VENCEDOR]

def get_linha_vitoria(jogo):
  '''
  Função que retorna uma lista com as linhas e colunas vencedoras, com o formato (linha, coluna)

  Argumentos
    * jogo (tuplo): Jogo para obter os valores

  Retorna:
    (lista): Uma lista com as linhas e colunas vencedoras, no formato (linha, coluna)
  '''
  return jogo[LINHA_VITORIA]


def ha_empate(jogo):
  '''
  Função que deteta se existe ou não empate. Considera-se como empate uma grelha cheia sem posiçóes livres

  Argumentos
    * jogo (tuplo): Jogo para obter os valores

  Retorna:
    (lista): Uma lista com as linhas e colunas vencedoras, no formato (linha, coluna)
  '''
  existe_empate = True;
  grelha = jogo[GRELHA]

  #Ver se existe empate
  #Empate: Se não existir mais linhas para jogar e não haver vencedores então é empate
  for coluna in range(len(grelha[0])):
    if ha_espaco(jogo, coluna) == True:
      existe_empate = False;
  return existe_empate

def pesquisar_linha(linha, numero_a_pesquisar,grelha):
  '''
  Função que pesquisa se existe 4 em linha numa linha

  Argumentos: 
    linha (int): Linha do jogo para obter 4 linha
    numero_a_pesquisar (int): Numero do jogador, para ver se existe 4 em linha  
    grelha (lista[lista]): Lista com listas, que representa a grelha.
    
  Retorna:
    (lista): Uma lista com as linhas e colunas vencedoras, no formato (linha, coluna)
  '''
  contador = 0
  coluna = 0;
  numero_de_colunas = len(grelha[0]) - 1
  linhas_vencedoras = []

  while contador<=4:
    if(numero_a_pesquisar == grelha[linha][coluna]):
      contador+=1
      linhas_vencedoras.append([linha+1, coluna+1])
    else:
      contador = 0;
      linhas_vencedoras = []
    coluna = coluna + 1
    if(coluna > numero_de_colunas  or contador == 4):
      break

  if contador == 4:
    return linhas_vencedoras
  else:
    return False

def pesquisar_coluna(coluna, numero_a_pesquisar,grelha):
  '''
  Função que pesquisa se existe 4 em linha numa coluna

  Argumentos: 
    coluna (int): Coluna do jogo para obter 4 linha
    numero_a_pesquisar (int): Numero do jogador, para ver se existe 4 em linha  
    grelha (lista[lista]): Lista com listas, que representa a grelha.
    
  Retorna:
    (lista): Uma lista com as linhas e colunas vencedoras, no formato (linha, coluna)
  '''
  contador = 0
  linha = 0;
  numero_de_linhas = len(grelha) - 1
  linhas_vencedoras = []


  while contador<=4:
    if(numero_a_pesquisar == grelha[linha][coluna]):
      contador+=1
      linhas_vencedoras.append([linha+1, coluna+1])

    else:
      linhas_vencedoras = []
      contador = 0;
    linha = linha + 1
    if(linha > numero_de_linhas  or contador == 4):
      break

  if contador == 4:
    return linhas_vencedoras
  else:
    return False

def pesquisar_diagonal_cima(linha, coluna, numero_a_pesquisar,grelha):
  '''
  Função que pesquisa 4 em linha na diagonal

  Argumentos: 
    coluna (int): Coluna do jogo para obter 4 linha
    linha (int): Linha do jogo para obter 4 em linha
    numero_a_pesquisar (int): Numero do jogador, para ver se existe 4 em linha  
    grelha (lista[lista]): Lista com listas, que representa a grelha.
    
  Retorna:
    (lista): Uma lista com as linhas e colunas vencedoras, no formato (linha, coluna)
  '''
  contador = 0
  numero_de_colunas = len(grelha[0]) - 1
  linhas_vencedoras = []


  while contador<=4:
    if(numero_a_pesquisar == grelha[linha][coluna]):
      contador+=1
      linhas_vencedoras.append([linha+1, coluna+1])

    else:
      linhas_vencedoras = []
      contador = 0;
    linha = linha - 1
    coluna = coluna + 1
    if(linha < 0 or coluna > numero_de_colunas  or contador == 4):
      break

  if contador == 4:
    return linhas_vencedoras
  else:
    return False

def pesquisar_diagonal_baixo(linha, coluna, numero_a_pesquisar,grelha):
  '''
  Função que pesquisa 4 em linha na diagonal

  Argumentos: 
    coluna (int): Coluna do jogo para obter 4 linha
    numero_a_pesquisar (int): Numero do jogador, para ver se existe 4 em linha  
    grelha (lista[lista]): Lista com listas, que representa a grelha.
    
  Retorna:
    (lista): Uma lista com as linhas e colunas vencedoras, no formato (linha, coluna)
  '''
  contador = 0
  numero_de_linhas = len(grelha) - 1
  numero_de_colunas = len(grelha[0]) - 1
  linhas_vencedoras = []

  while contador<=4:
    if(numero_a_pesquisar == grelha[linha][coluna]):
      contador+=1
      linhas_vencedoras.append([linha+1, coluna+1])

    else:
      contador = 0;
      linhas_vencedoras = []

    linha = linha + 1
    coluna = coluna + 1
    if(linha > numero_de_linhas or coluna > numero_de_colunas  or contador == 4):
      break

  if contador == 4:
    return linhas_vencedoras
  else:
    return False

def pesquisar_grelha(grelha, numero_a_pesquisar):
  existe_4_em_linha = False


  if(existe_4_em_linha == False):
    for il in range(0, len(grelha)):
      existe_4_em_linha = pesquisar_linha(il, numero_a_pesquisar, grelha)
      if(existe_4_em_linha != False):
        break;

  if(existe_4_em_linha == False):
    for ic in range(0, len(grelha[0])):
      existe_4_em_linha = pesquisar_coluna(ic, numero_a_pesquisar, grelha)
      if(existe_4_em_linha != False):
        break;


  if(existe_4_em_linha == False):
    for il in range(0, len(grelha)):
      for ic in range(0, len(grelha[0])):
        existe_4_em_linha = pesquisar_diagonal_baixo(il, ic,numero_a_pesquisar, grelha)
        if(existe_4_em_linha != False):
          break;
      if(existe_4_em_linha != False):
          break;
          

  if(existe_4_em_linha == False):
    
    for il in range(len(grelha)-1,-1, -1 ):
      for ic in range(0,len(grelha[0])):
        existe_4_em_linha = pesquisar_diagonal_cima(il,ic, numero_a_pesquisar, grelha)
        if(existe_4_em_linha != False):
          break;
      if(existe_4_em_linha != False):
          break;
  return existe_4_em_linha

