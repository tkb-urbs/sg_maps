"""
Created on Fri Aug 29 22:13:45 2025

@author: tkbean
"""

import pandas as pd
import requests

# Define a function to retrieve coordinates based on address from OneMap API
def getcoordinates(address):
    req = requests.get('https://www.onemap.gov.sg/api/common/elastic/search?searchVal='+address+'&returnGeom=Y&getAddrDetails=Y&pageNum=1')
    resultsdict = eval(req.text)
    if len(resultsdict['results'])>0:
        return resultsdict['results'][0]['LATITUDE'], resultsdict['results'][0]['LONGITUDE']
    else:
        pass
    
# Create column of addresses from arts sector data
df = pd.read_csv(r"C:\Users\tkbean\Documents\6 Others\Exploratory Data\1 Singapore Arts Scene\arts_firms.csv")
df['address'] = df['block']+ ' '+ df['street_name']

# create list of addresses and empty list to receive corresponding coordinates
addresslist = list(df['address'])
coordinateslist = []
    
# counts are for tracking purposes
count = 0
failed_count = 0
    
# create loop to etrieve coordinates
for address in addresslist:
    try:
        if len(getcoordinates(address))>0:
            count = count + 1
            print('Extracting',count,'out of',len(addresslist),'addresses')
            coordinateslist.append(getcoordinates(address))
    except:
        count = count + 1
        failed_count = failed_count + 1
        print('Failed to extract',count,'out of',len(addresslist),'addresses')
        coordinateslist.append(None)
print('Total Number of Addresses With No Coordinates',failed_count)

# Append coordinates to original data and export as csv
df.reset_index(drop=True, inplace=True)

df_coordinates = pd.DataFrame(coordinateslist)
df_combined = df.join(df_coordinates)
df_combined  = df_combined .rename(columns={0:'Latitude', 1:'Longitude'})

df_combined.to_csv("arts_sector_coordinates.csv", encoding='utf-8', index=False)
