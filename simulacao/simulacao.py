# coding=utf-8
import sys

def leituraAFD(descricao_afd,saida_arq,lista_palavras):
  with open(descricao_afd, 'r') as arq:
    cont = 0
    dic_trans = {}
    
    for linha in arq:
      linha = linha.partition('#')[0] #divide a linha lida em elementos antes e depois de #
      linha = linha.rstrip()
      temp = linha.split()
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
          lista_transicoes = [temp[0],temp[1],temp[2]]

          key, value = lista_transicoes[0], lista_transicoes[1:]
          if(key in dic_trans):
            dic_trans[key] += value
          else:
            dic_trans.update({key:value})


        
      cont +=1
    else:    

      verifica_palavra(saida_arq,dic_trans,estado_inicial,lista_estados_finais,lista_palavras)


def palavras(arquivo_palavras):
  lista_palavras = []
  with open(arquivo_palavras, 'r') as arq:
    for linha in arq:
      linha = linha.strip()
      lista_palavras.append(linha)
  return lista_palavras

def escreve_arquivo(saida_arq,lista_estados_finais): #lista_estados_finais recebe dicionário de palavras aceitas
  arquivo = open(saida_arq,"w")
  output = list()
  
  for palavra in lista_estados_finais:
    output.append(palavra)
    output.append(": ")
    output.append(lista_estados_finais[palavra])
    output.append("\n")
  arquivo.writelines(output)
  arquivo.close()

# value definido como: [simbolo,novo estado corrente] ou [simbolo1,novo estado corrente1, simbolo2, novo estado corrente2]. Logo value[0] equivale ao simbolo que aparece primeiro ligado ao estado corrente e value[1] equivale ao novo estado corrente ligado ao simbolo que aparece primeiro (simbolo1)
def verifica_palavra(saida_arq,dic_trans,estado_inicial,lista_estados_finais,lista_palavras):
  palavras_aceitas = {}
  for palavra in lista_palavras: # captura uma palavra da lista de palavras
    state = estado_inicial # computação começa do estado inicial
    for simbolo in palavra: # lê um simbolo por vez
  
      value = dic_trans[state] # value é uma lista
      
      if(len(value)>2): # mais de uma transição aceita (2 simbolos)
        if simbolo in value:
          for index, item in enumerate(value): #['a','0','b','1']
            if simbolo == item : # index == 0
              state = value[(index+1)] # index + 1 == 1
        else:
          state = -1
          break

      else:
        if(value[0] == simbolo):  
          state = value[1]
        else:
          state = -1 # nenhuma transição possível a partir do simbolo 
          break
    if(len(palavra)==1): # no caso do estado inicial ser tambem um estado final e nenhum simbolo for inserido (representação por meio do '_')
      if palavra == '_':
        if estado_inicial in lista_estados_finais:
          state = estado_inicial
          palavras_aceitas.update({palavra:'ACEITA'})
    if(state in lista_estados_finais):
      palavras_aceitas.update({palavra:'ACEITA'}) # classifica palavra como rejeitada no dicionario
    elif(state not in lista_estados_finais):
      palavras_aceitas.update({palavra:'REJEITADA'})# classifica palavra como aceita no dicionario

  escreve_arquivo(saida_arq,palavras_aceitas)

def main(argv):
  # argv[0] recebe o nome do arquivo.txt com a descrição do AFD
  # argv[1] recebe o nome do arquivo.txt com as palavras a serem testadas pelo AFD referente ao argv[0]

  lista_palavras = palavras(argv[1])

  leituraAFD(argv[0],argv[2],lista_palavras)


if __name__ == "__main__":
  main(sys.argv[1:])