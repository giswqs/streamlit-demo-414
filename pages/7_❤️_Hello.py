import streamlit as st
import geemap.foliumap as geemap
import ee


st.sidebar.title("Hello")

st.title('My Heart is with you')

m = geemap.Map(
    center=[40, -100],
    zoom=4,
    draw_control=False,
    measure_control=False,
    scale_control=False,
)
m.split_map(left_layer='ESA WorldCover 2021', right_layer='NLCD 2019 CONUS Land Cover')



col1, col2 = st.columns([6, 4])

with col2:

    options = st.multiselect("Select legends", ["NLCD 2019 CONUS Land Cover", "ESA WorldCover 2021"],)

    if "ESA WorldCover 2021" in options:

        m.add_legend(
            title='ESA Land Cover Type',
            builtin_legend='ESA_WorldCover',
            draggable=False,
            position='bottomleft',
            style={'bottom': '5px'},
        )

    

    if "NLCD 2019 CONUS Land Cover" in options:

        m.add_legend(
            title='NLCD Land Cover Type',
            builtin_legend='NLCD',
            draggable=False,
            position='bottomright',
        )

with col1:
    m.to_streamlit()

