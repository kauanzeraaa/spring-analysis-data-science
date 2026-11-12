# Carregamento das bibliotecas
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stats
import seaborn as sb

# Entrada de dados
data_dict = {
  "Potencia": [130,81,93,113,90,63,55,102,92,81,103,90,74,73,102,78,100,125],
  "Consumo": [10.1,10.5,11.3,10.5,11.6,12.4,15.0,11.3,12.4,12.0,10.9,11.6,12.4,13.1,10.9,12.0,10.5,5.0]
}

# Processamento dos dados

# Regressão Linear para um modelo de 1a ordem (linha)
coeficiente = np.polyfit(data_dict["Potencia"], data_dict["Consumo"], deg=1)

a = coeficiente[0]
b = coeficiente[1]

# Teste do modelo com os dados
x_previsao = [60.0, 120.0, 130.0]
y_modelo = [
  a * 60.0 + b,
  a * 120.0 + b,
  a * 130.0 + b
]

# Regressão Linear para um modelo de 2a ordem (quadratico)
coeficiente_quad = np.polyfit(data_dict["Potencia"], data_dict["Consumo"], deg=2)

a_quad = coeficiente_quad[0]
b_quad = coeficiente_quad[1]
c_quad = coeficiente_quad[2]

# Teste do modelo quadratico
x_mod2 = np.array([30.0, 50.0, 90.0, 120.0])
y_mod2 = a_quad * x_mod2 ** 2 + b_quad * x_mod2 + c_quad

dados_previstos = a * np.array(data_dict['Potencia']) + b
matriz_pearson = [data_dict['Consumo'], dados_previstos]
corr = np.corrcoef(matriz_pearson)
print("R2 = ", corr[0,1] ** 2)

dados_previstos2 = a_quad * np.array(data_dict["Potencia"]) ** 2 + b_quad * np.array(data_dict["Potencia"]) + c_quad
matriz_pearson2 = [data_dict["Consumo"], dados_previstos2]
corr_linear2 = np.corrcoef(matriz_pearson2)
print("R2_quad = ", corr_linear2[0,1] ** 2)

Res = data_dict["Consumo"] - dados_previstos

# Apresentação dos resultados
plt.figure(figsize=(7, 4.5))
sb.scatterplot(data=data_dict, x='Potencia', y='Consumo', color='#2563eb', s=80, alpha=0.85, edgecolor='black')
plt.plot(x_previsao, y_modelo)
plt.plot(x_mod2, y_mod2)
plt.title("Dispersão: Potencia x Consumo", fontweight='bold', pad=12)
plt.xlabel("Potencia (HP)")
plt.ylabel("Consumo (km/L)")
plt.tight_layout()
plt.show()

plt.boxplot(Res)
plt.show()