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

printTendency = False  # Set to False to skip printing central tendency measures

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

