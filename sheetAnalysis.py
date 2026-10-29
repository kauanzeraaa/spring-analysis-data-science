# Load libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import openpyxl # excel support library

# Entrada de dados
file_name = "Springs.xlsx"
data_df = pd.read_excel(file_name, sheet_name="Página1",header=0, usecols="A:J")
data_dict = data_df.to_dict('list') # transform xlsx data into dictonary

# print(data_df) - show table format
# print(data_dict) - show dict format

# Processing data
# Calculate boxplot variables

# Show results
# Draw result graphs

# plt.scatter(data_dict['C'], data_dict['dutilidade']) # spring length X dutilidade
# plt.title("Spring length X dutilidade")
# plt.xlabel("Spring Lengh (C)")
# plt.ylabel("Dutilidade")
# plt.show()

plt.scatter(data_dict['t'], data_dict['dutilidade']) # spring heigh X dutilidade
plt.title("Spring heigh X dutilidade")
plt.xlabel("Spring Lengh (T)")
plt.ylabel("Dutilidade")
plt.show()