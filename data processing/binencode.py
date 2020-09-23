import numpy as np
import pandas as pd

df = pd.DataFrame({'A' : [90,45,76,36,29,99,54], 'B' : [86,23,62,31,4,20,13], 'C' : [33,17,28,1,3,14,61]})

def bin_encoding(dataframe, depths):

    cols = []

    for i,col in enumerate(dataframe.columns):
        for depth in range(depths[i]):

            if depths[i] != 1:
                cols.append(col + '_' + str(depth + 1))

            else:
                cols.append(col)


    new_df = pd.DataFrame(columns=cols)

    # append values to the DataFrame

    #new_df.loc[0, 'A_1'] = 5
    
    for i,col in enumerate(dataframe.columns):
        if depths[i] != 1:
            for val in dataframe[col]:
                bin_format = bin(val)[2:]
                bin_format = (depths[i] - len(bin_format)) * '0' + bin_format

                for num in range(depths[i]):
                    new_df.loc[i, col + '_' + str(num + 1)] = bin_format[num]

        else:
            new_df[col] = dataframe[col]

    return new_df


print(bin_encoding(df, [7, 7, 7]))