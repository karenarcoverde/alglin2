# Programa codigo.py
# Autora: Karen dos Anjos Arcoverde
# Data: 06/02/2021
#


import numpy as np


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
    
    if (tipo_iris == '1'):
        IDs = Setosa
    if (tipo_iris == '2'):
        IDs = Versicolor
    if (tipo_iris == '3'):
        IDs = Virginica
        
    for i in range(1,46): # percorre todo o banco de dados 1-45
        linha = (arquivo.readline()).split(',') #separa os dados por virgula
    
        
        if  (int(linha[0]) in IDs):# percorre os ids selecionados
            linha.pop(0) # retira o ID dos dados
            linha.pop(-1) # retira a espécie dos dados
            for j in range(4): #para cada dado 
                linha[j] = float(linha[j]) #transforma em numero
                
            dados.append(linha) #adiciona na lista de dados
            
    arquivo.close()
    return dados


def construir_equacao_normal (dados):
    
    #equacao normal - minimos quadrados:
    # (x^T).x.w = (x^T).y
    #(x_transposta).x.w =(x_transposta).y
    # R.w = p
    # R = (x^T).x
    # p = (x^T).y
    
    ###### sem termo independente #####
    # y = a*x1 +b*x2 +c*x3
    x = []
    y = []
    
    #achar (x^T) e x
    # x - colunas SepalLengthCm,SepalWidthCm,PetalLengthCm
    x = np.array(dados) 
    x = np.delete(x.reshape(15,4),3,1) #deleta a ultima coluna de x
    x_transposta = np.transpose(x) #faz a transposta de x: (x^T)
    
    #achar R
    R = np.dot(x_transposta,x) #multiplica (x^T) por x
    
    #achar y - coluna PetalWidthCm
    y = np.array(dados) 
    y = np.delete(y.reshape(15,4),0,1) #deleta a primeira coluna de y
    y = np.delete(y.reshape(15,3),0,1) #deleta a segunda coluna de y
    y = np.delete(y.reshape(15,2),0,1) #deleta a terceira coluna de y

    #achar p 
    p = np.dot(x_transposta,y) 
    
    ###### com termo independente #####
    # y = a*x1 +b*x2 +c*x3 +k
     
    for i in range (0,15):
        dados[i][3] = 1
    
    #achar (x^T) e x
    x = np.array(dados) 
    x_transposta = np.transpose(x) #faz a transposta de x: (x^T)
    #achar R
    R1= np.dot(x_transposta,x) #multiplica (x^T) por x
    #achar p 
    p1 = np.dot(x_transposta,y) 
   
    return R,p,R1,p1
    
def decomposicao_espectral(R,R1):
    
    ############ matriz R - sem o termo independente ###############
    #determinando autovalores e autovetores
    autovalores, autovetores = np.linalg.eig(R) 
    # matriz diagonal de autovalores
    matrizDiagonal = np.diag(autovalores) 

    # obtendo novamente a matriz R através da decomposição espectral ou valores singulares
    # R = VDV^(T)
    R = np.matmul(np.matmul(autovetores,matrizDiagonal),np.transpose(autovetores)) 
    
    
    
    ############# matriz R1 - com o termo independente ############# 
    #determinando autovalores e autovetores
    autovalores1, autovetores1 = np.linalg.eig(R1) 
    # matriz diagonal de autovalores
    matrizDiagonal1 = np.diag(autovalores) 

    # obtendo novamente a matriz R através da decomposição espectral ou valores singulares
    # R1 = VDV^(T)
    R1 = np.matmul(np.matmul(autovetores,matrizDiagonal),np.transpose(autovetores)) 
    
    return  autovetores, matrizDiagonal, autovetores1, matrizDiagonal1

############################# Programa Principal #############################
def menu():
    resultado = ""
    tipo_iris = ""
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
            print()
            print("PARA SAIR DIGITE 0")
            
            while (tipo_iris != '0'):
             
                tipo_iris = input()
                
                if (tipo_iris == '0'):
                    break
           
                dados = pegarDados (tipo_iris)
                R,p,R1,p1 = construir_equacao_normal(dados)
                #a,b,c,k = PLU(R,p,R1,p1)
            
    
        if (resultado == '2'):
            print("Digite qual especie voce deseja fazer a regressao linear: ")
            print("1 = Iris-Setosa")
            print("2 = Iris-Versicolor")
            print("3 = Iris Virginica")
            print()
            print("PARA SAIR DIGITE 0")
            
            while (tipo_iris != '0'):
             
                tipo_iris = input()
                
                if (tipo_iris == '0'):
                    break
                    
                print()
           
                dados = pegarDados (tipo_iris)
                R,p,R1,p1 = construir_equacao_normal(dados)
                autovetores, matrizDiagonal,autovetores1,matrizDiagonal1 = decomposicao_espectral(R,R1)
                
                if  (tipo_iris == '1'):
                    print("Iris-Setosa\n")
                elif (tipo_iris == '2'):
                    print("Iris-Versicolor\n")
                elif (tipo_iris == '3'):
                    print("Iris-Virginica\n")
                
                print("SEM O TERMO INDEPENDENTE: ")
                print("V = ",autovetores)
                print()
                print('\u039B = ',matrizDiagonal)
                print()
                print("V^T = ",np.transpose(autovetores))
                
                print()
                print()
                
                print("COM O TERMO INDEPENDENTE: ")
                print("V = ", autovetores1)
                print()
                print('\u039B = ', matrizDiagonal1)
                print()
                print("V^T = ", np.transpose(autovetores1))
                
        
        
        if (resultado == '3'):
            print("ok1")
        
        if (resultado == '4'):
            print("ok2")
    
    
######## chamada ao menu
menu()