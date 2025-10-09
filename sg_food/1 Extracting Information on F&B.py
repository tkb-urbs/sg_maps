# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 14:07:11 2025

@author: tkbean
"""

# import all libraries needed to do analysis
import pandas as pd
import geopandas as gpd # needed to handle geojson files
from bs4 import BeautifulSoup

# parse out data from a row in the description column
def parse_html_table(html):
   soup = BeautifulSoup(html, "html.parser")
   data = {}
   for row in soup.find_all("tr"):
       cells = row.find_all(["th", "td"])
       if len(cells) == 2:  # Skip header rows with colspan
           key = cells[0].get_text(strip=True)
           val = cells[1].get_text(strip=True)
           data[key] = val
   return data

def data_editor(df):
    parsed_data = df["Description"].apply(parse_html_table)
    parsed_df = pd.json_normalize(parsed_data)
    result_df = pd.concat([df.drop(columns=["Description"]), parsed_df], axis=1)
    
    return result_df

# import SFA licensed food establishment dataset
food_est = gpd.read_file("EatingEstablishments.geojson")
food_est = data_editor(food_est)

# Import ACRA data on F&B firms
acra_files = ['ACRAInformationonCorporateEntitiesA.csv',
             'ACRAInformationonCorporateEntitiesB.csv',
             'ACRAInformationonCorporateEntitiesC.csv',
             'ACRAInformationonCorporateEntitiesD.csv',
             'ACRAInformationonCorporateEntitiesE.csv',
             'ACRAInformationonCorporateEntitiesF.csv',
             'ACRAInformationonCorporateEntitiesG.csv',
             'ACRAInformationonCorporateEntitiesH.csv',
             'ACRAInformationonCorporateEntitiesI.csv',
             'ACRAInformationonCorporateEntitiesJ.csv',
             'ACRAInformationonCorporateEntitiesK.csv',
             'ACRAInformationonCorporateEntitiesL.csv',
             'ACRAInformationonCorporateEntitiesM.csv',
             'ACRAInformationonCorporateEntitiesN.csv',
             'ACRAInformationonCorporateEntitiesO.csv',
             'ACRAInformationonCorporateEntitiesP.csv',
             'ACRAInformationonCorporateEntitiesQ.csv',
             'ACRAInformationonCorporateEntitiesR.csv',
             'ACRAInformationonCorporateEntitiesS.csv',
             'ACRAInformationonCorporateEntitiesT.csv',
             'ACRAInformationonCorporateEntitiesU.csv',
             'ACRAInformationonCorporateEntitiesV.csv',
             'ACRAInformationonCorporateEntitiesW.csv',
             'ACRAInformationonCorporateEntitiesX.csv',
             'ACRAInformationonCorporateEntitiesY.csv',
             'ACRAInformationonCorporateEntitiesZ.csv',
             'ACRAInformationonCorporateEntitiesOthers.csv']

desired_columns =['entity_name',
                 'entity_type_description',
                 'business_constitution_description',
                 'entity_status_description',
                 'registration_incorporation_date',
                 'block',
                 'street_name',
                 'primary_ssic_code',
                 'primary_ssic_description',
                 'primary_user_described_activity',
                 'secondary_ssic_code',
                 'secondary_ssic_description',
                 'secondary_user_described_activity']

# merge ssic codes with food license data

license_holders = list(food_est['LIC_NAME'].unique())

lic_info = pd.DataFrame(columns = desired_columns)

for file in acra_files:
    temp_df = pd.read_csv(file, usecols = desired_columns)
    temp_df2 = temp_df.loc[temp_df['entity_name'].isin(license_holders)]
    lic_info = pd.concat([lic_info,temp_df2])

sfa_food = pd.merge(food_est, lic_info, how = 'left', left_on = 'LIC_NAME', right_on = 'entity_name')

sfa_food.to_csv('sfa_with_acra_data.csv')

# Pull out data on all food retail companies from ACRA
food_sectors_raw = ['Supermarkets and hypermarkets', 
                    'Mini-marts, convenience stores and provision shops', 
                    'Retail sale of fruits and vegetables',
                    'Retail sale of meat, poultry, eggs and seafood', 
                    'Retail sale of confectionery and bakery products (not manufactured on site)', 
                    'Retail sale of health supplements', 
                    'Retail sale of food n.e.c.', 
                    'Retail Sale of Beverages in Specialised Stores',
                    'Stalls (including pushcarts) selling uncooked food', 
                    'Restaurants', 
                    'Cafes', 
                    'Fast food outlets',  
                    'Food courts, coffee shops and canteens (with mainly food and beverage income)', 
                    'Food kiosks mainly for takeaway and delivery', 
                    'Pubs', 
                    'Stalls selling cooked food and prepared drinks (including stalls at food courts and mobile food hawkers)', 
                    'Food caterers']

food_sectors = []

for sector in food_sectors_raw:
    sector_caps = sector.upper()
    food_sectors.append(sector_caps)

acra_food = pd.DataFrame(columns = desired_columns)

for file in acra_files:
    temp_df = pd.read_csv(file, usecols = desired_columns)
    temp_df2 = temp_df.loc[temp_df['primary_ssic_description'].isin(food_sectors)]
    acra_food = pd.concat([acra_food,temp_df2])
    
acra_food.to_csv('acra_food_firms.csv')
