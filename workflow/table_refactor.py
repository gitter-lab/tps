
import pandas as pd
import numpy as np

def refactor_col_delim(annotations_df, col_name):
    '''
    Function used for changing cloumn types of annotaions df

    :param annotations_df (DataFrame): global annptaions dataframe 
    :param col_name (String): name of column to refactor

    '''
    new_col = []
    for row in annotations_df[col_name]:

        if np.all(pd.isnull(row)):
            new_col.append(np.nan)
            continue
        elif row == "Not active":
            print("not active")
            new_col.append(row)
            continue
        else:
            temp_list = row.split(",")
            for num in range(len(temp_list)):
                temp_list[num] = str(float(temp_list[num]))
            new_col.append("|".join(temp_list))
    
    new_df = pd.Series(new_col)
    return new_df

def refactor_col_delim_heat(annotations_df, col_name):
    '''
    Function used for changing cloumn types of annotaions df

    :param annotations_df (DataFrame): global annptaions dataframe 
    :param col_name (String): name of column to refactor

    '''
    new_col = []
    for row in annotations_df[col_name]:

        if np.all(pd.isnull(row)):
            new_col.append(np.nan)
            continue
        elif row == "Not active":
            print("not active")
            new_col.append(row)
            continue
        else:
            temp_list = row.split(",")
            for num in range(len(temp_list)):
                temp_list[num] = str(int(temp_list[num]))
            new_col.append("|".join(temp_list))
    
    new_df = pd.Series(new_col)
    return new_df
    