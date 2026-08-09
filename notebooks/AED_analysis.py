import geopandas as gpd

file = "../data/PublicAccessAEDs.geojson"

aed = gpd.read_file(file)

aed.head()
b