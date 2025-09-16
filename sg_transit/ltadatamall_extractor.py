# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 10:21:54 2025

@author: tkbean
"""

# This code is adapted from one found on GitHub: https://github.com/blossomt/lta-datamall/blob/main/get_bus_tables.py

import os                  #library allowing interactions with operating system
from requests import get   #library for get data from APIs
from csv import DictWriter #library for handling csv files

key = 'insert your own key from LTA here'
headers = {'AccountKey': key,
          'accept':'application/json'}

# Function to get all data from API. It overcomes limit to 500 rows per call
def get_all_data_param(base_uri, parameters, output_file):
    end = False # This variable indicates when the loop should end
    n = 0 # n tells the function how many rows to skip when calling the next 500
    result_arr = []
    
    while end == False:
        uri = base_uri + "?$skip=" + str(n)
        response = get(uri, headers=headers, params=parameters) #function from library
        
        # 200 means we have reached the site. Other numbers signify errors
        if response.status_code == 200: 
            jsonObj = response.json()
            nrow = len(jsonObj['value'])
            result_arr.extend(jsonObj['value'])
            if nrow < 500:
                end = True
            n += nrow
        else:
            print("Failed to request with error" + str(response.status_code))
            end = True
        
    # Write List
    with open(output_file, 'w', encoding='utf-8') as f:
        title = [*result_arr[0].keys()]
        cw = DictWriter(f, title, delimiter=",")
        cw.writeheader()
        cw.writerows(result_arr)
    print("Total rows: " + str(n))

# uris of desired datasets
bus_stop_vol_uri = "https://datamall2.mytransport.sg/ltaodataservice/PV/Bus"
bus_origin_destination_uri = "https://datamall2.mytransport.sg/ltaodataservice/PV/ODBus"
train_stn_vol_uri = "https://datamall2.mytransport.sg/ltaodataservice/PV/Train"
train_origin_destination_uri = "https://datamall2.mytransport.sg/ltaodataservice/PV/ODTrain"

# set the desired date to April 2022. Follow the format below.
# it is formatted as a Python dictionary due to the arguments the 'get' function takes
dates = [{'Date':'202506'}, {'Date':'202507'}, {'Date':'202508'} ]
directory = r"insert your own directory here"

for date_parameter in dates:
    
    get_all_data_param(bus_stop_vol_uri, date_parameter, directory + 'bus_stop_vol_' + str(date_parameter["Date"]) + '.csv')
    get_all_data_param(bus_origin_destination_uri, date_parameter , directory + 'bus_origin_destination_' + str(date_parameter["Date"]) + '.csv')
    get_all_data_param(train_origin_destination_uri, date_parameter , directory + 'train_origin_destination_' + str(date_parameter["Date"]) + '.csv')
    get_all_data_param(train_stn_vol_uri, date_parameter, directory + 'train_stn_vol_' + str(date_parameter["Date"]) + '.csv')
