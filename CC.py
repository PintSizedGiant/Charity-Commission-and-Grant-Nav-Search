import streamlit as st
import plotly.express as px 
import pandas as pd 
import os
import warnings
import folium
from streamlit_folium import folium_static
import requests
import zipfile
import io
import json

st.set_page_config(page_title="Charity Commission + Grant nav Data", page_icon="bar_chart", layout='wide')

st.write('We want; Charity Commission and Grant nav merge. Key facts, highly filterable. Cloropleth map is the way')

# Charity Commission data import ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
url = 'https://ccewuksprdoneregsadata1.blob.core.windows.net/data/json/publicextract.charity.zip'
# make  request to get zip file
res = requests.get(url)

# Unzip the content
with zipfile.ZipFile(io.BytesIO(res.content), 'r') as zip_ref:
    # Assuming there's only one JSON file in the ZIP, you can extract it
    file_name = zip_ref.namelist()[0]
    json_content = zip_ref.read(file_name)

# Load JSON content into a Pandas DataFrame named df
json_data = json.loads(json_content)
df = pd.json_normalize(json_data)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# grant nav data ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
fp1 = r"C:\Users\OliverHughes\Downloads\Grant_nav_+50k_grantorgs_and_gov.csv"
gdf = pd.read_csv(fp1)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------













# SIDEBAR Filters ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Sidebar for filters
st.sidebar.title("Filters")

# Filters for charity_registration_status and linked_charity_number
charity_registration_status_options = ['All'] + df['charity_registration_status'].unique().tolist()
charity_registration_status_filter = st.sidebar.selectbox('Select Charity Registration Status', charity_registration_status_options)

linked_charity_numbers_options = ['All'] + df['linked_charity_number'].unique().tolist()
linked_charity_numbers_filter = st.sidebar.multiselect('Select Linked Charity Numbers', linked_charity_numbers_options)

# Apply filters
if charity_registration_status_filter == 'All' and not linked_charity_numbers_filter:
    filtered_df = df  # Show entire dataset if no filters are applied
else:
    filtered_df = df[
        (df['charity_registration_status'] == charity_registration_status_filter) |
        (df['linked_charity_number'].isin(linked_charity_numbers_filter))
    ]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# Download filtered data
with st.expander("Download Data"):
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", data=csv, file_name="Filtered_Data.csv", mime="text/csv",
                       help='Click here to download the filtered data as a CSV file')




































# Rename charity number column and convert to string
#gdf['linked_charity_number'] = gdf['Recipient Org:Charity Number'].astype(str)
#df['linked_charity_number'] = df['linked_charity_number'].astype(str)

# Merge DataFrames
#mdf = pd.merge(df, gdf, on='linked_charity_number', how='left')

# Display the merged DataFrame
#st.write(mdf)








# Display filtered data ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# display charity data
st.write(filtered_df)
# display grantnav
selected_columns = st.multiselect("Select Columns to Display", gdf.columns)
st.write(gdf[selected_columns])
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------






st.write(df.columns.tolist())