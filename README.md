# Download and Process Earthquake Data with ObsPy and Python

Code to use ObsPy in order to search for earthquake events and subsequently download them, process them and plot them on the map.

For further information please follow me in the below links  
LinkedIn: https://www.linkedin.com/in/dimitris-dais/  
Email: d.dais@pl.hanze.nl  
ResearchGate: https://www.researchgate.net/profile/Dimitris_Dais2  
Research Group Page: https://www.linkedin.com/company/earthquake-resistant-structures-promising-groningen  

A YouTube video-tutorial can be found in the following link: https://youtu.be/E9k-A8daess  

# get_events.py  
Code to get earthquake events from 2010-01-01 until 2020-04-25 from the Netherlands  
It will store the info of the events in an excel file  
It will plot the events on the map

To run the code please update the following folder paths according to your system:  
**os.environ['PROJ_LIB']**  
**folder_output**  

<img src="https://github.com/dimitrisdais/obspy_tutorial/blob/master/images/get_events_1.png" width="500">

```diff
# Store the info of the events in an excel file with get_events.py
```

<img src="https://github.com/dimitrisdais/obspy_tutorial/blob/master/images/get_events_2.png" width="500" height="500">

```diff
# Plot the events on the map with get_events.py
```

# download_events.py  

Read the excel file 'events.xlsx' and download records  
Define the requested event as the number of the row in the excel file 'events.xlsx'  

To run the code please update the following folder paths according to your system:  
**folder_excel**  
**folder_main**  

<img src="https://github.com/dimitrisdais/obspy_tutorial/blob/master/images/download_events_1.png" width="500">

```diff
# The mseed and xml files as downloaded from the download_events.py
```

# process_data.py

Read the excel file 'events.xlsx'  
Define the requested event as the number of the row in the excel file 'events.xlsx'  
Define the name of the requested station to be processed  
For each channel of the requsted station remove the instrumental response and filter the data  
Plot the processed data  

To run the code please update the following folder paths according to your system:  
**folder_excel**  
**folder_main**  

<img src="https://github.com/dimitrisdais/obspy_tutorial/blob/master/images/process_data_1.png" width="500">

```diff
# The plot prepared for the removal of the instrumental response from the process_data.py
```

<img src="https://github.com/dimitrisdais/obspy_tutorial/blob/master/images/process_data_2.png" width="500" height="500">

```diff
# The plot prepared with the raw and the filtered data from the process_data.py
```

