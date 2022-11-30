import streamlit as st
import geemap.foliumap as geemap
import ee
import geemap.colormaps as cm
import geopandas as gpd

geemap.ee_initialize()

@st.cache
def uploaded_file_to_gdf(data):
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    gdf = gpd.read_file(file_path)

    return gdf

st.title("Clip DEM by Country")

col1, col2 = st.columns([6, 4])

countries = ee.FeatureCollection(geemap.examples.get_ee_path('countries'))
style = {"color": "00000088", "width": 1, "fillColor": "00000000"}

options = countries.aggregate_array('NAME').getInfo()
options.sort()

default_country = "United States of America"

options.remove(default_country)
options.insert(0, default_country)
options.insert(1, "Canada")

default_index = options.index("United States of America")

with col2:

    data = st.file_uploader("Upload ROI", type=["geojson"])
    # gdf = uploaded_file_to_gdf(data)

    country = st.selectbox("Select a country", options, index=2)
    min_max = st.slider("Select elevation range", 0, 6000, (100, 3000))
    palette = st.selectbox("Select a color palette", list(cm.palettes.keys()), index=1)

Map = geemap.Map(Draw_export=True)

image = ee.Image('USGS/SRTMGL1_003')
vis_params = {
    'min': min_max[0],
    'max': min_max[1],
    'palette': palette,
}

fc = countries.filter(ee.Filter.eq('NAME', country))
image = image.clipToCollection(fc)

Map.addLayer(image, vis_params, 'SRTM')
Map.centerObject(fc)

Map.add_colorbar(vis_params=vis_params)

Map.addLayer(countries.style(**style), {}, "Countries", False)

# Map.add_gdf(gdf)

with col1:
    Map.to_streamlit(height=400)