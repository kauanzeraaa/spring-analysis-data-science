# Load libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import openpyxl # excel support library
import statistics as stats

# -------------------------------------------------------------------------------------------------
# Data Entry
# -------------------------------------------------------------------------------------------------
file_name = "Springs.xlsx"
data_df = pd.read_excel(file_name, sheet_name="Página1",header=0, usecols="A:J")
data_dict = data_df.to_dict('list') # transform xlsx data into dictonary

# -------------------------------------------------------------------------------------------------
# Data Analysis
# -------------------------------------------------------------------------------------------------
# Calculate the mean off each column
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

# -------------------------------------------------------------------------------------------------
# Show Results
# -------------------------------------------------------------------------------------------------

# Show Mean results
#    for i, value in mean_dict.items():
#        print(f"Média de {i}: {value}")

# Show Mode results
#    for i, value in mode_dict.items():
#        print(f"Moda de {i}: {value}")

# Show Median results
#    for i, value in median_dict.items():
#        print(f"Mediana de {i}: {value}")