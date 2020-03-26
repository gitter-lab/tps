import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
import scipy as sp
import numpy as np

FULL_DATASET = True
# Decide whether to run the old code with the full dataset or the new code
# with selected peptides
if (FULL_DATASET):
    # Load excel file of party processed data
    data_xls = pd.ExcelFile('./data/timeseries/merged_normalized.xlsx')
    
    # Create empty data frame for result data
    result_data = pd.DataFrame()
    
    # Load all of the sheets into a list
    sheet_list = {}
    index = 0
    for sheet_name in data_xls.sheet_names:
        # Load sheet into list
        sheet_list[index] = data_xls.parse(sheet_name)
    
        index += 1
    
    
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
    
    # # Get the data for the stats MulitComparison test
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

    result_data.columns = ['peptide', 'protein', 'gene.name', 'modified.sites', '0min', '2min', '4min', '8min', 
    '16min', '32min', '64min', '128min','0min', '2min', '4min', '8min', 
    '16min', '32min', '64min', '128min','0min', '2min', '4min', '8min', 
    '16min', '32min', '64min', '128min']

    # Calculate medians and log2 fold changes
    medians = pd.DataFrame()
    log2_fold_changes = pd.DataFrame()
    for i in result_data.index:
        # Calculate medians
        m0 = result_data.iloc[i:i+1,4:5] + result_data.iloc[i:i+1,12:13]+ result_data.iloc[i:i+1,20:21]
        m2 = result_data.iloc[i:i+1,5:6] + result_data.iloc[i:i+1,13:14]+ result_data.iloc[i:i+1,21:22]
        m4 = result_data.iloc[i:i+1,6:7] + result_data.iloc[i:i+1,14:15]+ result_data.iloc[i:i+1,22:23]
        m8 = result_data.iloc[i:i+1,7:8] + result_data.iloc[i:i+1,15:16]+ result_data.iloc[i:i+1,23:24]
        m16 = result_data.iloc[i:i+1,8:9] + result_data.iloc[i:i+1,16:17]+ result_data.iloc[i:i+1,24:25]
        m32 = result_data.iloc[i:i+1,9:10] + result_data.iloc[i:i+1,17:18]+ result_data.iloc[i:i+1,25:26]
        m64 = result_data.iloc[i:i+1,10:11] + result_data.iloc[i:i+1,18:19]+ result_data.iloc[i:i+1,26:27]
        m128 = result_data.iloc[i:i+1,11:12] + result_data.iloc[i:i+1,19:20]+ result_data.iloc[i:i+1,27:28]
        # Add medians to median dataframe
        medians[0].append(m0, ignore_index=True)
        medians[1].append(m2, ignore_index=True)
        medians[2].append(m4, ignore_index=True)
        medians[3].append(m8, ignore_index=True)
        medians[4].append(m16, ignore_index=True)
        medians[5].append(m32, ignore_index=True)
        medians[6].append(m64, ignore_index=True)
        medians[7].append(m128, ignore_index=True)
        # Calculate log2 fold changes and add to log2 fold change dataframe
        log2_fold_changes[0].append(np.log2(m0/m0), ignore_index=True)
        log2_fold_changes[1].append(np.log2(m2/m0), ignore_index=True)
        log2_fold_changes[2].append(np.log2(m4/m0), ignore_index=True)
        log2_fold_changes[3].append(np.log2(m8/m0), ignore_index=True)
        log2_fold_changes[4].append(np.log2(m16/m0), ignore_index=True)
        log2_fold_changes[5].append(np.log2(m32/m0), ignore_index=True)
        log2_fold_changes[6].append(np.log2(m64/m0), ignore_index=True)
        log2_fold_changes[7].append(np.log2(m128/m0), ignore_index=True)
    
    
    
    # Run the MultiComparison tests
    for i in result_data.index:
        dframe = pd.DataFrame(result_data.iloc[i:i+1,4:28])
        curr_peptide = dframe.stack().reset_index()
        curr_peptide = curr_peptide.rename(columns={'level_0': 'id','level_1': 'replicate', 0:'result'})
        mComp = MultiComparison(curr_peptide['result'],curr_peptide['replicate'])
        print(mComp.tukeyhsd().pvalues)

    # log2 fold change (2 min) = log2(median at 2 min / median at 0 min)
    # median centering = divide each item in column by the column median (BEFORE TUKEY TEST)
        
    # mComp = MultiComparison(replicates['result'],replicates['replicate'])
    
    # # Add results to table
    # result_data = pd.concat([result_data, pd.DataFrame(mComp.tukeyhsd().pvalues)], axis=1, ignore_index=True)
    # result_data = pd.concat([result_data, pd.DataFrame(mComp.tukeyhsd().meandiffs)], axis=1, ignore_index=True)
    
    # print(mComp.tukeyhsd().summary())

    
    # # Export results to excel sheet
    result_data.to_excel("result.xlsx")

########################################################################################
else:
    # Test Data
    test_data = pd.read_csv('/Users/jack/Downloads/tps-b1623110bd928e693ed33be5ffd8c71a83e3c1ff/data/timeseries/MultiComparison_example.tsv', sep="\t")
    
    #test_replicates = test_data.stack().reset_index()
    #test_replicates = test_replicates.rename(columns={'level_0': 'id','level_1': 'groups', 0:'intensities'})
    
    # Skip median centering for now, requires all peptides, then center per column
    #print(test_data.median())
    # median center the data
    #test_data.iloc[:,0] = test_data.iloc[:,0].apply(lambda x: x-test_data.median())
    
    print(test_data)
    print(test_data['K.n[305.21]SSGSGSSVADERVDY[243.03]VVVDQQK[432.30].T_intensities'])
    
     # Run the MultiComparison test on the test data
    test_mComp = MultiComparison(test_data['K.n[305.21]SSGSGSSVADERVDY[243.03]VVVDQQK[432.30].T_intensities'],test_data['K.n[305.21]SSGSGSSVADERVDY[243.03]VVVDQQK[432.30].T_groups'])
    
    print(test_mComp.tukeyhsd().summary())
