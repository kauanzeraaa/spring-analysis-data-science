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

# -------------------------------------------------------------------------------------------------
# Graph visualization
# -------------------------------------------------------------------------------------------------
# Configure a default visual style for the graphs
sb.set_theme(style="whitegrid")

# Define numeric columns excluding 'Id'
cols_graficos = cleaned_df.drop(columns=['Id'], errors='ignore').columns

# Plot distribution of each numeric variable in separate figures
for col in cols_graficos:
    plt.figure(figsize=(8, 5))
    sb.histplot(cleaned_df[col], kde=True, bins=10, color='skyblue')
    plt.title(f"Distribuição da Variável: {col}")
    plt.xlabel(col)
    plt.ylabel("Frequência Absoluta")
    plt.show()

# Compare variation and distribution of all variables in the same figure - With Outliers
plt.figure(figsize=(12, 6))
sb.boxplot(data=numeric_df[cols_graficos], palette="Set2")
plt.title("Boxplot das Variáveis Analisadas Com Outliers")
plt.ylabel("Valores")
plt.xticks(rotation=45) # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

# Compare variation and distribution of all variables in the same figure
plt.figure(figsize=(12, 6))
sb.boxplot(data=cleaned_df[cols_graficos], palette="Set2")
plt.title("Boxplot das Variáveis Analisadas Sem Outliers")
plt.ylabel("Valores")
plt.xticks(rotation=45) # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

# Histogram of 'dutilidade' to visualize its distribution
# if 'dutilidade' in cleaned_df.columns:
#     plt.figure(figsize=(8, 5))
#     sb.histplot(cleaned_df['dutilidade'], kde=True, bins=10, color='teal')
#     plt.title("Distribuição da Dutilidade")
#     plt.xlabel("Dutilidade")
#     plt.ylabel("Frequência Absoluta")
#     plt.show()

# Scatter plot - Altura (t) vs Dutilidade
if 't' in cleaned_df.columns and 'dutilidade' in cleaned_df.columns:
    plt.figure(figsize=(8, 5))
    sb.scatterplot(data=cleaned_df, x='t', y='dutilidade', color='darkred', s=80, alpha=0.7)
    plt.title("Relação: Altura (t) x Dutilidade")
    plt.xlabel("Altura (t)")
    plt.ylabel("Dutilidade")
    plt.show()

# Heatmap of Pearson correlation between variables
plt.figure(figsize=(10, 8))
matriz_correlacao = cleaned_df[cols_graficos].corr()
sb.heatmap(matriz_correlacao, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)
plt.title("Mapa de Calor: Correlação de Pearson entre Variáveis")
plt.tight_layout()
plt.show()