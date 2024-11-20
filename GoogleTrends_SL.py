import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from datetime import datetime
import time

# Set the page title
st.title("Generative AI Interest by State - Heat Map")
st.write("This map visualizes interest in Generative AI by state over time using a heat map. Use the slider below to explore how interest has evolved.")

# Load CSV files
@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

# Paths to data files
trends_file_path = "US_Trends_Sorted.csv"
geo_code_file_path = "US_GeoCode.csv"

# Load data
data = load_csv(trends_file_path)
geo_data = load_csv(geo_code_file_path)

# Create a mapping of state names to their latitude and longitude
state_coords = geo_data.set_index("Name")[["latitude", "longitude"]].to_dict(orient="index")

# Transpose the trend data for easier processing
data = data.set_index("State").transpose()

# Convert index to datetime objects
data.index = pd.to_datetime(data.index, format="%m/%d/%Y")

# Convert datetime index to Python `datetime` objects for Streamlit slider
dates = [date.to_pydatetime() for date in data.index]

# Initialize session state for current date
if "current_date_index" not in st.session_state:
    st.session_state.current_date_index = 0

# Add a checkbox to toggle auto-play
auto_play = st.sidebar.checkbox("Auto-Play Slider", value=False)

# Handle auto-play logic
if auto_play:
    st.session_state.current_date_index = (st.session_state.current_date_index + 1) % len(dates)
    time.sleep(1)  # Adjust playback speed (1 second delay)

# Add a slider for selecting the date manually
selected_date = st.slider(
    "Select Date for Heat Map",
    min_value=dates[0],
    max_value=dates[-1],
    value=dates[st.session_state.current_date_index],
)

# Snap the selected date to the nearest valid date in the dataset
nearest_date = min(dates, key=lambda x: abs(x - selected_date))
st.session_state.current_date_index = dates.index(nearest_date)

# Get the data for the nearest date
selected_date_data = data.loc[nearest_date]

# Prepare the heatmap data
heatmap_data = selected_date_data.reset_index()
heatmap_data.columns = ["State", "Interest"]

# Combine interest with state coordinates
heatmap_data["Coordinates"] = heatmap_data["State"].map(state_coords)
heatmap_data = heatmap_data.dropna(subset=["Coordinates"])  # Remove states without coordinates

# Prepare data for HeatMap (latitude, longitude, interest)
heatmap_points = [
    [coord["latitude"], coord["longitude"], interest]
    for coord, interest in zip(heatmap_data["Coordinates"], heatmap_data["Interest"])
]

# Create the Folium map
st.subheader("Generative AI Interest Heat Map")
heatmap_map = folium.Map(location=[38, -92], zoom_start=4, tiles="cartodbdark_matter")

# Add the heat map to the map
HeatMap(heatmap_points, min_opacity=0.4, max_val=100, radius=20, blur=15).add_to(heatmap_map)

# Display the heat map in Streamlit
st_folium(heatmap_map, width=800, height=400)
