"""
Created on Fri Aug 29 21:39:48 2025

@author: tkbean
"""

import pandas as pd

# Create a list of all ssic codes for arts related sectors
all_sectors = pd.read_csv("ssic2020-classification-structure.csv")

arts_sectors_raw = ['Training courses for music, dancing, art, speech and drama',
                'Production of live stage presentations', 
                'Performing arts venue operation',
                'Orchestras, musical bands, choirs and dance groups',
                'Dramatic arts, music and other arts production-related activities n.e.c. (eg stage, lighting and sound services)']
 
arts_sectors = []

for sector in arts_sectors_raw:
    sector_caps = sector.upper()
    arts_sectors.append(sector_caps)

# Create a list of all acra files
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

arts_firms = pd.DataFrame(columns = desired_columns)

for file in acra_files:
    temp_df = pd.read_csv(file, usecols = desired_columns)
    temp_df2 = temp_df.loc[temp_df['primary_ssic_description'].isin(arts_sectors)]
    arts_firms = pd.concat([arts_firms,temp_df2])
    
arts_firms.to_csv('arts_firms.csv')
