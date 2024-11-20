import streamlit as st
import pandas as pd
import sqlite3
import os
import glob
import folium
from streamlit_folium import st_folium

# Set the page title
st.title("Power Plant and Data Center Locations")
st.write("This application displays power plants and data centers on the same map.")
st.write("Use the filters on the left to filter by power plant type, data center company, or reporting year of power generation.")

# Connect to the SQLite database for power plants
DATABASE = "pudl_subset.sqlite"

@st.cache_data
def load_power_plant_data():
    """
    Load power plant data from the SQLite database and return it as a DataFrame.
    """
    conn = sqlite3.connect(DATABASE)
    query = """
    SELECT 
        plant_name_ferc1,
        utility_name_ferc1,
        city,
        state,
        latitude,
        longitude,
        plant_type,
        net_generation_mwh,
        report_year
    FROM yearly_plant_generation
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@st.cache_data
def load_data_center_data(folder_path):
    """
    Load all CSV files from the data center folder and return a combined DataFrame.
    """
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    data_frames = []
    for file in all_files:
        company_name = os.path.basename(file).split("_")[0].capitalize()
        df = pd.read_csv(file)
        df["Company"] = company_name
        data_frames.append(df)
    combined_df = pd.concat(data_frames, ignore_index=True)
    # Clean data: remove invalid latitude/longitude
    combined_df = combined_df.dropna(subset=["Latitude", "Longitude"])
    combined_df = combined_df[
        combined_df["Latitude"].apply(lambda x: isinstance(x, (int, float))) &
        combined_df["Longitude"].apply(lambda x: isinstance(x, (int, float)))
    ]
    return combined_df

# Load data
power_plant_data = load_power_plant_data()
data_center_folder = "Data_Center_Locations"
data_center_data = load_data_center_data(data_center_folder)

# Group power plant types
plant_type_groups = {
    "Hydro": ["run_of_river", "run_of_river_with_storage", "hydro"],
    "Solar": ["photovoltaic", "solar_thermal"],
    "Fossil Fuels": ["combustion_turbine", "internal_combustion", "fuel_cell"],
    "Nuclear": ["nuclear"],
    "Wind": ["wind"],
    "Geothermal": ["geothermal"],
    "Energy Storage": ["storage"],
    "Steam": ["steam"],
    "Combination": ["combined_cycle"],
}

def group_plant_type(plant_type):
    for group, types in plant_type_groups.items():
        if plant_type in types:
            return group
    return "Other"

power_plant_data["grouped_plant_type"] = power_plant_data["plant_type"].apply(group_plant_type)

# Sidebar Filters
st.sidebar.header("Filter Options")

# Power plant toggles
display_power_plants = st.sidebar.checkbox("Display Power Plants", value=True)
scale_dots = st.sidebar.checkbox("Scale Power Plant Markers by Power Generation Amount", value=True)
color_power_plant_markers = st.sidebar.checkbox("Color Power Plant Markers by Type", value=True)

# Data center toggle
display_data_centers = st.sidebar.checkbox("Display Data Centers", value=True)

# Power plant filters
years = sorted(power_plant_data["report_year"].unique())
selected_year = st.sidebar.selectbox("Select Reporting Year", years)
grouped_plant_types = power_plant_data["grouped_plant_type"].unique()
selected_plant_types = st.sidebar.multiselect("Select Plant Types", grouped_plant_types, default=grouped_plant_types)

# Data center filters
data_center_companies = data_center_data["Company"].unique()
selected_companies = st.sidebar.multiselect("Select Data Center Companies", data_center_companies, default=data_center_companies)

# Filter power plant and data center data
filtered_power_plant_data = power_plant_data[
    (power_plant_data["report_year"] == selected_year) &
    (power_plant_data["grouped_plant_type"].isin(selected_plant_types))
]

filtered_data_center_data = data_center_data[data_center_data["Company"].isin(selected_companies)]

# Color palettes
power_plant_colors = [
    "#F08080", "#D8BFD8", "#98FB98", "#FFDAB9", "#F4A460",
    "#DDA0DD", "#FFE4B5", "#E6E6FA", "#F0E68C", "#C0C0C0"
]
data_center_colors = [
    "#FF0000", "#0000FF", "#008000", "#800080", "#FFA500",
    "#A52A2A", "#00FFFF", "#FFD700", "#00FF00", "#FF69B4",
    "#8B4513", "#4682B4", "#6A5ACD", "#DC143C", "#7FFFD4"
]

power_plant_color_map = {
    plant_type: power_plant_colors[i % len(power_plant_colors)] for i, plant_type in enumerate(grouped_plant_types)
}
data_center_color_map = {
    company: data_center_colors[i % len(data_center_colors)] for i, company in enumerate(data_center_companies)
}

# Display legends in the sidebar
st.sidebar.markdown("### Power Plant Legend")
for plant_type, color in power_plant_color_map.items():
    st.sidebar.markdown(
        f"<span style='background-color:{color};width:15px;height:15px;display:inline-block;margin-right:10px;border-radius:50%;'></span>{plant_type}",
        unsafe_allow_html=True,
    )

st.sidebar.markdown("### Data Center Legend")
for company, color in data_center_color_map.items():
    st.sidebar.markdown(
        f"<span style='background-color:{color};width:15px;height:15px;display:inline-block;margin-right:10px;border-radius:50%;'></span>{company}",
        unsafe_allow_html=True,
    )

# Create a Folium map
st.subheader("Map of Power Plants and Data Centers")
m = folium.Map(location=[38, -92], zoom_start=4, tiles="cartodbdark_matter")

# Add power plants to the map if the toggle is enabled
if display_power_plants:
    for _, row in filtered_power_plant_data.iterrows():
        # Determine marker color based on toggle
        marker_color = (
            power_plant_color_map[row["grouped_plant_type"]]
            if color_power_plant_markers
            else "#4B4B4B"  # Dark gray color
        )
        
        # Scale marker size based on toggle
        marker_size = 5 if not scale_dots else max(5, min(30, row["net_generation_mwh"] / 1_000_000 * 10))
        
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=marker_size,
            popup=folium.Popup(
                f"<b>Plant Name:</b> {row['plant_name_ferc1']}<br>"
                f"<b>Utility:</b> {row['utility_name_ferc1']}<br>"
                f"<b>City:</b> {row['city']}<br>"
                f"<b>State:</b> {row['state']}<br>"
                f"<b>Type:</b> {row['grouped_plant_type']}<br>"
                f"<b>Year:</b> {row['report_year']}<br>"
                f"<b>Generation (MWh):</b> {row['net_generation_mwh']:,}",
                max_width=300
            ),
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.6
        ).add_to(m)

# Add data centers to the map if the toggle is enabled
if display_data_centers:
    for _, row in filtered_data_center_data.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(
                f"<b>Company:</b> {row['Company']}<br>"
                f"<b>City:</b> {row['Location'].split(',')[0]}<br>"
                f"<b>State:</b> {row['Location'].split(',')[1] if ',' in row['Location'] else '-'}<br>"
                f"<b>Country:</b> {row['Country']}<br>"
                f"<b>Continent:</b> {row['Continent']}",
                max_width=300
            ),
            icon=folium.Icon(color="white", icon_color=data_center_color_map[row["Company"]], icon="cloud"),
        ).add_to(m)

# Display the map
st_folium(m, width=800, height=400)
