# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 16:22:17 2025

@author: tkbean
"""

# import all libraries needed to do analysis
import pandas as pd

# import SFA licensed food establishment dataset
sfa_food = pd.read_csv(r"sfa_2025_geocoded.csv")

# Investigate how many types sfa_food categorises food establishments into
print(sfa_food['Type of Food Business'].unique())
print(len(sfa_food['Type of Food Business'].unique()))

est_types = pd.DataFrame(sfa_food['Type of Food Business'].unique())

# Investigate how many food establishments fall under each type
cate_freq = sfa_food.groupby(['Type of Food Business'])['Licence Number'].count()


# Import acra data 2025
acra_2025 = pd.read_csv(r"Sep_2025_all_sg_live_companies.csv")

# Merge ACRA information with SFA data
food_est = pd.merge(sfa_food, acra_2025, how = 'left', left_on = 'Licensee Name', right_on = 'entity_name')

# Import SSIC Descriptions
ssic_desc = pd.read_csv(r"ssic2025-classification-structure.csv")
ssic_desc = ssic_desc.dropna()
        
food_est['primary_ssic_code'] = food_est['primary_ssic_code'].astype(str)
ssic_desc['SSIC 2025 Title'] = ssic_desc['SSIC 2025 Title'].astype(str)

def ssic_cleaner(c):
    if len(c) > 5:
        new_c = c[0:5]
    else:
        new_c = 'NA'
    return new_c
        
food_est['primary_ssic_code'] = food_est['primary_ssic_code'].apply(ssic_cleaner)
        
food_est_2 = pd.merge(food_est, ssic_desc, how = 'left', left_on = 'primary_ssic_code', right_on = 'SSIC 2025')

food_est_2['secondary_ssic_code'] = food_est_2['secondary_ssic_code'].astype(str)

food_est_3 = pd.merge(food_est_2, ssic_desc, how = 'left', left_on = 'secondary_ssic_code', right_on = 'SSIC 2025')

# Keep only necessary columns, rename some 
food_cleaned = food_est_3.drop(['Unnamed: 0_x', 'SNO', 'Unnamed: 0_y', 'entity_name', 'block', 'street_name', 'SSIC 2025_x', 'SSIC 2025_y'], axis = 1)

food_cleaned = food_cleaned.rename(columns = {'SSIC 2025 Title_x':'primary_ssic_description', 'SSIC 2025 Title_y':'secondary_ssic_description'})
food_cleaned = food_cleaned[['Establishment Address', 
                             'Licence Number', 
                             'Licensee Name',
                             'Business Name', 
                             'Type of Food Business', 
                             'Latitude', 
                             'Longitude',
                             'entity_type_description', 
                             'business_constitution_description',
                             'entity_status_description',
                             'registration_incorporation_date',
                             'primary_ssic_code', 
                             'primary_ssic_description',
                             'secondary_ssic_code', 
                             'secondary_ssic_description']]

food_cleaned.to_csv(r'sfa_acra_food_data.csv')
