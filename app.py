# app.py - Streamlit + Earth Engine interactive map

import ee
import streamlit as st
import leafmap.foliumap as leafmap
import folium 
import json

def add_ee_layer(self, ee_object, vis_params, name):
    try:
        import geemap.foliumap as geemap
    except:
        import geemap
    geemap.ee_initialize()

    map_id_dict = ee.Image(ee_object).getMapId(vis_params)
    tile_layer = folium.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name=name,
        overlay=True,
        control=True
    )
    tile_layer.add_to(self)

leafmap.Map.add_ee_layer = add_ee_layer

# Authenticate using service account

# Load credentials from Streamlit secrets

credentials = ee.ServiceAccountCredentials(
    st.secrets["earthengine"]["service_account"],
    key_data= st.secrets["earthengine"]["private_key"]
)

ee.Initialize(credentials)

# Page settings
st.set_page_config(layout="wide")
st.title("Deforestation in the Brazilian Amazon Forest - Interactive Map")
st.markdown("Explore how the areas of mining and pasture are geographically connected to the crescent deforestation in the Brazilian Amazon Forest and the native people's lands.")

# Map setup
Map = leafmap.Map(center=[-4, -62], zoom=5, ee=True)
Map.add_basemap("CartoDB.DarkMatter")

# Importing Amazon limits and mask
amazon = ee.FeatureCollection("projects/festive-canto-462512-t1/assets/Limits_amazon")
amazon_geom = amazon.geometry()
SA_mask = ee.Geometry.Rectangle([-90, -65, -25, 20])
SA_feature = ee.Feature(SA_mask)
amazon_mask = SA_feature.difference(amazon_geom, 1)
amazon_mask = ee.FeatureCollection(amazon_mask)
amazon_mask_style = amazon_mask.style(color='000000', width=1, fillColor='6d6d6d99')


# Add indigenous lands
ind_lands = ee.FeatureCollection("projects/festive-canto-462512-t1/assets/tis_poligonais")
ind_lands_style = ind_lands.style(color='8baf2c', fillColor='8baf2c')
clipped_ind_lands = ind_lands_style.clip(amazon_geom)
Map.add_ee_layer(clipped_ind_lands, {}, "Indigenous Lands")

# Add deforestation tiles

amazon = ee.FeatureCollection("projects/festive-canto-462512-t1/assets/Limits_amazon")
amazon_geom = amazon.geometry()

#First Hansen

Hansen_10N_080W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_10N_080W")
clipped_10n_080w = Hansen_10N_080W.clip(amazon_geom)
clipped_10n_080w = clipped_10n_080w.updateMask(clipped_10n_080w.neq(0))

#Second Hansen

Hansen_10S_060W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_10S_060W")
clipped_10s_060w = Hansen_10S_060W.clip(amazon_geom)
clipped_10s_060w = clipped_10s_060w.updateMask(clipped_10s_060w.neq(0))

#Third Hansen

Hansen_00N_080W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_00N_080W")
clipped_00n_080w = Hansen_00N_080W.clip(amazon_geom)
clipped_00n_080w = clipped_00n_080w.updateMask(clipped_00n_080w.neq(0))

#Fourth Hansen

Hansen_10S_070W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_10S_070W")
clipped_10s_070w = Hansen_10S_070W.clip(amazon_geom)
clipped_10s_070w = clipped_10s_070w.updateMask(clipped_10s_070w.neq(0))

#Fifth Hansen

Hansen_10S_050W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_10S_050W")
clipped_10s_050w = Hansen_10S_050W.clip(amazon_geom)
clipped_10s_050w = clipped_10s_050w.updateMask(clipped_10s_050w.neq(0))

#Sixth Hansen

Hansen_00N_060W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_00N_060W")
clipped_00n_060w = Hansen_00N_060W.clip(amazon_geom)
clipped_00n_060w = clipped_00n_060w.updateMask(clipped_00n_060w.neq(0))

#Seventh Hansen

Hansen_10N_070W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_10N_070W")
clipped_10n_070w = Hansen_10N_070W.clip(amazon_geom)
clipped_10n_070w = clipped_10n_070w.updateMask(clipped_10n_070w.neq(0))

#Eigth Hansen

Hansen_10N_060W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_10N_060W")
clipped_10n_060w = Hansen_10N_060W.clip(amazon_geom)
clipped_10n_060w = clipped_10n_060w.updateMask(clipped_10n_060w.neq(0))

#Ninth Hansen

Hansen_00N_050W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_00N_050W")
clipped_00n_050w = Hansen_00N_050W.clip(amazon_geom)
clipped_00n_050w = clipped_00n_050w.updateMask(clipped_00n_050w.neq(0))

#Tenth Hansen

Hansen_00N_070W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_lossyear_00N_070W")
clipped_00n_070w = Hansen_00N_070W.clip(amazon_geom)
clipped_00n_070w = clipped_00n_070w.updateMask(clipped_00n_070w.neq(0))

#11th Hansen

Hansen_10S_080W = ee.Image("projects/festive-canto-462512-t1/assets/Hansen_10S_080W")
clipped_10s_080w = Hansen_10S_080W.clip(amazon_geom)
clipped_10s_080w = clipped_10s_080w.updateMask(clipped_10s_080w.neq(0))

for img, name in zip([clipped_10n_080w, clipped_10s_060w, clipped_00n_080w,
                      clipped_10s_070w,clipped_10s_050w, clipped_00n_060w,
                      clipped_10n_070w, clipped_10n_060w, clipped_00n_050w,
                      clipped_00n_070w, clipped_10s_080w],
                     ["Deforestation_10n_080w", "Deforestation_10s_060w", "Deforestation_00n_080w",
                      "Deforestation_10s_070w", "Deforestation_10s_050w", "Deforestation_00n_060w",
                      "Deforestation_10n_070w", "Deforestation_10n_060w", "Deforestation_00n_050w",
                      "Deforestation_00n_070w","Deforestation_10s_080w"]):
    Map.add_ee_layer(img, {'palette': 'ffffff'}, name)

# Add mining layer
mining_file = ee.Image("projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_mined_substance_v1")
mining = mining_file.select('mined_substance_2023')
mining_masked = mining.updateMask(mining.neq(0))
sampled = mining_masked.stratifiedSample(
    numPoints=500,
    classBand='mined_substance_2023',
    region=mining.geometry(),
    scale=60,
    geometries=True,
    seed=42
)
sampled_amazon = sampled.filterBounds(amazon_geom)
palette_dict = ee.Dictionary({
    102: 'f4a582', 103: 'f4a582', 104: 'f4a582', 108: 'f4a582', 109: 'f4a582',
    110: 'f4a582', 111: 'f4a582', 114: 'f4a582', 115: 'f4a582', 117: '6019ae',
    122: '6019ae', 124: '0571b0', 125: '0571b0', 202: 'e66101', 214: 'e66101',
    215: 'e66101', 217: 'fdb863', 224: 'a62b63', 225: 'a62b63'
})
def style_feature(f):
    cls = f.get('mined_substance_2023')
    color = palette_dict.get(cls, 'ff0000')
    return f.set('style', {
        'color': color,
        'pointSize': 4,
        'pointShape': 'circle'
    })
styled_sampled = sampled_amazon.map(style_feature)


# Add pasture layer
pasture = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_pasture_detection_year_v1')
vis_params = {
    'min': 1985,
    'max': 2022,
    'palette': [
        'ffffcc', 'ffeda0', 'fed976', 'feb24c', 'fd8d3c',
        'fc4e2a', 'e31a1c', 'bd0026', '800026'
    ]
}
Map.add_ee_layer(pasture, vis_params, "Agriculture Pasture")
Map.add_ee_layer(styled_sampled.style(styleProperty='style'), {}, "Mining Areas")
Map.add_ee_layer(amazon_mask_style, {}, "Map Mask")

# Add legend to sidebar
legend_html = '''
<div style="background-color:white;padding:10px;border-radius:5px; font-size:13px;">
  <b>Legend for Layers</b><br><br>
  <b> Basic Layers</b><br>
  <span style="display:inline-block;width:12px;height:12px;background:#8baf2c;border:1px solid black;"></span> Indigenous Lands<br>
  <span style="display:inline-block;width:12px;height:12px;background:#ffffff;border:1px solid black;"></span> Deforestation<br><br>

  <b> Mining Activities</b><br>
  <span style="display:inline-block;width:10px;height:10px;background:#f4a582;border:1px solid black;border-radius:50%;"></span> Industrial Mining – Metals<br>
  <span style="display:inline-block;width:10px;height:10px;background:#6019ae;border:1px solid black;border-radius:50%;"></span> Industrial Mining – Non-Metal<br>
  <span style="display:inline-block;width:10px;height:10px;background:#0571b0;border:1px solid black;border-radius:50%;"></span> Industrial Mining – Precious Stones<br>
  <span style="display:inline-block;width:10px;height:10px;background:#e66101;border:1px solid black;border-radius:50%;"></span> Artisanal Mining – Metals<br>
  <span style="display:inline-block;width:10px;height:10px;background:#fdb863;border:1px solid black;border-radius:50%;"></span> Artisanal Mining – Non-Metal<br>
  <span style="display:inline-block;width:10px;height:10px;background:#a62b63;border:1px solid black;border-radius:50%;"></span> Artisanal Mining – Precious Stones<br><br>

  <b> Pasture</b><br>
  <span style="display:inline-block;width:12px;height:12px;background:#ffffcc;border:1px solid black;"></span> Pasture from 1990<br>
  <span style="display:inline-block;width:12px;height:12px;background:#800026;border:1px solid black;"></span> Pasture from 2020<br>
</div>
'''
with st.sidebar:
    st.markdown(legend_html, unsafe_allow_html=True)

# Show mapstreamlit run app.py
Map.to_streamlit(height=700)
