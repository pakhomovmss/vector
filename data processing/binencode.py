import pandas as pd

def bin_encoding(dataframe, depths):

    print('RUNNING...\n')

    cols = []

    counter = 0

    for i,col in enumerate(dataframe.columns):
        for depth in range(depths[i]):

            if depths[i] != 1:
                cols.append(col + '_' + str(depth + 1))

            else:
                cols.append(col)


    new_df = pd.DataFrame(columns=cols)

    for line in range(dataframe.shape[0]):
        row = []

        for col, val in enumerate(dataframe.loc[line].values):

            if depths[col] != 1:
                bin_format = bin(val)[2:]
                bin_format = list((depths[col] - len(bin_format)) * '0' + bin_format)

                row += bin_format
            
            else:
                row.append(val)
        
        new_df.loc[line] = row

        counter += 1
        print(counter)

    return new_df