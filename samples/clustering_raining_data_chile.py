import os.path
import unittest
import numpy as np
from clust_st import CorClustST
import pandas as pd

try:
    from sklearn.neighbors import DistanceMetric
except ImportError:
    from sklearn.metrics import DistanceMetric


def get_distance_matrix(stations_info_df, stations_of_interest):
    dist_func = DistanceMetric.get_metric('haversine')
    world_radius = 6373
    df_spatial_sample = stations_info_df.loc[stations_of_interest][["latitud", "longitud"]]
    df_spatial_sample_rad = df_spatial_sample.copy()
    df_spatial_sample_rad['latitud'] = np.radians(df_spatial_sample_rad['latitud'])
    df_spatial_sample_rad['longitud'] = np.radians(df_spatial_sample_rad['longitud'])
    dist_matrix = dist_func.pairwise(df_spatial_sample_rad[['latitud', 'longitud']].to_numpy()) * world_radius
    return dist_matrix 


def main():
    print("hola")
    # data load
    precipitations_df = pd.read_csv("./chile_precipitation_clustering_data/chilean_stations_precipitation.csv",
                                    index_col=0, parse_dates=True)
    stations_info_df = pd.read_csv("./chile_precipitation_clustering_data/stations_info.csv",
                                   index_col=1)
    stations_of_interest = pd.Series(precipitations_df.columns.values).apply(int).values

    # create distance matrix
    dist_matrix = get_distance_matrix(stations_info_df, stations_of_interest)

    # create correlation matrix
    corr_matrix = abs(precipitations_df.corr(method="spearman"))

    corclust_st = CorClustST(epsilon=80, rho=0.7)
    corclust_st.fit(dist_matrix, corr_matrix)

    # plots


if __name__ == "__main__":
    main()
