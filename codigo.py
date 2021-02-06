# Programa codigo.py
# Autora: Karen dos Anjos Arcoverde
# Data: 06/02/2021
#


############################# Funcoes #############################
def pegarDados(tipo_iris): 
    
    # tipo_iris = 1 Setosa  , tipo_iris = 2  Versicolor, 
    # tipo_iris = 3 Virginica
    dados = []
    IDs = []
    
    Setosa = range(25,39+1)
    Versicolor = range(75,89+1)
    Virginica = range (125,139+1)
    
    arquivo= open("dados_13.csv",'r')
    arquivo.readline() # ignora a primeira linha
    
    if (tipo_iris == 1):
        IDs = Setosa
    if (tipo_iris == 2):
        IDs = Versicolor
    if (tipo_iris == 3):
        IDs = Virginica
        
    for i in range(1,45): # percorre todo o banco de dados 1-45
        linha = (arquivo.readline()).split(',') #separa os dados por virgula
        
        if  (int(linha[0]) in IDs):# percorre os ids selecionados
            linha.pop(0) # retira o ID dos dados
            linha.pop(-1) # retira a espécie dos dados
            for j in range(4): #para cada dado 
                linha[j] = float(linha[j]) #transforma em numero
                
            dados.append(linha) #adiciona na lista de dados
            
    arquivo.close()
    return dados
    












############################# Programa Principal #############################
def menu():
    resultado = ""
    print()
    print("Digite somente o numero da questao que voce deseja ver o resultado: ")
    print("Questao 1")
    print("Questao 2")
    print("Questao 3")
    print("Questao 4")
    print()
    print("PARA SAIR DIGITE 0")
    
    while (resultado != '0'):
        resultado = input()
    
        if (resultado == '1'):
            print("Digite qual especie voce deseja fazer a regressao linear: ")
            print("1 = Iris-Setosa")
            print("2 = Iris-Versicolor")
            print("3 = Iris Virginica")
             
            tipo_iris = int(input(""))
           
            dados = pegarDados (tipo_iris)
            print(dados)
    
        if (resultado == '2'):
            print("ok")
        
        if (resultado == '3'):
            print("ok1")
        
        if (resultado == '4'):
            print("ok2")
    
    
    
    
    
    
    
    
    
    
    
######## chamada ao menu
menu()