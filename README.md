# Generative AI's Effect on Energy Consumption

## Index
- [About](#about)
- [Packages/Tools Used](#packagestools-used)
- [File Structure](#file-structure) 
- [Data Sources](#data-sources)
- [Gallery](#gallery)
- [Credit/Acknowledgment](#creditacknowledgment)

## About
This project investigates the energy consumption of generative AI usage and its impact on global power demands, focusing on data centers in the United States. We examined whether the growth in energy consumption from AI usage outpaces the adoption of green energy. Utilizing various datasets and visualization tools, the analysis addresses the energy demands of generative AI and potential sustainability challenges.

## Packages/Tools Used
- Datasette: For quick exploration and querying of datasets.
- Kaggle Notebooks: To retrieve and process large datasets.
- Streamlit: For creating interactive visualizations, including power plant and data center maps.
- Folium: For map-based visualizations.
- Zippopotamus API: For ZIP code-based geographic correlation.
- SERPAPI: To programmatically collect Google Trends data for generative AI interest.

## File Structure
Add a file structure here with the basic details about files, below is an example.

| No | File Name | Details 
|----|------------|-------|
| 1  | Analysis.ipynb | Noah
| 2  | Data_Center_Locations | Folder containing CSVs with locations of data centers of large tech companies
| 3  | DataImport.ipynb | This notebook is used as an example on how to import the tables from pudl_subset.sqlite and describes what is in each of these tables.
| 4  | desktop.ini | ?
| 5  | GoogleTrends_SL.py | MG
| 6  | PowerGen_SL.py | MG
| 7  | Project_SL.py | MG
| 8  | pudl_subset.sqlite | SQLite database containing the subset of data that was pulled from Kaggle.
| 9  | Total_US_Interest.csv | CSV containing normalized data on how popular the phrase 'generative AI' was across the US every week since 17 November, 2019.
| 10 | US_GeoCode.csv | CSV containing the center latitude/longitude of every state in the US.
| 11 | US_Trends_Sorted | CSV containing how popular the term 'generative AI' was across each state in the US every month since November 2022.
| 12 | ZIP_Production.ipynb | Noah


##  Data Sources
- PUDL (Public Utility Data Liberation)
- Kaggle datasets (e.g., yearly power generation by state, data center locations)
- Google Trends data on generative AI interest (via SERPAPI).

##  Gallery
Pictures of your project.

## Credit/Acknowledgment
- Deryk Clary
- Rashad Brown
- Noah Richwine
- Mary Grace Burke
