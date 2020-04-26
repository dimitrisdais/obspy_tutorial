"""

Code to get earthquake events from 2010-01-01 until 2020-04-25 from the Netherlands
It will store the info of the events in an excel file
It will plot the events on the map

To run the code please update the following folder paths according to your system:
os.environ['PROJ_LIB']
folder_output

Author: Dimitris Dais
LinkedIn: https://www.linkedin.com/in/dimitris-dais/  
Email: d.dais@pl.hanze.nl  

"""

#%%
#
#

import os
import obspy.clients.fdsn
import numpy as np
import pandas as pd
import obspy
import obspy.clients.fdsn
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

os.environ['PROJ_LIB'] = r'C:/Users/jimar/Anaconda3/pkgs/proj4-4.9.3-hfa6e2cd_9/Library/share'
from mpl_toolkits.basemap import Basemap

# the plots and the excel with the data will be stored here
folder_output = 'C:/Users/jimar/Dimitris/python/github_codes/obspy_tutorial/events/'
# create the folder_output
if not os.path.exists(folder_output):
    os.makedirs(folder_output)

# the info of the events will be stored in this excel
excel_filename = 'events.xlsx' 
excel_tab = 'info'

# dates to request data for
starttime = obspy.UTCDateTime("2010-01-01")
endtime = obspy.UTCDateTime("2020-04-25")

client = "KNMI"

# define map extent
minlatitude = 52.9
maxlatitude = 53.7
minlongitude = 6.4
maxlongitude = 7.3

# min and max requested magnitudes
minmagnitude = 2
maxmagnitude = 5

#%%
#
#

client = obspy.clients.fdsn.Client(client)

events = client.get_events(minlatitude=minlatitude, maxlatitude=maxlatitude,
                           minlongitude=minlongitude, maxlongitude=maxlongitude,
                           starttime=starttime,
                           endtime=endtime,
                           minmagnitude=minmagnitude,maxmagnitude=maxmagnitude)

print("found %s event(s):" % len(events))
print(events)

# use this command to print all the events
#print(events.__str__(print_all=True))

#%%
# store data to dataframe
#

feature_list = ['Origin Time (UTC)', 'Lat [°]', 'Lon [°]', 'depth [m]', 'event_type', 'mag', 'magnitude_type', 'creation_info', 'info']
df = pd.DataFrame(0, index=np.arange(len(events)), columns=feature_list)

for ii in range (0, len(events)):
        
    df['Origin Time (UTC)'].loc[ii] = events[ii].origins[0].time
    df['Lat [°]'].loc[ii] = events[ii].origins[0].latitude
    df['Lon [°]'].loc[ii] = events[ii].origins[0].longitude
    df['depth [m]'].loc[ii] = events[ii].origins[0].depth    
    df['event_type'].loc[ii] = events[ii].event_type   
    df['mag'].loc[ii] = events[ii].magnitudes[0].mag     
    df['magnitude_type'].loc[ii] = events[ii].magnitudes[0].magnitude_type    
    df['creation_info'].loc[ii] = events[ii].origins[0].creation_info 
    df['info'].loc[ii] = events[ii].event_descriptions[0].text 
    

#%%
# save to excel
#
    
excel_output = folder_output + excel_filename
df.to_excel(excel_output, sheet_name=excel_tab)


#%%
# plot events over the map
#

# prepare parameters for plots       
plt.rcParams.update({'font.size': 14})
plt.rcParams['axes.labelweight'] = 'bold'

# starttime
t1 = starttime.strftime('%Y-%m-%d')
# endtime
t2 = endtime.strftime('%Y-%m-%d')

# longitude
x = df['Lon [°]'].values
# latitude
y = df['Lat [°]'].values
# magnitude
z = df['mag'].values

# title of the plot
plt_title = 'Earthquakes {} - {}'.format(t1, t2)
# the plot will be saved at this file path
plt_fig = folder_output + plt_title + '.png'  

figsize = (10, 10)
fig = plt.figure(figsize=figsize)

ax = fig.add_subplot(111, facecolor='w', frame_on=False)

norm = Normalize()

x_ticks = np.arange(minlongitude,maxlongitude + maxlongitude/10000, float("{0:.3f}".format(maxlongitude-minlongitude))/5)
y_ticks = np.arange(minlatitude,maxlatitude + maxlatitude/10000, float("{0:.3f}".format(maxlatitude-minlatitude))/5)

# Set up Basemap instance
map = Basemap(llcrnrlon = minlongitude, llcrnrlat = minlatitude, urcrnrlon = maxlongitude, urcrnrlat = maxlatitude,
            projection = 'merc',resolution='h')


# transform lon / lat coordinates to map projection
x_lon, y_lat = map(*(x, y))

# draw map details
map.drawcoastlines()
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='grey', lake_color='aqua')
map.drawcountries(
    linewidth=.75, linestyle='solid', color='#000073',
    antialiased=True,
    ax=ax, zorder=3)
map.drawparallels(y_ticks,
                color = 'black', linewidth = 0.5,
                labels=[True, False, False, False])
map.drawmeridians(x_ticks,
                color = '0.25', linewidth = 0.5,
                labels=[False, False, False, True])

# plot events
scatter = map.scatter(x_lon, y_lat,
          c=z, alpha=1, s=200 * norm(z),
          cmap='jet', ax=ax,
          vmin=z.min(), vmax=z.max(), zorder=4)

cbar = map.colorbar(scatter)
cbar.set_label('Magnitude', size=14)

plt.title(plt_title, fontweight="bold")
plt.xlabel('Longitude', labelpad=40)
plt.ylabel('Latitude', labelpad=80)

plt.tight_layout()
plt.savefig(plt_fig, bbox_inches='tight', dpi=500)
