import numpy
import pandas
from sklearn.neighbors import KDTree
from sklearn.preprocessing import StandardScaler

def kdtree_nearest_5_etfs(user_growth, user_std, df, time_horizon, k):
    std_col = f'Standard_Deviation_{time_horizon}Y'
    growth_col = f'Annual_Growth_{time_horizon}Y'

    df_clean = df.dropna(subset=[std_col, growth_col])

    df_clean['_std_flipped'] = -df_clean[std_col]
    df_clean['_growth'] = df_clean[growth_col]
    std_growth_data = df_clean[['_std_flipped', '_growth']].to_numpy()
    scaler = StandardScaler()
    std_growth_data_scaled = scaler.fit_transform(std_growth_data)
    user_point_scaled = scaler.transform([[user_std, user_growth]])

    tree = KDTree(std_growth_data_scaled, leaf_size=20)
    k_actual = min(k, len(df_clean))
    dists, indices = tree.query(user_point_scaled, k=k_actual)

    nearest_etfs = df_clean.iloc[indices[0]].copy()
    nearest_etfs['Distance'] = dists[0]

    return nearest_etfs.sort_values('Distance').reset_index(drop=True)
