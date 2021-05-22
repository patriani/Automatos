# coding=utf-8
import sys

def leituraAFD(arquivo_entrada,arquivo_saida):
  with open(arquivo_entrada, 'r') as arq:
    
    cont = 0
    dic_trans = {}

    for linha in arq:
      linha = linha.partition('#')[0] #divide a linha lida em elementos antes e depois de #
      linha = linha.rstrip()
      temp = linha.split()
      if(cont == 0): # temp[0] == ("formalismo")
        if(temp[0] != "AFD"):
          print("\nColoque um arquivo de AFD para converter\n")
          break       
      if(cont == 1):
        num_estados = temp[0]
        lista_estados = temp[1:]
            
      if(cont == 2):
        num_simbolos = temp[0]
        lista_simbolos = temp[1:]
      
      if(cont == 3):
        estado_inicial = temp[0]
      
      if(cont == 4):
        num_estados_finais = temp[0]
        lista_estados_finais = temp[1:]
              
      if(cont >= 5):
        if(len(temp)>0):
          state_key = temp[0] # estado chave do dicionário
          simble_key = temp[1] # símbolo chave do dicionário encadeado
          lista_trans = temp[2] # lista de estados a partir do estado corrente
          if(temp[3:]):# um AFD não pode levar a mais de um estado pela leitura de um unico simbolo
            print("Erro, automato nao deterministico")
            break
          if(state_key in dic_trans):
            dic_trans[state_key][simble_key] = lista_trans
          else:
            dic_trans[state_key] = {} # cria um dicionário para o "símbolo novo"
            dic_trans[state_key][simble_key] = lista_trans
      cont+=1
    else:

      for i in range(len(lista_estados)): #caso algum estado não leia nenhum simbolo
        if lista_estados[i] not in dic_trans:
          dic_trans[lista_estados[i]] = {}
          for simbolo in lista_simbolos:
            dic_trans[lista_estados[i]][simbolo] = ''
      #cria uma representação vazia de transição (não eh uma transição vazia. Eh uma ausência)
      for i in range(len(lista_estados)):
        for simbolo in lista_simbolos:  
          if simbolo not in dic_trans[lista_estados[i]]:
            dic_trans[lista_estados[i]][simbolo] = ''

    diferenca_trivial(dic_trans, lista_estados_finais, lista_simbolos,estado_inicial,arquivo_saida)

# Função que marca os estados finais e não finais do dicionário de transições
def diferenca_trivial(dic_trans, lista_estados_finais, lista_simbolos,estado_inicial,arquivo_saida):
  nao_finais = dic_trans.keys()
  nao_finais = nao_finais - lista_estados_finais
  nao_finais = sorted(nao_finais, key=None, reverse=False)

  lista = [lista_estados_finais, nao_finais]
  
  minimizacao_afd(lista_estados_finais,lista,lista_simbolos,dic_trans,estado_inicial,arquivo_saida)

def minimizacao_afd(estados_finais,lista, lista_simbolos, dic_trans,estado_inicial,arquivo_saida):
  # cópia de lista para referencia futura (estados_finais,estados_nao_finais) 
  lista_S = lista.copy()

  while lista_S:
    #como lista_S eh uma lista de listas, secao pega primeiro a lista de estados finais ( primeiro pop(0) ) e depois começa a pegar elementos da lista de estados não finais.
    secao = lista_S.pop(0)
    diferenca = []
    intersecao = []

    # (linha 86) estados = [] : lista de estados que a partir do simbolo em questao levam a um estado presente em secao
    for simbolo in lista_simbolos:
      estados = []
      for estado in dic_trans:
        #adiciona o estado que leva um elemento da lista (pode ser final ou não) - por meio de pelo menos um símbolo
        if dic_trans[estado][simbolo] in secao:
          estados.append(estado)
    

      for estado_set in lista: 
        diferenca = []
        intersecao = []
 
        # diferenca: captura resultado em uma lista da analise de transições de tipos diferentes. Por meio do "not in" pega elementos que não estão na mesma classificação.
        for estado in estado_set:
          if estado not in estados:
            diferenca.append(estado)
        # intersecao: captura elementos que estão em ambos conjuntos de estados.
        for estado in estados:
          if estado in estado_set:
            intersecao.append(estado)
        # essas operações podem retornar vazio [].O "and" tratará isso de forma que se alguma das listas estiver vazia a lista de estados não é modificada na iteração. Caso não seja, diferenca e intersecao.
	# diferenca e intersecao substituem o conjunto de estados antigos analisados nessa iteração (estado_set)
        if diferenca and intersecao:
          lista.remove(estado_set)
          lista.insert(0,diferenca)
          lista.insert(0,intersecao)
          if estado_set in lista_S: # remove estado_set para que não seja analisado na próxima iteração
            lista_S.remove(estado_set)
            lista_S.insert(0, diferenca)
            lista_S.insert(0, intersecao)
      
  afd_minimo = {} # cria novo dicionario para o minimizado
  
  # como lista agora é resultado da análise de equivalencia entre estados podemos criar uma lista de transições com o novo conjunto de estados tendo como base o dicionario do afd base
  for estado in lista:
    transicao_nova = {}
    for simbolo in lista_simbolos:
      transicao = dic_trans[estado[0]][simbolo]
      if transicao in estado:
        transicao_estado = estado
      else: # reinicia leitura da lista para tentar encontrar a transição correspondente 
        for lista_confere in lista:
          if transicao in lista_confere:
            transicao_estado = lista_confere
      transicao_nova[simbolo] = transicao_estado
    afd_minimo[repr(estado)] = transicao_nova
  
  lista = afd_minimo
  
  novos_finais = []
  # analisa os novos estados finais por meio da comparação com a lista de estados finais do afd base
  for final in estados_finais:
      for estado in lista:
          if final in estado:
              novos_finais.append(estado)              
  if novos_finais != []:
    estados_finais = novos_finais
  
  #remove possiveis redundancias nas listas
  estados_finais = list(set(estados_finais))    
  lista = list(set(lista.keys()))
  
  escreveAFD(lista, lista_simbolos,estado_inicial,estados_finais,afd_minimo,arquivo_saida)

def escreveAFD(lista_estados_afd_minimo,lista_simbolos,estado_inicial,estados_finais_afd_minimo,afd_minimo,arquivo_saida): 

  arquivo = open(arquivo_saida, "w")
  output = list()

  lista_estados_afd_minimo = sorted(lista_estados_afd_minimo)

  estados_finais_afd_minimo = sorted(estados_finais_afd_minimo)
  
  # (Linha 1) Representação do formalismo
  output.append("AFD_Minimo\n")
   

  # quantidade de estados e quais são
  sorted(lista_estados_afd_minimo)
  output.append("Quantidade de estados: ")
  tamanho = str(len(lista_estados_afd_minimo))
  output.append(tamanho)
  output.append("\nLista de Estados: ")
  for i in range(len(lista_estados_afd_minimo)):
    output.append(lista_estados_afd_minimo[i])
    output.append(" ")
  output.append("\n")

  # quantidade de simbolos

  output.append("Quantidade de simbolos: ")
  tamanho = str(len(lista_simbolos))
  output.append(tamanho)
  output.append("\n")

  # estado inicial

  output.append("Estado Inicial: ")
  output.append(estado_inicial)
  output.append('\n')

  # quantidade de estados finais e quais são

  tamanho = str(len(estados_finais_afd_minimo))
  output.append("Numero de estados Finais: ")
  output.append(tamanho)
  output.append("\nLista de Estados Finais: ")
  
  for i in range(len(estados_finais_afd_minimo)):
    output.append(estados_finais_afd_minimo[i])
    output.append(" ")
  output.append("\n")

  # formatação de transição
  output.append("Transições:\n")
  for estado in lista_estados_afd_minimo:
    for simbolo in lista_simbolos:
      output.append("δ( ")
      output.append(estado)
      output.append(" , ")
      output.append(simbolo)
      output.append(" ) = {")
      output.append(str(afd_minimo[estado][simbolo]))
      output.append("}\n")

  
  arquivo.writelines(output)
  arquivo.close() 
  
def main(argv):
  # argv[0]: contém o nome do arquivo de descrição do AFD a ser minimizado
  # argv[1]: contém o nome do arquivo de saída que terá a descrição do AFD mínimo 

  leituraAFD(argv[0],argv[1])
  

if __name__ == "__main__":
  main(sys.argv[1:])  
