"""

Read the excel file 'events.xlsx' and download records
Define the requested event as the number of the row in the excel file 'events.xlsx'

To run the code please update the following folder paths according to your system:
folder_excel
folder_main

"""

#%%
#
#

import datetime
import os
import pandas as pd
import obspy.clients.fdsn
import obspy
from obspy.clients.fdsn.mass_downloader import RectangularDomain, \
    Restrictions, MassDownloader

# the folder path for the excel with the info about events
folder_excel = 'C:/Users/jimar/Dimitris/python/github_codes/obspy_tutorial/events/'
# the data will be stored in a subfolder in the folder
folder_main = 'C:/Users/jimar/Dimitris/python/github_codes/obspy_tutorial/'

# read the excel with the info about events
excel_filename = 'events.xlsx' 
excel_tab = 'info'
excel_file = folder_excel + excel_filename

df = pd.read_excel(excel_file, sheet_name = excel_tab)

#%%
# define the requested data
#

# requested event
ii= 7
   
# define map extent
statLat_min = 52.9
statLat_max = 53.7
statLon_min = 6.4
statLon_max = 7.3

# seconds to request before and after the given date and time
seconds_before = 15
seconds_after = 30

# request data only from the KNMI network
network = 'NL'
providers = "http://rdsa.knmi.nl"

# requested channels
channel_priorities =  ["HG[ZNE12]"]

#%%
# download data
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
                            
# convert time to obspy.core.utcdatetime.UTCDateTime                
origin_time = obspy.UTCDateTime(eq_time)       
             
# prepare data downloader 
domain = RectangularDomain(minlongitude=statLon_min, maxlongitude=statLon_max,\
                           minlatitude=statLat_min, maxlatitude=statLat_max)

restrictions = Restrictions(
    # Get data from 5 minutes before the event to one hour after the
    # event. This defines the temporal bounds of the waveform data.
    starttime=origin_time - seconds_before,
    endtime=origin_time + seconds_after,
#    station = 'BGAR',
    network = network,
    # You might not want to deal with gaps in the data. If this setting is
    # True, any trace with a gap/overlap will be discarded.
    reject_channels_with_gaps=True,
    # And you might only want waveforms that have data for at least 95 % of
    # the requested time span. Any trace that is shorter than 95 % of the
    # desired total duration will be discarded.
    minimum_length=0.95,
    # No two stations should be closer than 10 km to each other. This is
    # useful to for example filter out stations that are part of different
    # networks but at the same physical station. Settings this option to
    # zero or None will disable that filtering.
    minimum_interstation_distance_in_m=0,
    # Only HH or BH channels. If a station has HH channels, those will be
    # downloaded, otherwise the BH. Nothing will be downloaded if it has
    # neither. You can add more/less patterns if you like.
    channel_priorities=channel_priorities,
#    channel_priorities=["HG[NE]", "HG[NE]"],
    # Location codes are arbitrary and there is no rule as to which
    # location is best. Same logic as for the previous setting.
    location_priorities=["", "00", "10"])

# No specified providers will result in all known ones being queried.
# mdl = MassDownloader()
mdl = MassDownloader(providers=[providers])
# The data will be downloaded to the ``./waveforms/`` and ``./stations/`` # folders with automatically chosen file names.
mdl.download(domain, restrictions, mseed_storage = folder_output,
             stationxml_storage = folder_output)

