# Generative AI's Effect on Energy Consumption

## Index
- [About](#about)
- [Packages/Tools Used](#packagestools-used)
- [File Structure](#file-structure) 
- [Data Sources](#data-sources)
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
Below is a table describing what each of the files in this repository is.

| No | File Name | Details 
|----|------------|-------|
| 1  | Analysis.ipynb | This notebook was used to process/group the data and produce graphics
| 2  | Data_Center_Locations | Folder containing CSVs with locations of data centers of large tech companies
| 3  | DataImport.ipynb | This notebook is used as an example on how to import the tables from pudl_subset.sqlite and describes what is in each of these tables.
| 4  | GoogleTrends_SL.py | This script generates an interactive heat map of 'generative AI' interest in the United States based on GoogleTrends data.
| 5  | PowerGen_SL.py | This script generates an interactive map displaying power plants and data centers in the United States.
| 6  | Products_Outputs | Folder containing graphs, photos, and products output from this project.
| 7  | pudl_subset.sqlite | SQLite database containing the subset of data that was pulled from Kaggle.
| 8  | Total_US_Interest.csv | CSV containing normalized data on how popular the phrase 'generative AI' was across the US every week since 17 November, 2019.
| 9  | US_GeoCode.csv | CSV containing the center latitude/longitude of every state in the US.
| 10 | US_Trends_Sorted | CSV containing how popular the term 'generative AI' was across each state in the US every month since November 2022.
| 11 | ZIP_Production.ipynb | This notebook was used with the zippopotomus API to analyze based on datacenter zip codes

## Streamlit Tutorial
Below are the commands needed to run each of our Streamlit apps (must have Streamlit installed on your machine):
- GoogleTrends_SL.py: python -m streamlit run GoogleTrends_SL.py
- Project_SL.py: python -m streamlit run Project_SL.py

Once you run one of these commands, the Streamlit app will launch in your default web browser.

##  Data Sources
- [PUDL (Public Utility Data Liberation) from Kaggle](https://www.kaggle.com/datasets/catalystcooperative/pudl-project)
  - Acquired through a Kaggle Notebook that can be accessed at [this link](https://www.kaggle.com/code/deryk96/pudl-data-curation).
  - The notebook shows how to query the PUDL dataset and pull the subset of data we used for this project.
  - DataImport.ipynb shows how to import pudl_subset.sqlite into Pandas.
- [Data Center Locations of Top Tech Companies from Kaggle](https://www.kaggle.com/datasets/mauryansshivam/list-of-data-centers-of-top-tech-companies)
- [Google Trends data from SERPAPI](https://serpapi.com/google-trends-api)

## Credit/Acknowledgment
- Deryk Clary
- Rashad Brown
- Noah Richwine
- Mary Grace Burke
