"""

Read the excel file 'events.xlsx'
Define the requested event as the number of the row in the excel file 'events.xlsx'
Define the name of the requested station to be processed
For each channel of the requsted station remove the instrumental response and filter the data
Plot the processed data

To run the code please update the following folder paths according to your system:
folder_excel
folder_main

Author: Dimitris Dais
LinkedIn: https://www.linkedin.com/in/dimitris-dais/  
Email: d.dais@pl.hanze.nl  

"""

#%%
#
#

import datetime
import os
import pandas as pd
import obspy.clients.fdsn
import obspy
from obspy import read, read_inventory
import matplotlib.pyplot as plt
import numpy as np 

# the folder path for the excel with the info about events
folder_excel = 'C:/Users/jimar/Dimitris/python/github_codes/obspy_tutorial/events/'
# the data will be stored in a subfolder in the folder
folder_main = 'C:/Users/jimar/Dimitris/python/github_codes/obspy_tutorial/'

# read the excel with the info about events
excel_filename = 'events.xlsx' 
excel_tab = 'info'
excel_file = folder_excel + excel_filename

df = pd.read_excel(excel_file, sheet_name = excel_tab)

# requested event
ii= 7

# requested station
station = 'BGAR'

#%%
#
#

# convert time from string to datetime
time_format = '%Y-%m-%dT%H:%M:%S.%f%z'
eq_time = datetime.datetime.strptime(df['Origin Time (UTC)'][ii], time_format)

# use the date of the event as folder name where the downloaded data will be stored
event_date = '{:04d}-{:02d}-{:02d}'.format(eq_time.year, eq_time.month, eq_time.day)
folder_output = folder_main + event_date + '/'

# create the folder_output
if not os.path.exists(folder_output):
    os.makedirs(folder_output)

folder_plots = folder_main + event_date + '/plots/'
# create the folder_output
if not os.path.exists(folder_plots):
    os.makedirs(folder_plots)
                        
# convert time to obspy.core.utcdatetime.UTCDateTime                
origin_time = obspy.UTCDateTime(eq_time) 

# retrieve the downloaded mseed files in the folder_output
mseed_files = [f for f in os.listdir(folder_output) if f.endswith('.mseed')]
# retrieve the downloaded xml files in the folder_output
xml_files = [f for f in os.listdir(folder_output) if f.endswith('.xml')]

# retrieve the mseed files from the requested station
records = []
for mseed_file in mseed_files:
    if station in mseed_file:
        records.append(mseed_file)

# retrieve the xml file from the requested station       
for xml_file in xml_files:
    if station in xml_file:
        inv_file = xml_file

# for each channel of the requsted station remove the instrumental response and filter the data    
for record in records:
    st = read(folder_output + record)
    tr = st[0]
    inv = read_inventory(folder_output + inv_file)

    filename = '{}_{}_{}.png'.format(tr.stats.network, tr.stats.station, tr.stats.channel)
    plt_fig = folder_plots + filename
    
    pre_filt = [0.001, 0.005, 10, 20]
    tr.remove_response(inventory=inv, pre_filt=pre_filt, output="ACC",
                       water_level=60, plot=plt_fig)
    plt.close("all")
    
    # Filtering with a lowpass on a copy of the original Trace
    tr_filt = tr.copy()
    tr_filt.filter('lowpass', freq=1.0, corners=2, zerophase=True)
    
    # Now let's plot the raw and filtered data...
    t = np.arange(0, tr.stats.npts / tr.stats.sampling_rate, tr.stats.delta)
    fig = plt.figure()
    plt.subplot(211)
    plt.plot(t, tr.data, 'k')
    plt.ylabel('Raw Data')
    plt.grid(True)
    plt.subplot(212)
    plt.plot(t, tr_filt.data, 'k')
    plt.ylabel('Lowpassed Data')
    plt.xlabel('Time [s]')
    plt.suptitle(tr.stats.starttime)
    plt.grid(True)
    
    filename = '{}_{}_{}_filtered.png'.format(tr.stats.network, tr.stats.station, tr.stats.channel)
    plt_fig = folder_plots + filename
    
    plt.savefig(plt_fig, dpi=500)
    plt.close('all')
                
