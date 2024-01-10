import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
cleaned_df = pd.read_csv('cleaned_data.csv')
original_df = pd.read_csv('laptop_data.csv')
original_df.drop(columns=['Unnamed: 0'], inplace=True)

def get_recommendations(company, typename, ram, gpu, weight, price, touchscreen, ips, ppi, cpu, ghz, hdd, ssd, os):
    input_data = pd.DataFrame({
        'Company': company,
        'TypeName': typename,
        'Ram': ram,
        'Gpu': gpu,
        'Weight': weight,
        'Price': price,
        'Touchscreen': touchscreen,
        'IPS': ips,
        'PPI': ppi,
        'CPU Name': cpu,
        'GHz': ghz,
        'HDD': hdd,
        'SSD': ssd,
        'os': os
    }, index=[0])
    df1 = pd.concat([cleaned_df, input_data], ignore_index=True)
    df1_dummies = pd.get_dummies(df1, drop_first=True)
    df1_dummies = MinMaxScaler().fit_transform(df1_dummies)
    nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(df1_dummies)
    distances, indices = nbrs.kneighbors(df1_dummies)
    closest = indices[-1][1:]
    return original_df.iloc[closest]