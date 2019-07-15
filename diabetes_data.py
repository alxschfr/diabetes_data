#!/usr/bin/env python3
'''python3 program to read the export csv-file of the diabetes-management application mySugr (https://mysugr.com/)
as pandas0.24.2.DataFrame object to enable statistical time-based analysis.'''

import csv

import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

#initialize variables (list for storing concatenated dates, subset selection filter based on relevant column indices,
# datetime_format of concatenated Datum_ID
timestamp_list = []
mysugr_df_columnfilter = [0, 4, 6, 8, 9, 12, 13]
datetime_format = '%d.%m.%Y %H:%M:%S'

#open MySugr export csv and append concatenated timestamp to separate list 'timestamp_list' to create unique timestamps
with open('data/export.csv', newline='') as f:
    mysugr_csv = csv.DictReader(f)
    for row in mysugr_csv:
        timestamp_list.append(row['Datum'] + ' ' + row['Zeit'])

#read MySugr export csv as pandas DataFrame
mysugr_df = pd.read_csv('data/export.csv')

#insert new column into DF with concatenated timestamp
mysugr_df.insert(0, 'Datum_ID', timestamp_list)

#initialise and print filtered list of column names for subset selection, filtered by index values in mysugr_df_columnfilter
header_list = mysugr_df.columns.to_numpy().tolist()
header_list = [header_list[i] for i in mysugr_df_columnfilter]
print(header_list)

#make subset selection based on list of relevant column names and reassign to DataFrame
mysugr_df = mysugr_df.loc[:, header_list]

#replace all ',' in colums 4, 5, 6 with '.' for type conversion
mysugr_df[header_list[3:7]] = mysugr_df[header_list[3:7]].replace({',': '.'}, regex=True)

#convert missing columns to pandas float64 dtype
mysugr_df['Bolus (Mahlzeit)'] = mysugr_df['Bolus (Mahlzeit)'].astype('float64')
mysugr_df['Bolus (Korrektur)'] = mysugr_df['Bolus (Korrektur)'].astype('float64')
mysugr_df['Mahlzeitkohlenhydrate (Broteinheiten, Faktor 12)'] = mysugr_df['Mahlzeitkohlenhydrate (Broteinheiten, Faktor 12)'].astype('float64')

#convert concatenated date and time to pandas datetime64 object and initialize DateTimeIndex based on 'Datum_ID' and
# print index type to check if it worked
mysugr_df['Datum_ID'] = pd.to_datetime(mysugr_df['Datum_ID'], format=datetime_format)
mysugr_df = mysugr_df.set_index(mysugr_df['Datum_ID'])
print(type(mysugr_df.info()))

#select subsection based on date, print general descriptive statistic for every column and a plot that maps blood
# glucose measurements to dates
print(mysugr_df.loc['2019-07-01':'2019-07-10'].describe().to_string())

#interpolate missing values for blood sugar test, because of entries with only BE or insulin values
mysugr_df['Blutzuckermessung (mg/dL)'] = mysugr_df['Blutzuckermessung (mg/dL)'].interpolate(method='linear', limit_direction='forward')

#plot lineplot of dataframe in selected date range
mysugr_df.loc['2019-07-01':'2019-07-10'].plot.line(x='Datum_ID', y='Blutzuckermessung (mg/dL)', linestyle='-')
plt.show()

#Filter rows with NaN-Values for specific column
#mysugr_df[mysugr_df['Blutzuckermessung (mg/dL)'].notnull()]
