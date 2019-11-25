import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
import scipy as sp
import numpy as np

# Load excel file of party processed data
data_xls = pd.ExcelFile('/Users/jack/Downloads/example_data/merged_normalized.xlsx')

# Create empty data frame for result data
result_data = pd.DataFrame()

# Load all of the sheets into a list
sheet_list = {}
index = 0
for sheet_name in data_xls.sheet_names:
    # Load sheet into list
    sheet_list[index] = data_xls.parse(sheet_name)

    index += 1

# Create empty result dataframe to return
result_data = pd.DataFrame()

# Get rid of all rows except duplicates
duplicate_data = sheet_list[0][(sheet_list[0]['peptide'].isin(sheet_list[1]['peptide']))].dropna().reset_index(drop=True)
duplicate_data = duplicate_data[(duplicate_data['peptide'].isin(sheet_list[2]['peptide']))].dropna().reset_index(drop=True)

# Trim the duplicate data to just the first four rows (information about peptides)
result_data = duplicate_data.iloc[:,0:4]

# Create variables for the data in A, B, and C
data_A = sheet_list[0][(sheet_list[0]['peptide'].isin(duplicate_data['peptide']))].dropna().reset_index(drop=True)
data_B = sheet_list[1][(sheet_list[1]['peptide'].isin(duplicate_data['peptide']))].dropna().reset_index(drop=True)
data_C = sheet_list[2][(sheet_list[2]['peptide'].isin(duplicate_data['peptide']))].dropna().reset_index(drop=True)

# Add the data from sheets A, B, and C respectively
result_data = pd.concat([result_data, data_A.iloc[:,4:12]], axis=1, ignore_index=True)
result_data = pd.concat([result_data, data_B.iloc[:,4:12]], axis=1, ignore_index=True)
result_data = pd.concat([result_data, data_C.iloc[:,4:12]], axis=1, ignore_index=True)

print(result_data)

# Get the data for the stats MulitComparison test
array_A = np.asarray(data_A.iloc[:,4:12])
array_B = np.asarray(data_B.iloc[:,4:12])
array_C = np.asarray(data_C.iloc[:,4:12])

# Stack the dataframes into one
df = pd.DataFrame()
df_A = pd.DataFrame(array_A)
df_B = pd.DataFrame(array_B)
df_C = pd.DataFrame(array_C)
df = pd.concat([df, df_A], axis=1, ignore_index=True)
df = pd.concat([df, df_B], axis=1, ignore_index=True)
df = pd.concat([df, df_C], axis=1, ignore_index=True)

replicates = df.stack().reset_index()
replicates = replicates.rename(columns={'level_0': 'id','level_1': 'replicate', 0:'result'})

print(replicates)

# Run the MultiComparison test
mComp = MultiComparison(replicates['result'],replicates['replicate'])

# Add results to table
result_data = pd.concat([result_data, pd.DataFrame(mComp.tukeyhsd().pvalues)], axis=1, ignore_index=True)
result_data = pd.concat([result_data, pd.DataFrame(mComp.tukeyhsd().meandiffs)], axis=1, ignore_index=True)

print(mComp.tukeyhsd().summary())

# Export results to excel sheet
result_data.to_excel("result.xlsx")

