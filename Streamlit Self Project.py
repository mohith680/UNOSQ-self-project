import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Load your data
df = pd.read_csv("C:/Users/MOHITH VARMA/Downloads/unosq_processed_data (1).csv")
df['State'] = df['State'].str.lower()

# Fix mismatches between CSV and GeoJSON
df['State'] = df['State'].replace({
    'chattisgarh': 'chhattisgarh',
    'jammu & kashmir': 'jammu and kashmir'
})
# Count participants per state
state_counts = df['State'].value_counts().reset_index()
state_counts.columns = ['State', 'num_participants']

# Merge with original state names
df_map = state_counts.copy()

# Optional: normalize names
df_map['State'] = df_map['State'].str.lower()

# Load GeoJSON
url = "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@bcbcba3/geojson/india.geojson"
geojson = requests.get(url).json()

# Normalize state names in GeoJSON
for feature in geojson['features']:
    feature['properties']['st_nm'] = feature['properties']['st_nm'].lower()

# Plot using num_participants
fig = px.choropleth(
    df_map,
    geojson=geojson,
    locations='State',
    featureidkey='properties.st_nm',
    color='num_participants',  # ✅ Now this exists
    hover_name='State',
    color_continuous_scale='YlGnBu',
    title='UNOSQ Participants by State',
    projection='mercator'
)

fig.update_geos(fitbounds="locations", visible=True, showcountries=True, countrycolor="black")
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)
