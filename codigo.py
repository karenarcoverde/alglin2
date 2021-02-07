# Programa codigo.py
# Autora: Karen dos Anjos Arcoverde
# Data: 06/02/2021
#


import numpy as np
from scipy.linalg import svd


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

# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
def PLU(R,p):
    indice_coluna = 0 
    indice_linha = 1
    indice_L_1s = 0
    tamanho_R = len(R)
    
    while (indice_coluna < tamanho_R):
        #constroi a matriz L, triangular inferior
        if (R[indice_coluna][indice_coluna] != 0):
            L = np.zeros((tamanho_R, tamanho_R))
            
            indice_coluna_aux = indice_coluna + 1
            while (indice_coluna_aux < tamanho_R):
                L[indice_coluna_aux][indice_coluna] = - R[indice_coluna_aux][indice_coluna]/R[indice_coluna][indice_coluna]
                indice_linha += 1
                indice_coluna_aux += 1
            
            while (indice_L_1s < tamanho_R):
                L[indice_L_1s][indice_L_1s] = 1
                indice_L_1s += 1
            
            indice_L_1s = 0
            indice_linha = 1
                 
            #multiplica a matriz R por L
            R = np.dot (L,R)
            p = np.dot (L,p)
        
                
        #se o pivo for zero, necessario multiplicar por uma matriz P de permutacao
        if (R[indice_coluna][indice_coluna] == 0):
            P = np.zeros((tamanho_R, tamanho_R))
            P[indice_coluna][indice_coluna + 1] = 1
            P[indice_coluna + 1][indice_coluna] = 1
            
            R = np.dot(P,R)
            p = np.dot (P,p)
       
        indice_coluna += 1 
        
   
        
    #backsubstitution
    w = np.linalg.solve(R, p)
      
    return w
           
# -----------------------------------------------------------------------------
def decomposicao_espectral(R,R1):
    
    ############ matriz R - sem o termo independente ###############
    # R = VDV^(T)
    #determinando autovalores e autovetores
    autovalores, autovetores = np.linalg.eig(R) 
    # matriz diagonal de autovalores
    matrizDiagonal = np.diag(autovalores) 

    ############# matriz R1 - com o termo independente ############# 
    # R1 = VDV^(T)
    #determinando autovalores e autovetores
    autovalores1, autovetores1 = np.linalg.eig(R1) 
    # matriz diagonal de autovalores
    matrizDiagonal1 = np.diag(autovalores) 
    
    return  autovetores, matrizDiagonal, autovetores1, matrizDiagonal1

############################# Programa Principal #############################
def menu():
    resultado = ""
    tipo_iris = ""
    coeficientes_sem_aux = []
    coeficientes_com_aux = []
    indice = 0
    
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
                w = PLU(R,p)
                w1 = PLU(R1,p1)
                          
                print()
                if  (tipo_iris == '1'):
                    print("Iris-Setosa\n")
                elif (tipo_iris == '2'):
                    print("Iris-Versicolor\n")
                elif (tipo_iris == '3'):
                    print("Iris-Virginica\n")
                    
                print("SEM O TERMO INDEPENDENTE: ")
                print("y = a*x1 + b*x2 + c*x3")
                print("[a b c] = ",end="")
                
                
                while (indice < len(w)):
                    coeficientes_sem_aux.append(w[indice][0])
                    coeficientes_sem = np.array(coeficientes_sem_aux)
                    indice += 1
                
                print(coeficientes_sem)
                coeficientes_sem_aux = []
                
                    
                print()
                
                print("COM O TERMO INDEPENDENTE: ")
                print("y = a*x1 + b*x2 + c*x3 + k")
                print("[a b c k] = ",end="")
                
                indice = 0
                while (indice < len(w1)):
                    coeficientes_com_aux.append(w1[indice][0])
                    coeficientes_com = np.array(coeficientes_com_aux)
                    indice += 1
                
                print(coeficientes_com)
                coeficientes_com_aux = []  
                indice = 0
               
            
    
        if (resultado == '2'):
            print("Digite qual especie voce deseja fazer a decomposicao espectral: ")
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
           print("Digite qual especie voce deseja fazer o SVD: ")
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
               U, s, VT = svd(R)
               U, s, VT = svd(R1)
               
               if  (tipo_iris == '1'):
                    print("Iris-Setosa\n")
               elif (tipo_iris == '2'):
                    print("Iris-Versicolor\n")
               elif (tipo_iris == '3'):
                    print("Iris-Virginica\n")
               
               print("SEM O TERMO INDEPENDENTE: ")
               print("U = ", U)
               print()
               print('\u03A3 = ', s)
               print()
               print("V^T = ", VT)
                
               print()
               print()
                
               print("COM O TERMO INDEPENDENTE: ")
               print("U = ", U)
               print()
               print('\u03A3 = ', s)
               print()
               print("V^T = ", VT)
                
        if (resultado == '4'):
            print("ok2")
    
    
######## chamada ao menu
menu()