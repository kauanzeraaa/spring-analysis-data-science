# Load libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import openpyxl  # excel support library
import statistics as stats

# Configure terminal display settings for Pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

# -------------------------------------------------------------------------------------------------
# Data Entry
# -------------------------------------------------------------------------------------------------
file_name = "Springs.xlsx"
data_df = pd.read_excel(file_name, sheet_name="Página1", header=0, usecols="A:J")
data_dict = data_df.to_dict('list')  # transform xlsx data into dictionary

# -------------------------------------------------------------------------------------------------
# Data Analysis
# -------------------------------------------------------------------------------------------------
# Calculate the mean of each column
mean_dict = {}
for col, values in data_dict.items():
    if col != 'Id':
        mean_dict[col] = np.mean(values)

# Calculate the mode of each column
mode_dict = {}
for col, values in data_dict.items():
    if col != "Id":
        mode_dict[col] = stats.mode(values)

# Calculate the median of each column
median_dict = {}
for col, values in data_dict.items():
    if col != 'Id':
        median_dict[col] = stats.median(values)

# Outlier Filtering (IQR per column, excluding 'Id')
numeric_df = data_df.drop(columns=['Id'], errors='ignore')

# 1st and 3rd quartiles per numeric column
Q1 = numeric_df.quantile(0.25)
Q3 = numeric_df.quantile(0.75)
DQ = Q3 - Q1  # Interquartile range (IQR)

lower_limit = Q1 - 1.5 * DQ
upper_limit = Q3 + 1.5 * DQ

# Filter rows keeping only those within [lower_limit, upper_limit] for all numeric columns
is_inlier = ((numeric_df >= lower_limit) & (numeric_df <= upper_limit)).all(axis=1)
cleaned_df = data_df[is_inlier]

# -------------------------------------------------------------------------------------------------
# Show Results
# -------------------------------------------------------------------------------------------------

printTendency = True  # Set to False to skip printing central tendency measures

if printTendency:
    # Summary table of central tendency
    summary_df = pd.DataFrame({
        'Média': mean_dict,
        'Mediana': median_dict,
        'Moda': mode_dict
    })

    print("=" * 70)
    print("              MEDIDAS DE TENDÊNCIA CENTRAL (POR COLUNA)")
    print("=" * 70)
    print(summary_df)

    print("\n" + "=" * 70)
    print("             ESTATÍSTICAS DESCRITIVAS - DADOS BRUTOS")
    print("=" * 70)
    print(numeric_df.describe())

    print("\n" + "=" * 70)
    print(f"            ESTATÍSTICAS DESCRITIVAS - DADOS LIMPOS")
    print("=" * 70)
    print(cleaned_df.drop(columns=['Id'], errors='ignore').describe())

# apresentação dos gráficos

# padroniza o estilo dos gráficos
sb.set_theme(style="whitegrid", font_scale=1.05)
cols_graficos = numeric_df.columns

# boxplot geral de todas as variáveis com Outliers
plt.figure(figsize=(11, 5))
sb.boxplot(
    data=numeric_df[cols_graficos],
    color='#cbd5e1',
    width=0.45,
    fliersize=5,
    boxprops=dict(edgecolor='#334155'),
    whiskerprops=dict(color='#334155'),
    capprops=dict(color='#334155'),
    medianprops=dict(color='#0f172a', linewidth=1.6)
)
plt.title("Boxplot Geral das Variáveis Analisadas (Com Outliers)", fontweight='bold', pad=12)
plt.xlabel("Variáveis")
plt.ylabel("Valores")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# histogramas gerais: Rigidez e Ductilidade
plt.figure(figsize=(7.5, 4.5))
sb.histplot(cleaned_df['rigidez'], kde=True, bins=6, color='#2563eb', edgecolor='white', alpha=0.65)
media_k = cleaned_df['rigidez'].mean()
mediana_k = cleaned_df['rigidez'].median()
plt.axvline(media_k, color='#dc2626', linestyle='--', linewidth=1.5, label=f"Média: {media_k:.3f}")
plt.axvline(mediana_k, color='#047857', linestyle=':', linewidth=1.5, label=f"Mediana: {mediana_k:.3f}")
plt.title("Distribuição de Frequência da Rigidez", fontweight='bold', pad=12)
plt.xlabel("Rigidez")
plt.ylabel("Frequência Absoluta")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(7.5, 4.5))
sb.histplot(cleaned_df['dutilidade'], kde=True, bins=6, color='#2563eb', edgecolor='white', alpha=0.65)
media_d = cleaned_df['dutilidade'].mean()
mediana_d = cleaned_df['dutilidade'].median()
plt.axvline(media_d, color='#dc2626', linestyle='--', linewidth=1.5, label=f"Média: {media_d:.2f}")
plt.axvline(mediana_d, color='#047857', linestyle=':', linewidth=1.5, label=f"Mediana: {mediana_d:.2f}")
plt.title("Distribuição de Frequência da Ductilidade", fontweight='bold', pad=12)
plt.xlabel("Ductilidade")
plt.ylabel("Frequência Absoluta")
plt.legend()
plt.tight_layout()
plt.show()

# mapa de Calor - correlação de Pearson
plt.figure(figsize=(9, 7.5))
matriz_correlacao = cleaned_df[cols_graficos].corr()
sb.heatmap(
    matriz_correlacao,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5,
    vmin=-1,
    vmax=1
)
plt.title("Mapa de Calor: Correlação de Pearson entre Variáveis", fontweight='bold', pad=12)
plt.tight_layout()
plt.show()

# análise mais detalhada da Rigidez vs. (n, L, t)
# rigidez x n (Número de Espiras)

# boxplot
plt.figure(figsize=(7, 4.5))
sb.boxplot(data=cleaned_df, x='n', y='rigidez', color='#93c5fd', width=0.45)
sb.stripplot(data=cleaned_df, x='n', y='rigidez', color='#0f172a', size=6, jitter=0.1, alpha=0.8)
plt.title("Boxplot: Rigidez por Número de Espiras (n)", fontweight='bold', pad=12)
plt.xlabel("Número de Espiras (n)")
plt.ylabel("Rigidez")
plt.tight_layout()
plt.show()

# dispersão
plt.figure(figsize=(7, 4.5))
sb.scatterplot(data=cleaned_df, x='n', y='rigidez', color='#2563eb', s=80, alpha=0.85, edgecolor='black')
plt.title("Dispersão: Rigidez x Número de Espiras (n) [r = -0.70]", fontweight='bold', pad=12)
plt.xlabel("Número de Espiras (n)")
plt.ylabel("Rigidez")
plt.tight_layout()
plt.show()

# histograma
plt.figure(figsize=(7.5, 4.5))
sb.histplot(data=cleaned_df, x='rigidez', hue='n', palette='Blues_r', multiple='stack', bins=6, edgecolor='white')
plt.title("Histograma: Distribuição da Rigidez por Número de Espiras (n)", fontweight='bold', pad=12)
plt.xlabel("Rigidez")
plt.ylabel("Frequência Absoluta")
plt.tight_layout()
plt.show()

# rigidz x L (Comprimento do Passo)
# boxplot
plt.figure(figsize=(7, 4.5))
sb.boxplot(data=cleaned_df, x=cleaned_df['L'].round(), y='rigidez', color='#93c5fd', width=0.45)
sb.stripplot(data=cleaned_df, x=cleaned_df['L'].round(), y='rigidez', color='#0f172a', size=6, jitter=0.1, alpha=0.8)
plt.title("Boxplot: Rigidez por Comprimento do Passo (L)", fontweight='bold', pad=12)
plt.xlabel("Comprimento do Passo L (mm)")
plt.ylabel("Rigidez")
plt.tight_layout()
plt.show()

# dispersão
plt.figure(figsize=(7, 4.5))
sb.scatterplot(data=cleaned_df, x='L', y='rigidez', color='#2563eb', s=80, alpha=0.85, edgecolor='black')
plt.title("Dispersão: Rigidez x Comprimento do Passo (L) [r = -0.71]", fontweight='bold', pad=12)
plt.xlabel("Comprimento do Passo L (mm)")
plt.ylabel("Rigidez")
plt.tight_layout()
plt.show()

# histograma
grupo_L = pd.cut(cleaned_df['L'], bins=[0, 20, 30, 50], labels=['15 mm', '23 mm', '32-40 mm'])
plt.figure(figsize=(7.5, 4.5))
sb.histplot(data=cleaned_df, x='rigidez', hue=grupo_L, palette='Blues_r', multiple='stack', bins=6, edgecolor='white')
plt.title("Histograma: Distribuição da Rigidez por Faixas de Comprimento (L)", fontweight='bold', pad=12)
plt.xlabel("Rigidez")
plt.ylabel("Frequência Absoluta")
plt.tight_layout()
plt.show()

# rigidez x t (Altura da Mola)
# boxplot
plt.figure(figsize=(7, 4.5))
sb.boxplot(data=cleaned_df, x=cleaned_df['t'].round(), y='rigidez', color='#93c5fd', width=0.45)
sb.stripplot(data=cleaned_df, x=cleaned_df['t'].round(), y='rigidez', color='#0f172a', size=6, jitter=0.1, alpha=0.8)
plt.title("Boxplot: Rigidez por Altura da Mola (t)", fontweight='bold', pad=12)
plt.xlabel("Altura da Mola t (mm)")
plt.ylabel("Rigidez")
plt.tight_layout()
plt.show()

# dispersão
plt.figure(figsize=(7, 4.5))
sb.scatterplot(data=cleaned_df, x='t', y='rigidez', color='#2563eb', s=80, alpha=0.85, edgecolor='black')
plt.title("Dispersão: Rigidez x Altura da Mola (t) [r = +0.50]", fontweight='bold', pad=12)
plt.xlabel("Altura da Mola t (mm)")
plt.ylabel("Rigidez")
plt.tight_layout()
plt.show()

# histograma
grupo_t = pd.cut(cleaned_df['t'], bins=[0, 6, 8, 12], labels=['t <= 6 mm', 't = 8 mm', 't = 10 mm'])
plt.figure(figsize=(7.5, 4.5))
sb.histplot(data=cleaned_df, x='rigidez', hue=grupo_t, palette='Blues_r', multiple='stack', bins=6, edgecolor='white')
plt.title("Histograma: Distribuição da Rigidez por Altura da Mola (t)", fontweight='bold', pad=12)
plt.xlabel("Rigidez")
plt.ylabel("Frequência Absoluta")
plt.tight_layout()
plt.show()


# análise mais detalhada da Ductilidadde vs. (n, L, t)
# ductilidade vs. (h, L)

# ductilidade x h (Espessura do Fio)
# boxplot
plt.figure(figsize=(7, 4.5))
sb.boxplot(data=cleaned_df, x=cleaned_df['h'].round(1), y='dutilidade', color='#cbd5e1', width=0.45)
sb.stripplot(data=cleaned_df, x=cleaned_df['h'].round(1), y='dutilidade', color='#0f172a', size=6, jitter=0.1, alpha=0.8)
plt.title("Boxplot: Ductilidade por Espessura do Fio (h)", fontweight='bold', pad=12)
plt.xlabel("Espessura do Fio h (mm)")
plt.ylabel("Ductilidade")
plt.tight_layout()
plt.show()

# dispersão
plt.figure(figsize=(7, 4.5))
sb.scatterplot(data=cleaned_df, x='h', y='dutilidade', color='#2563eb', s=80, alpha=0.85, edgecolor='black')
plt.title("Dispersão: Ductilidade x Espessura do Fio (h) [r = -0.66]", fontweight='bold', pad=12)
plt.xlabel("Espessura do Fio h (mm)")
plt.ylabel("Ductilidade")
plt.tight_layout()
plt.show()

# histograma
grupo_h = pd.cut(cleaned_df['h'], bins=[0, 1.8, 2.5, 4.0], labels=['h ~ 1.5 mm', 'h ~ 2.0 mm', 'h ~ 3.0 mm'])
plt.figure(figsize=(7.5, 4.5))
sb.histplot(data=cleaned_df, x='dutilidade', hue=grupo_h, palette='Blues_r', multiple='stack', bins=6, edgecolor='white')
plt.title("Histograma: Distribuição da Ductilidade por Espessura do Fio (h)", fontweight='bold', pad=12)
plt.xlabel("Ductilidade")
plt.ylabel("Frequência Absoluta")
plt.tight_layout()
plt.show()

# ductilidade x L (Comprimento do Passo)
# boxplot
plt.figure(figsize=(7, 4.5))
sb.boxplot(data=cleaned_df, x=cleaned_df['L'].round(), y='dutilidade', color='#cbd5e1', width=0.45)
sb.stripplot(data=cleaned_df, x=cleaned_df['L'].round(), y='dutilidade', color='#0f172a', size=6, jitter=0.1, alpha=0.8)
plt.title("Boxplot: Ductilidade por Comprimento do Passo (L)", fontweight='bold', pad=12)
plt.xlabel("Comprimento do Passo L (mm)")
plt.ylabel("Ductilidade")
plt.tight_layout()
plt.show()

# dispersão
plt.figure(figsize=(7, 4.5))
sb.scatterplot(data=cleaned_df, x='L', y='dutilidade', color='#2563eb', s=80, alpha=0.85, edgecolor='black')
plt.title("Dispersão: Ductilidade x Comprimento do Passo (L) [r = +0.09]", fontweight='bold', pad=12)
plt.xlabel("Comprimento do Passo L (mm)")
plt.ylabel("Ductilidade")
plt.tight_layout()
plt.show()

# histograma
plt.figure(figsize=(7.5, 4.5))
sb.histplot(data=cleaned_df, x='dutilidade', hue=grupo_L, palette='Blues_r', multiple='stack', bins=6, edgecolor='white')
plt.title("Histograma: Distribuição da Ductilidade por Faixas de Comprimento (L)", fontweight='bold', pad=12)
plt.xlabel("Ductilidade")
plt.ylabel("Frequência Absoluta")
plt.tight_layout()
plt.show()
