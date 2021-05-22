# coding=utf-8
import sys

def leituraAFN(descricao_afn):
  with open(descricao_afn, 'r') as arq:
    cont = 0
    dic_trans = {}

    for linha in arq:
      linha = linha.partition('#')[0] #divide a linha lida em elementos antes e depois de #
      linha = linha.rstrip()
      temp = linha.split()
      if(cont == 0): # temp[0] == ("formalismo")
        if(temp[0] != "AFN"):
          print("\nColoque um arquivo de AFN para converter\n")
          break       
      if(cont == 1):
        num_estados = temp[0]
        lista_estados = temp[1:]
        #print(lista_estados)
            
      if(cont == 2):
        num_simbolos = temp[0]
        lista_simbolos = temp[1:]
        #print(lista_simbolos)
      
      if(cont == 3):
        estado_inicial = temp[0]
        #print(estado_inicial)
      
      if(cont == 4):
        num_estados_finais = temp[0]
        lista_estados_finais = temp[1:]
        #print(lista_estados_finais)
              
      if(cont >= 5):
        if(len(temp)>0):
          state_key = temp[0] # estado chave do dicionário
          simble_key = temp[1] # símbolo chave do dicionário encadeado
          lista_trans = temp[2:] # lista de estados a partir do estado corrente
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
      #print(dic_trans)
      return (lista_estados , lista_simbolos,dic_trans,lista_estados_finais)
 
def conversao(arquivo_saida,lista_estados,lista_simbolos,afn, afn_estados_finais):
  nova_lista_estados = []
  afd = {}
  afd[lista_estados[0]] = {} # cria dicionário para estado inicial
  for y in range(len(lista_simbolos)): # união de estados para AFD
      temp = "".join(afn[lista_estados[0]][lista_simbolos[y]])   
      afd[lista_estados[0]][lista_simbolos[y]] = temp 
      if temp not in lista_estados: # caso seja do formato "12"
          nova_lista_estados.append(temp)
          lista_estados.append(temp)
      if temp in lista_estados:
        if temp not in nova_lista_estados:
          nova_lista_estados.append(temp)
          
  # Dicionário para os outros estados
  vazio = ''
  controle = [] #recebe nova_lista_estados para fins comparativos. Não tem seus elementos removidos durante as iterações no while
  controle = nova_lista_estados
  while len(nova_lista_estados) != 0:
    if vazio in nova_lista_estados: #evita que lixo seja interpretado como estado
      nova_lista_estados.remove(vazio)
    if len(nova_lista_estados) == 0: # quando o ultimo estado eh apagado fica [''] no lugar de um estado. Isso não deve ser aceito
      break
    afd[nova_lista_estados[0]] = {} # cria estado no AFD correspondente à união
    for _ in range(len(nova_lista_estados[0])):
      for i in range(len(lista_simbolos)):
        var = [] # criando lista temporária
        for j in range(len(nova_lista_estados[0])):
          #print(nova_lista_estados[0][j])
          if lista_simbolos[i] in afn[nova_lista_estados[0][j]]: # verifica se estado aborda o símbolo em questão
            var += afn[nova_lista_estados[0][j]][lista_simbolos[i]] # fazendo a união dos estados
        var = list(set(var)) # retira repetições do tipo ['1','2','1','2']
        var = sorted(var) # remove estados duplicados como ['12','21']
        
        s = ""
        s = s.join(var) # criando um novo estados para todos os elementos da lista
        #print(type(s))
        # s = str(sorted(s))
       

        if s not in lista_estados:
          nova_lista_estados.append(s)
          lista_estados.append(s)
          controle.append(s)
        if s in lista_estados:
          if s not in nova_lista_estados:
            if s not in controle:

              controle.append(s)
              controle = list(set(controle))
              nova_lista_estados.append(s)
              
        if len(nova_lista_estados[0]) != 0:
          afd[nova_lista_estados[0]][lista_simbolos[i]] = s # atribuindo o novo estado ao AFD
    nova_lista_estados.remove(nova_lista_estados[0])
    
  
  lista_estados_afd = list(afd.keys())
  estados_finais_afd = []

  for x in lista_estados_afd:
      for i in x:
          if i in afn_estados_finais:
              estados_finais_afd.append(x)
              break
              
  escreve_arquivo(arquivo_saida,lista_estados_afd,lista_simbolos,lista_estados_afd[0],estados_finais_afd,afd)

def escreve_arquivo(arquivo_saida,lista_estados_afd,lista_simbolos,estado_inicial,estados_finais_afd,afd): 

  #print(afd)
  arquivo = open(arquivo_saida , "w")
  output = list()
  
  # (Linha 1) Representação do formalismo
  output.append("AFD\n")

  # quantidade de estados e quais são
  output.append("Quantidade de estados: ")
  tamanho = str(len(lista_estados_afd))
  output.append(tamanho)
  output.append("\nLista de Estados: ")
  for i in range(len(lista_estados_afd)):
    output.append(lista_estados_afd[i])
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

  tamanho = str(len(estados_finais_afd))
  output.append("Numero de estados Finais: ")
  output.append(tamanho)
  output.append("\nLista de Estados Finais: ")
  for i in range(len(estados_finais_afd)):
    output.append(estados_finais_afd[i])
    output.append(" ")
  output.append("\n")

  #linha 6 em diante == transições
  # δ(q3, a) = {q3}
  #lista_estados_afd,lista_simbolos
  output.append("Transições:\n")
  for estado in lista_estados_afd:
    for simbolo in lista_simbolos:
      output.append("δ( ")
      output.append(estado)
      output.append(" , ")
      output.append(simbolo)
      output.append(" ) = {")
      output.append(afd[estado][simbolo])
      output.append("}\n")

  arquivo.writelines(output)
  arquivo.close()
  
def main(argv): 
  # argv[0]: contém o nome do arquivo de descrição do AFN
  # argv[1]: contém o nome do arquivo de saída com a descrição do AFD (AFN convertido)
  
  lista_estados, lista_simbolos,afn,estados_finais_afn = leituraAFN(argv[0])
  
  conversao(argv[1],lista_estados,lista_simbolos,afn,estados_finais_afn)
  


if __name__ == "__main__":
  main(sys.argv[1:])