import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np


def read_csv():
    df = pd.read_csv(
        'n201807.csv', decimal=',', sep=';', thousands='.',
        low_memory=False, encoding='latin1'
    )
    df = df.rename(columns=str.lower)
    return df

# on cherche le montant en


def get_mean_by_spe(df):
    # on remplace les valeurs négative par des valeurs positive (car un remboursement est forcément positif)
    # j'ai laissé volontairement les outliers
    df['rem_mon'] = df['rem_mon'].abs()
    df = df.groupby(['pre_spe'])['rem_mon'].mean().to_frame().reset_index()
    df = df.rename(columns={"rem_mon": "rem_moy"})
    return df


# on veut le pourcentage de remboursement de chaque spécialité
def get_per_by_spe(df):
    # on remplace les valeurs négative par des valeurs positive (car un remboursement est forcément positif)
    df['rem_mon'] = df['rem_mon'].abs()
    df = (df.groupby(['pre_spe'])['rem_mon'].sum() /
          df['rem_mon'].sum()).to_frame().reset_index()
    df = df.rename(columns={"rem_mon": "rem_tau"})
    return df


if __name__ == "__main__":
    df = read_csv()
    df_mean = get_mean_by_spe(df)
    df_per = get_per_by_spe(df)
    df_new = df_mean.merge(df_per, how='inner', on='pre_spe')
    df = df[['l_pre_spe', 'pre_spe']].drop_duplicates()
    df_final = (df.groupby('l_pre_spe')[
                'pre_spe'].nunique() == 1).to_frame().reset_index()
    df_final = df_final[df_final['pre_spe'] == True]
    df_final = df_final.drop(columns=['pre_spe'])

    df_final = df_final.merge(df, how='inner', on='l_pre_spe')
    df = df.merge(df_new, how='inner', on='pre_spe')
    df.to_csv('new_csv.csv')
