import numpy as np
import pandas as pd

import geopandas as gpd
import shapely

file_path = "./data/BND_ADM_DONG_PG.shp"

gdf = gpd.read_file(file_path,encoding='cp949')
gdf_latlng = gdf.to_crs(epsg=4326)

polygon2coords = lambda poligon: poligon.exterior.coords
coords2lng = lambda coords: list(map(lambda coord: coord[0], coords))
coords2lat = lambda coords: list(map(lambda coord: coord[1], coords))


def multipolygon2polygon(poligon):
    if type(poligon) == shapely.geometry.polygon.Polygon:
        return poligon
    elif type(poligon) == shapely.geometry.multipolygon.MultiPolygon:
        return max(poligon.geoms, key=lambda p: p.area)
    else:
        return None
    
df = pd.DataFrame(gdf_latlng)
df['geometry'] = df['geometry'].apply(lambda x : multipolygon2polygon(x))

mean_coord_df = pd.concat(
    [
        df.drop(columns=["geometry"]),
        df["geometry"]
        .apply(
            lambda x: {
                "lat": np.mean(coords2lat(polygon2coords(x))),
                "lng": np.mean(coords2lng(polygon2coords(x))),
            }
        )
        .apply(pd.Series),
    ],
    axis=1,
)
mean_coord_df.to_csv("./mean_coord_df.csv")