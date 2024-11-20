import streamlit as st
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium

# Set the page title and layout
st.title("Power Plants Visualization")
st.write("This app visualizes power plants based on their location, type, and generation capacity.")

# Connect to the SQLite database
DATABASE = "pudl_subset.sqlite"

@st.cache_data
def load_data():
    """
    Load data from the SQLite database and return it as a DataFrame.
    """
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    
    # Query to retrieve the relevant columns
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

# Load the data
data = load_data()

# Define updated groupings for plant types
plant_type_groups = {
    "Hydro": ["run_of_river", "run_of_river_with_storage", "hydro"],
    "Solar": ["photovoltaic", "solar_thermal"],
    "Fossil Fuels": ["combustion_turbine", "internal_combustion", "fuel_cell"],
    "Nuclear": ["nuclear"],
    "Wind": ["wind"],
    "Geothermal": ["geothermal"],
    "Energy Storage": ["storage"],
    "Steam": ["steam"],  # Keep steam separate due to diverse energy sources
    "Combination": ["combined_cycle"],  # New group for combined cycle plants
}

# Function to group plant types
def group_plant_type(plant_type):
    for group, types in plant_type_groups.items():
        if plant_type in types:
            return group
    return "Other"  # For any plant types not explicitly grouped

# Add a new column for grouped plant types
data["grouped_plant_type"] = data["plant_type"].apply(group_plant_type)

# Sidebar Filters
st.sidebar.header("Filter Options")

# Filter by a single year using a dropdown
years = sorted(data["report_year"].unique())
selected_year = st.sidebar.selectbox("Select Reporting Year", years)

# Filter by grouped plant type
grouped_plant_types = data["grouped_plant_type"].unique()
selected_grouped_plant_types = st.sidebar.multiselect(
    "Select Plant Type Groups", grouped_plant_types, default=grouped_plant_types
)

# Filter the data based on user input
filtered_data = data[
    (data["report_year"] == selected_year) &
    (data["grouped_plant_type"].isin(selected_grouped_plant_types))
]

# Define a muted color palette with more distinct colors
muted_color_palette = [
    "#F08080",  # Light Coral
    "#D8BFD8",  # Thistle
    "#98FB98",  # Pale Green
    "#FFDAB9",  # Peach Puff
    "#F4A460",  # Sandy Brown
    "#DDA0DD",  # Plum
    "#FFE4B5",  # Moccasin
    "#E6E6FA",  # Lavender
    "#F0E68C",  # Khaki
    "#C0C0C0",  # Silver
    "#BDB76B",  # Dark Khaki
    "#FFB6C1",  # Light Pink
]

# Dynamically assign muted colors to grouped plant types
unique_grouped_plant_types = filtered_data["grouped_plant_type"].unique()
color_map = {group: muted_color_palette[i % len(muted_color_palette)] for i, group in enumerate(unique_grouped_plant_types)}

# Display the legend in the sidebar
st.sidebar.markdown("### Legend")
for plant_type, color in color_map.items():
    st.sidebar.markdown(
        f"<span style='background-color:{color};width:15px;height:15px;display:inline-block;margin-right:10px;border-radius:50%;'></span>{plant_type}",
        unsafe_allow_html=True,
    )

# Create a Folium map centered on the United States with a wide zoom
st.subheader("Filtered Map")
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)  # Centered on the CONUS

# Plot points on the map with custom markers
for _, row in filtered_data.iterrows():
    # Get color based on grouped plant type
    marker_color = color_map.get(row["grouped_plant_type"], "gray")
    
    # Scale marker size by net_generation_mwh (normalize for visualization purposes)
    marker_size = max(5, min(30, row["net_generation_mwh"] / 1_000_000 * 10))
    
    # Create popup content
    popup_content = f"""
    <b>Plant Name:</b> {row['plant_name_ferc1']}<br>
    <b>Utility Company:</b> {row['utility_name_ferc1']}<br>
    <b>City:</b> {row['city']}<br>
    <b>State:</b> {row['state']}<br>
    <b>Plant Type Group:</b> {row['grouped_plant_type']}<br>
    <b>Reporting Year:</b> {row['report_year']}<br>
    <b>Net Generation (MWh):</b> {row['net_generation_mwh']:,}
    """
    
    # Add a CircleMarker for each plant
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=marker_size,
        popup=folium.Popup(popup_content, max_width=300),
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.5  # Set marker transparency
    ).add_to(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)
