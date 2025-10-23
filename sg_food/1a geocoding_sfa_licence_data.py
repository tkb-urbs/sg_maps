"""
Created on Thu Oct 16 17:49:27 2025

@author: tkbean
"""

import pandas as pd
import requests
import re

# Download data from SFA website. For example, I downloaded files based on whether they contained a certain digit in the postal code
sfa_raw_csv = [r"LicensedFoodEstablishmentsSearch (1).csv", 
               r"LicensedFoodEstablishmentsSearch (2).csv", 
               r"LicensedFoodEstablishmentsSearch (3).csv", 
               r"LicensedFoodEstablishmentsSearch (4).csv",
               r"LicensedFoodEstablishmentsSearch (5).csv",
               r"LicensedFoodEstablishmentsSearch (6).csv",
               r"LicensedFoodEstablishmentsSearch (7).csv",
               r"LicensedFoodEstablishmentsSearch (8).csv",
               r"LicensedFoodEstablishmentsSearch.csv"]

sfa_raw_combined = pd.concat([pd.read_csv(file) for file in sfa_raw_csv], ignore_index=True)

# drop duplicate data
sfa_data_cleaned = sfa_raw_combined.drop_duplicates(subset = ["Licence Number"])

sfa_data_cleaned.to_csv(r"sfa_2025_combined.csv")

# I prefer to cut these steps so I have large data frames backed up
food_licenses = pd.read_csv(r"sfa_2025_combined.csv")

# OneMap API key for geocoding
key = 'insert_SLA_OneMap_key'
headers = {'Authorization': key}

# function to get coordinates from OneMap by Shawn Tham
def getcoordinates(address):
    req = requests.get('https://www.onemap.gov.sg/api/common/elastic/search?searchVal='+address+'&returnGeom=Y&getAddrDetails=Y&pageNum=1', headers = headers)
    resultsdict = eval(req.text)
    if len(resultsdict['results'])>0:
        return resultsdict['results'][0]['LATITUDE'], resultsdict['results'][0]['LONGITUDE']
    else:
        pass

# create list of addresses
addresslist_uncleaned = list(food_licenses['Establishment Address'])
addresslist = []

for addr in addresslist_uncleaned:

  # to deal with floats and NaN which the later code cannot deal with
  if type(addr) != str:
        addresslist.append(addr)
  # most addresses have a unit number and we can extract the block and street number before that     
  elif '#' in addr:
        addr_cleaned = (re.findall('.+#', addr)[0])[:-2]
        addresslist.append(addr_cleaned)
  # No unit number to help locate street? This uses the postal code
  elif 'Singapore' in addr:
        addr_cleaned = (re.findall('.+Singapore', addr)[0])[:-10]
        addresslist.append(addr_cleaned)
  # To deal with any remaining exceptions  
  else:
        addresslist.append(addr)

# create variables to hold coordinate data
coordinateslist = []
count = 0
failed_count = 0

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
food_licenses.reset_index(drop=True, inplace=True)

df_coordinates = pd.DataFrame(coordinateslist)
df_combined = food_licenses.join(df_coordinates)
df_combined  = df_combined.rename(columns={0:'Latitude', 1:'Longitude'})

df_combined.to_csv(r"sfa_2025_geocoded.csv", encoding='utf-8', index=False)

