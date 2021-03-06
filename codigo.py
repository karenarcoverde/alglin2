# Programa codigo.py
# Autora: Karen dos Anjos Arcoverde
# Data: 06/02/2021
#


import numpy as np
import sys



############################# Funcoes #############################
def pegarDados(tipo_iris): 
    
    # tipo_iris = 1 Setosa  , tipo_iris = 2  Versicolor, 
    # tipo_iris = 3 Virginica
    dados = []
    IDs = []
    
    ## definicao dos ids das especies selecionadas para o trabalho
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
        
    for i in range(1,46): # percorre todo o banco de dados 1-45
        linha = (arquivo.readline()).split(',') #separa os dados por virgula
    
        if  (int(linha[0]) in IDs):# percorre os ids selecionados
            linha.pop(0) # retira o ID dos dados
            linha.pop(-1) # retira a especie dos dados
            for j in range(4): #para cada dado 
                linha[j] = float(linha[j]) #transforma em numero
                
            dados.append(linha) #adiciona na lista de dados
            
    arquivo.close()
    
    return dados

# ----------------------------------------------------------
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

# ----------------------------------------------------------
def PLU(R,p):
    indice_coluna = 0 
    indice_L_1s = 0
    indice_escolher_linha = 0
    tamanho_R = len(R)
    
    while (indice_coluna < (tamanho_R-1)):
        #constroi a matriz L, triangular inferior
        if (R[indice_coluna][indice_coluna] != 0):
            L = np.zeros((tamanho_R, tamanho_R))
            
            indice_coluna_aux = indice_coluna + 1
            while (indice_coluna_aux < tamanho_R):
                L[indice_coluna_aux][indice_coluna] = - R[indice_coluna_aux][indice_coluna]/R[indice_coluna][indice_coluna]
                indice_coluna_aux += 1
            
            while (indice_L_1s < tamanho_R):
                L[indice_L_1s][indice_L_1s] = 1
                indice_L_1s += 1
            
            indice_L_1s = 0
                        
            #multiplica a matriz R por L
            R = np.dot (L,R)
            p = np.dot (L,p)
        
                
        #se o pivo for zero, necessario multiplicar por uma matriz P de permutacao
        if (R[indice_coluna][indice_coluna] == 0):
            P = np.zeros((tamanho_R, tamanho_R))
            indice_escolher_linha = indice_coluna + 1
            while (indice_escolher_linha < tamanho_R):
                if (R[indice_escolher_linha][indice_coluna] != 0):
                    P[indice_coluna][indice_escolher_linha] = 1
                    P[indice_escolher_linha][indice_coluna] = 1
                    
                    indice_coluna -= 1
                    break
                
                indice_escolher_linha += 1
                      
            i = 0
            j = 0
            guarda_1 = False
            while (i < tamanho_R):
                while (j < tamanho_R):
                    if (P[i][j] == 1):
                        guarda_1 = True
                        j += 1
                if (guarda_1 == False):
                    P[i][i] = 1
                i += 1
            
            R = np.dot(P,R)
            p = np.dot (P,p)
            
       
        indice_coluna += 1 
    
    #backsubstitution
    w = np.linalg.solve(R, p)
      
    return w
           
# ----------------------------------------------------------
def decomposicao_espectral(R):
    
    # R = VDV^(T)
    #determinando autovalores e autovetores
    autovalores, autovetores = np.linalg.eig(R) 
    # matriz diagonal de autovalores
    matrizDiagonal = np.diag(autovalores) 
        
    return  autovetores, matrizDiagonal

# ----------------------------------------------------------
def contruir_svd (R):
    s = []
    i = 0
 
    # R = U.s.VT
    #determinando autovalores e autovetores
    ### U
    ## autovetores de R.(R^T)
    autovaloresU, autovetoresU = np.linalg.eig(np.dot(R,np.transpose(R)))
    
    # como R eh simetrica e quadrada: (R^T).R = R.(R^T)
    # entao autovetores e autovalores de U sao iguais aos de V
    
    tamanho_autovalores_U = autovaloresU.shape
      
    while (i < tamanho_autovalores_U [0]):       
        s.append(np.sqrt(autovaloresU [i]))
        i += 1
    
    return  autovetoresU, np.array(s),np.transpose(autovetoresU)

# ----------------------------------------------------------
def estimar_amostras(amostra, w_setosa,w_versicolor,w_virginica,c_independente):
    
   lista_erros = []
   estimativa = ""
   indice = 0
   amostra_x = []
   indice_erros_modulo = 0
   
   while (indice < 3):
       amostra_x.append (amostra[indice])
       indice += 1
       
   if (c_independente == True):
       amostra_x.append(1)
      
   amostra_x = np.array(amostra_x)
   
   #produto interno <x,y> = (x^T).y
   
   estimativa_setosa = np.dot(amostra_x,w_setosa)
   estimativa_versicolor = np.dot(amostra_x,w_versicolor)
   estimativa_virginica = np.dot(amostra_x,w_virginica)
   
   erro_setosa = estimativa_setosa[0] - amostra[3]
   lista_erros.append(erro_setosa)
   
   erro_versicolor = estimativa_versicolor[0] - amostra[3]
   lista_erros.append(erro_versicolor)
   
   erro_virginica = estimativa_virginica[0] - amostra[3]
   lista_erros.append(erro_virginica)
   
   while (indice_erros_modulo < len(lista_erros)):
       lista_erros [indice_erros_modulo] = abs(lista_erros[indice_erros_modulo])
       indice_erros_modulo += 1
   
   if (min(lista_erros) == abs(erro_setosa)):
       estimativa = "Iris-Setosa"
       
       return estimativa
   
   if (min(lista_erros) == abs(erro_versicolor)):
       estimativa = "Iris-Versicolor"
       
       return estimativa
   
   if (min(lista_erros) == abs(erro_virginica)):
       estimativa = "Iris-Virginica"
       
       return estimativa
    
################### Programa Principal ###################
def menu():
    resultado = 0
    tipo_iris = 0
    coeficientes_sem_aux = []
    coeficientes_com_aux = []
    indice = 0
    
    
    while (resultado != 5):    
        print()
        print('##################### MENU PRINCIPAL ##############################')
        print("Digite somente o numero da questao que voce deseja ver o resultado: ")
        print("1 = Questao 1")
        print("2 = Questao 2")
        print("3 = Questao 3")
        print("4 = Questao 4")
        print("5 = SAIR")
        print('###################################################################')
        print()
        
        resultado = int(input())
        
        if (resultado == 5):
            sys.exit(0)
    
        if (resultado == 1):
            
            while (tipo_iris != 4):
                print('##################### MENU IRIS #########################')
                print("Digite qual especie voce deseja fazer a regressao linear: ")
                print("1 = Iris-Setosa")
                print("2 = Iris-Versicolor")
                print("3 = Iris Virginica")
                print("4 = VOLTAR AO MENU PRINCIPAL")
                print('#########################################################')
                print()
             
                tipo_iris = int(input())
                
                if (tipo_iris == 4):
                   menu()
                   
                else:
                    dados = pegarDados (tipo_iris)
                    R,p,R1,p1 = construir_equacao_normal(dados)
                    w = PLU(R,p)
                    w1 = PLU(R1,p1)
                              
                    print()
                    if  (tipo_iris == 1):
                        print("Iris-Setosa\n")
                    elif (tipo_iris == 2):
                        print("Iris-Versicolor\n")
                    elif (tipo_iris == 3):
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
                   
                    print()
    
        if (resultado == 2):
            
            while (tipo_iris != 4):
                print('##################### MENU IRIS ###############################')
                print("Digite qual especie voce deseja fazer a decomposicao espectral: ")
                print("1 = Iris-Setosa")
                print("2 = Iris-Versicolor")
                print("3 = Iris Virginica")
                print("4 = VOLTAR AO MENU PRINCIPAL")
                print('###########################################################')
                print()
             
             
                tipo_iris = int(input())
                
                if (tipo_iris == 4):
                   menu()
                   
                else:
                    dados = pegarDados (tipo_iris)
                    R,p,R1,p1 = construir_equacao_normal(dados)
                    autovetores, matrizDiagonal = decomposicao_espectral(R)
                    autovetores1, matrizDiagonal1 = decomposicao_espectral(R1)
                    
                    if  (tipo_iris == 1):
                        print("Iris-Setosa\n")
                    elif (tipo_iris == 2):
                        print("Iris-Versicolor\n")
                    elif (tipo_iris == 3):
                        print("Iris-Virginica\n")
                    
                    print("R = V\u039BV^(T)")
                    print()
                    
                    
                    print("SEM O TERMO INDEPENDENTE: ")
                    print("R = ", R)
                    print()
                    print("V = ",autovetores)
                    print()
                    print('\u039B = ',matrizDiagonal)
                    print()
                    print("V^T = ",np.transpose(autovetores))
                    
                    print()
                    print()
                    
                    print("COM O TERMO INDEPENDENTE: ")
                    print("R = ", R1)
                    print()
                    print("V = ", autovetores1)
                    print()
                    print('\u039B = ', matrizDiagonal1)
                    print()
                    print("V^T = ", np.transpose(autovetores1))
                    
                    print()
        
        if (resultado == 3):
             
           while (tipo_iris != 4):
               print('##################### MENU IRIS #############')
               print("Digite qual especie voce deseja fazer o SVD: ")
               print("1 = Iris-Setosa")
               print("2 = Iris-Versicolor")
               print("3 = Iris Virginica")
               print("4 = VOLTAR AO MENU PRINCIPAL")
               print('#############################################')
               print()
             
               tipo_iris = int(input())
              
               if (tipo_iris == 4):
                   menu()
               
               else:
                
                   dados = pegarDados (tipo_iris)
                   R,p,R1,p1 = construir_equacao_normal(dados)
                   U, s, VT = contruir_svd(R)
                   U1, s1, VT1 = contruir_svd(R1)
                   
                   if  (tipo_iris == 1):
                        print("Iris-Setosa\n")
                   elif (tipo_iris == 2):
                        print("Iris-Versicolor\n")
                   elif (tipo_iris == 3):
                        print("Iris-Virginica\n")
                        
                   print("R = U\u03A3V^(T)")
                   print()
                   
                   print("SEM O TERMO INDEPENDENTE: ")
                   print("R = ", R)
                   print()
                   print("U = ", U)
                   print()
                   print('\u03A3 = ', np.diag(s))
                   print()
                   print("V^T = ", VT)
                   print()
                   print()
                    
                   print("COM O TERMO INDEPENDENTE: ")
                   print("R = ", R1)
                   print()
                   print("U = ", U1)
                   print()
                   print('\u03A3 = ', np.diag(s1))
                   print()
                   print("V^T = ", VT1)
                   
                   print()
                   
               
                
        if (resultado == 4):
            A = [5.0,2.3,3.3,1.0]
            B = [4.6,3.2,1.4,0.2]
            C = [5.0,3.3,1.4,0.2]
            D = [6.1,3.0,4.6,1.4]
            E = [5.9,3.0,5.1,1.8]
            
            print("SEM O TERMO INDEPENDENTE: ")
            dados = pegarDados (1)
            R,p,R1,p1 = construir_equacao_normal(dados)
            w_setosa = PLU(R,p)
            
            dados = pegarDados (2)
            R,p,R1,p1 = construir_equacao_normal(dados)
            w_versicolor = PLU(R,p)
        
            dados = pegarDados (3)
            R,p,R1,p1 = construir_equacao_normal(dados)
            w_virginica = PLU(R,p)
            
            c_independente = False
            estimativa = estimar_amostras(A,w_setosa,w_versicolor,w_virginica,c_independente)
            print("A = ", estimativa)
            estimativa = estimar_amostras(B,w_setosa,w_versicolor,w_virginica,c_independente)
            print("B = ", estimativa)
            estimativa = estimar_amostras(C,w_setosa,w_versicolor,w_virginica,c_independente)
            print("C = ", estimativa)
            estimativa = estimar_amostras(D,w_setosa,w_versicolor,w_virginica,c_independente)
            print("D = ", estimativa)
            estimativa = estimar_amostras(E,w_setosa,w_versicolor,w_virginica,c_independente)
            print("E = ", estimativa)
            
            print()
            print("COM O TERMO INDEPENDENTE: ")
            dados = pegarDados (1)
            R,p,R1,p1 = construir_equacao_normal(dados)
            w1_setosa = PLU(R1,p1)
            
            dados = pegarDados (2)
            R,p,R1,p1 = construir_equacao_normal(dados)
            w1_versicolor = PLU(R1,p1)
            
            dados = pegarDados (3)
            R,p,R1,p1 = construir_equacao_normal(dados)
            w1_virginica = PLU(R1,p1)
            
            c_independente = True
            estimativa1 = estimar_amostras(A,w1_setosa,w1_versicolor,w1_virginica,c_independente)
            print("A = ", estimativa1)
            estimativa1 = estimar_amostras(B,w1_setosa,w1_versicolor,w1_virginica,c_independente)
            print("B = ", estimativa1)
            estimativa1 = estimar_amostras(C,w1_setosa,w1_versicolor,w1_virginica,c_independente)
            print("C = ", estimativa1)
            estimativa1 = estimar_amostras(D,w1_setosa,w1_versicolor,w1_virginica,c_independente)
            print("D = ", estimativa1)
            estimativa1 = estimar_amostras(E,w1_setosa,w1_versicolor,w1_virginica,c_independente)
            print("E = ", estimativa1)
            
            menu()
                       
######## chamada ao menu
menu()