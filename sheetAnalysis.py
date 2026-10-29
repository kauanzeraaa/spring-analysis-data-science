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


# Show results