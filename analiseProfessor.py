# Carregamento das bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# OBS: caso não rode, verifique se o pacote openpyxl foi instalado


# Entrada de dados
arquivo = "experimentoProfessor.xlsx"    # nome do arquivo do Excel
tabela1_original = pd.read_excel(arquivo, sheet_name="tabela1", header=1, usecols="B:I")     # Lê como um dataframe
tabela1_dict = tabela1_original.to_dict('list')     # Converte para um dataframe

tabela2_original = pd.read_excel(arquivo, sheet_name="tabela2", header=1, usecols="B:F")     # Lê como um dataframe
tabela2_dict = tabela2_original.to_dict('list')     # Converte para um dataframe


# Processamento dos dados

# Calculo da rigidez media de cada mola
# a) adição de uma coluna vazia a mais no DICT da tabela1 p/ guardar a rigidez
tabela1_dict["K"] = []

# b) calculo da rigidez média de cada mola testada
qtd_linhas = len(tabela2_dict["ID"])
contador = range(qtd_linhas)
rigidez_media = {"ID": [],
                 "K": []}
ID_mola = -1    # valor de partida para um ID não existente
index = 0       # indice de contagem de quantas molas forma adicionadas
soma_rigidez = 0.0  # acumulador para a media
for i in contador:
    if (ID_mola == -1):
        ID_mola = tabela2_dict["ID"][i]         # primeira mola calculada
    elif (tabela2_dict["ID"][i] != ID_mola):    # nova mola, então armazena os últimos cálculos
        rigidez_media["ID"].append(ID_mola)
        valor_medio = soma_rigidez/5.0          # faz a média, sempre supõe que cinco números estão disponíveis.
        rigidez_media["K"].append(valor_medio)  # armazena a média
        soma_rigidez = 0.0                      # zera o acumulador
        ID_mola = tabela2_dict["ID"][i]         # atualiza o ID da próxima mola

    soma_rigidez = soma_rigidez + tabela2_dict["rigidez"][i]
# Adiciona a ultima mola
rigidez_media["ID"].append(ID_mola)
valor_medio = soma_rigidez / 5.0
rigidez_media["K"].append(valor_medio)

# c) Carrega os valores para a tabela1 completa
# OBS: o laço duplo foi feito, pois não necessariamente
# os IDs estão em ordem
tam = len(rigidez_media["ID"])
contador = range(tam)
contador2 = range(tam)
pos = 0
for i in contador:
    ID_atual = rigidez_media["ID"][i]
    for j in contador2:
        if ID_atual == tabela1_dict["ID"][j]:
            tabela1_dict["K"].append(rigidez_media["K"][i])
            break

# OBS: a partir desse ponto, pode-se fazer o mesmo para os
# intervalos de confiança da rigidez e também para a dutilidade.

# OBS: pode-se construir os boxplots em função de alguma variável
# OBS: pode-se construir os gráficos de dispersão


# Apresentação dos resultados
print("\nApresentação do dicionário lido - tabela1: ")
print(tabela1_dict)
print("\nApresentação do dicionário lido - tabela2: ")
print(tabela2_dict)

# Grafico de dispersão da rigidez em função da altura t
plt.scatter(tabela1_dict["t"], tabela1_dict["K"])
plt.title("Dispersão da rigidez em função da altura")
plt.xlabel("Altura da mola (t)")
plt.ylabel("Rigidez da mola (K)")
plt.show()