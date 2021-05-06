# Import packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
print(os.getcwd())

# Code for importing data through API
# """ import requests
# url= 'API link of interest'
# r= requests.get(url)
# json_data= r.jason() # to decode the json file into a dictionary
# for key,value in json_data.items():
#         print(Key + ':', value)
# json_data to DataFrame
# df = pd.DataFrame(json_data, columns=[])
# Now we can explore our DataFrame"""


# importing data csv ito Pandas DataFrame
Covid = pd.read_csv('data.csv')

# set option for getting all the rows and columns when printing
pd.set_option('display.max_rows', None, 'display.max_columns', None)

# Analyzing data
# printing data head and tail
print(Covid.head(10))
print(Covid.tail(10))

# printing the list of the columns name
print(Covid.columns)

# checking the shape of the data set
print(Covid.shape)

# observing data
print(Covid.describe())
print(Covid.describe(include='object'))
print(Covid.info())

# To get the unique values

print(Covid.YearWeekISO.unique())
print(Covid.ReportingCountry.unique())
print(Covid.Vaccine.unique())

# Checking for missing values
print(Covid.isnull().sum())

# Filling the missing values with 0
Covid.fillna(value = 0, inplace=True)
print(Covid.isnull().sum())

# Setting the option to display all the rows and columns
pd.set_option('display.max_rows', None, 'display.max_columns', None)

# drop the columns not useful
Covid.drop(columns=["Denominator", "Region"], axis=0, inplace=True)
print(Covid.shape)

# New columns derived from existing columns
Covid['total_vac_administered']=Covid['FirstDose'] + Covid['SecondDose'] + Covid['UnknownDose']
Covid['FirstDose_perpop%']=100*Covid['FirstDose']/Covid['Population']
Covid['fullyvaccinated_perpop%']=100*Covid['SecondDose']/Covid['Population']
Covid['fullyvaccinated_perm']=10000008*Covid['SecondDose']/Covid['Population']
print(Covid.head(1))

# Slice the original dataframe to display the 'vaccines' and 'country' columns only.
# passing the list of the columns to the original dataset

df1 = Covid[["Vaccine", "ReportingCountry"]]
print(df1.head(10))

# the total number of countries reporting
print(len(Covid.ReportingCountry.unique()))

# Create a dictionary of each vaccine and its country of usage.

d = {}
for i in df1["Vaccine"].unique():
    d[i] = [df1["ReportingCountry"][j] for j in df1[df1["Vaccine"] == i].index]

# We need to remove repeated values in each key as the country names appear multiple times.

res = {}
for key, value in d.items():
    res[key] = set(value)

print(res)

# Find the number of values for each key in the dictionary.
# To count the number of countries using each vaccine.

for key, value in res.items():
    print(key, len([item for item in value if item]))

# Convert this into a dataframe

vacc_coun = pd.DataFrame.from_dict(res,orient='index')
print(vacc_coun)


# defining a function to reuse to return the sum of the column
def total(column):
    return column.sum()
print(Covid[['SecondDose', 'FirstDose', 'total_vac_administered', 'NumberDosesReceived']].agg(total))

# grouping the data by Reporting Country to get the total fully vaccinated per million for each country
vacc_per_mil = Covid.groupby('ReportingCountry').sum().sort_values('fullyvaccinated_perm', ascending=False)\
    .reset_index()
print(vacc_per_mil.head())

# plotting tht fully vaccinated total for each country
sns.set_style('darkgrid')
sns.set_palette('Blues')
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=vacc_per_mil, y="fullyvaccinated_perm", x="ReportingCountry")
ax.set_title('People Fully Vaccinated per million', color='black', fontsize=20, ha='left', weight='bold')
ax.set_xlabel('Country', fontsize=15, weight='bold', color='black')
ax.set_ylabel('People fully vaccinated', fontsize=15, weight='bold', color='black')
plt.show()
plt.clf()


# Slicing the original data to keep only 2 columns to get the population for each country
df2=Covid.groupby('ReportingCountry')['Population'].unique().reset_index()
print(df2)
# finding the total population of EU/EEA [453090377]
print(df2['Population'].sum())

# Total partially and fully vaccinated by age group in EU/EEA

df3=Covid.groupby('TargetGroup').sum().sort_values(['SecondDose', 'FirstDose'], ascending=[False, False]).reset_index()
print(df3)

sns.set(color_codes=True)
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=df3, y="SecondDose", x="TargetGroup", color='#2693d7')
ax.set_title('Fully vaccinated by Target group', color='black', fontsize=20, ha='left', weight='bold')
ax.set_xlabel('Target Group', fontsize=15, weight='bold', color='black')
ax.set_ylabel('People fully vaccinated', fontsize=15, weight='bold', color='black')
plt.show()
plt.clf()

# Using the the.iterrows()
df3=df3.set_index('TargetGroup')
print(df3.head(1))
for lab, row in df3.iterrows():
    print(lab + ":" + str(row["SecondDose"]))


# total vaccine administered by vaccine types
df5=Covid.groupby('Vaccine').sum().sort_values(['FirstDose', 'SecondDose', 'total_vac_administered', 'NumberDosesReceived'], ascending=[False, False, False, False]).reset_index()
print(df5)
df5_ind=df5.set_index('Vaccine')
for lab, row in df5_ind.iterrows():
    print(lab + ':' + "total_vac_administered" + ' ' + ':' + str(row["total_vac_administered"]))
    print(lab + ':' + "total partially vaccinated" + ' ' + ':' + str(row["FirstDose"]))
    print(lab + ':' + "total fully vaccinated" + ' ' + ':'+ str(row["SecondDose"]))
    print(lab + ':' + "total doses received" + ' ' + ':' + str(row['NumberDosesReceived']))


# plotting total vaccine administered
plt.figure(figsize=(6, 12))
sns.barplot(y="total_vac_administered", x="Vaccine", data=df5)
plt.ylabel("Total People Vaccinated", color="black", fontsize=15, weight='bold')
plt.xlabel("Vaccine Types", color="black", fontsize=15, weight='bold')
plt.title("Total People Vaccinated by vaccine type ", color="black", fontsize=20, weight='bold')
plt.show()



# slicing the data to find out the total vaccination for each country
countries = Covid.groupby(['ReportingCountry'])[['total_vac_administered', 'FirstDose_perpop%', 'fullyvaccinated_perpop%','fullyvaccinated_perm']].sum().reset_index()
print(countries.sort_values(['total_vac_administered'], ascending=False, ignore_index=True))
print(countries.sort_values(['FirstDose_perpop%'], ascending=False, ignore_index=True))
print(countries.sort_values(['fullyvaccinated_perpop%'], ascending=False, ignore_index=True))
print(countries.sort_values(['fullyvaccinated_perm'], ascending=False, ignore_index=True))


# Plotting Vaccine progress  in EU/EEA
Covid1=Covid.groupby('YearWeekISO').sum().reset_index()
print(Covid1.head)

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(19, 9))
plt.style.use('ggplot')
ax.plot(Covid1["YearWeekISO"], Covid1["total_vac_administered"], color='b', label='Total', linestyle='--', marker='.')
ax.plot(Covid1['YearWeekISO'], Covid1['FirstDose'], color='orange', label='Part_vaccinated', marker='.')
ax.plot(Covid1['YearWeekISO'], Covid1['SecondDose'], color='red', label='Fully_vaccinated', marker='.')
ax.set_ylabel('Number of people vaccinated', color="black", fontsize=15, weight='bold')
ax.set_xlabel("Date", fontsize=15, weight='bold')
ax.set_title('EU/EEA Weekly Vaccination', color="black", fontsize=20, weight='bold')
ax.legend()
plt.show()
plt.clf()






df4=Covid.groupby(['YearWeekISO', 'Vaccine'])['total_vac_administered'].agg([sum, max, np.mean, np.median]).reset_index()
df4=df4.set_index('YearWeekISO')
print(df4)

df6=Covid.groupby(['ReportingCountry', 'Vaccine'])['total_vac_administered'].sum().reset_index()
df6=df6.sort_values(['total_vac_administered'], ascending=False).reset_index(drop=True)
print(df6)



# Slicing data to get only the columns of interest
data=Covid[['ReportingCountry', 'FirstDose', 'SecondDose', 'FirstDose_perpop%', 'fullyvaccinated_perpop%', 'fullyvaccinated_perm', 'total_vac_administered', 'NumberDosesReceived']]
print(data.head(1))

# top 10 and top 3 countries - total vaccine administered

tot_vaccinated=data.groupby(['ReportingCountry'])['total_vac_administered'].sum().reset_index()
tot_vacc_top10=tot_vaccinated.sort_values(['total_vac_administered'], ascending=False).iloc[0:10].reset_index()
print(tot_vacc_top10)
print(tot_vacc_top10.iloc[0:3])

# plotting
sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=tot_vacc_top10, y="total_vac_administered", x="ReportingCountry")
ax.set_title('Top 10 Countries - Total Vaccinated People', color='black', fontsize=20, weight='bold')
ax.set_xlabel('Country', fontsize=15, weight='bold', color='black')
ax.set_ylabel('People vaccinated', fontsize=15, weight='bold', color='black')
plt.show()


# top 10 and top 3 countries - Partially vaccinated people

first_dose=data.groupby(['ReportingCountry'])['FirstDose'].sum().reset_index()
firstDose_top10=first_dose.sort_values(['FirstDose'], ascending=False).iloc[0:10].reset_index(drop=True)
print(firstDose_top10)
print(firstDose_top10.iloc[0:3])

# Plotting

sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=firstDose_top10, y="FirstDose", x="ReportingCountry")
ax.set_title('Top 10 Countries - Partially Vaccinated People', color='black', fontsize=20, weight='bold')
ax.set_xlabel('Country', fontsize=15, weight='bold', color='black')
ax.set_ylabel('People partially vaccinated', fontsize=15, weight='bold', color='black')
plt.show()


# top 10 and top 3 countries - Fully vaccinated people

Fully_vac=data.groupby(['ReportingCountry'])['SecondDose'].sum().reset_index()
Fully_vacc_top10=Fully_vac.sort_values(['SecondDose'], ascending=False).iloc[0:10].reset_index()
print(Fully_vacc_top10)
print(Fully_vacc_top10.iloc[0:3])

# Plotting top ten countries fully vaccinated people

sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=Fully_vacc_top10, y="SecondDose", x="ReportingCountry")
ax.set_title('Top 10 Countries - Fully Vaccinated People', color='black', fontsize=20, weight='bold')
ax.set_xlabel('Country', fontsize=15, weight='bold', color='black')
ax.set_ylabel('People fully vaccinated', fontsize=15, weight='bold', color='black')
plt.show()

# top 10 and top 3 countries - Partially vaccinated people per hundred (%)

firs_dose_percentage=data.groupby(['ReportingCountry'])['FirstDose_perpop%'].sum().reset_index()
first_percentage_top10=firs_dose_percentage.sort_values(['FirstDose_perpop%'], ascending=False).iloc[0:10].reset_index()
print(first_percentage_top10)
print(first_percentage_top10.iloc[0:3])

# Plotting

sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=first_percentage_top10, y="FirstDose_perpop%", x="ReportingCountry")
ax.set_title('Top 10 Countries - Partially Vaccinated People (%)', color='black', fontsize=20, weight='bold')
ax.set_xlabel('Country', fontsize=15, weight='bold', color='black')
ax.set_ylabel('People partially vaccinated (%)', fontsize=15, weight='bold', color='black')
plt.show()


# top 10 and top 3 countries - Fully Vaccinated people per hundred (%)

full_vacc_percentage=data.groupby(['ReportingCountry'])['fullyvaccinated_perpop%'].sum().reset_index()
full_percentage_top10=full_vacc_percentage.sort_values(['fullyvaccinated_perpop%'], ascending=False).iloc[0:10].reset_index()
print(full_percentage_top10)
print(full_percentage_top10.iloc[0:3, :])

# Plotting

sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=full_percentage_top10, y="fullyvaccinated_perpop%", x="ReportingCountry")
ax.set_title('Top 10 Countries - Fully Vaccinated People (%)', color='black', fontsize=20, weight='bold')
ax.set_xlabel('Country', fontsize=15, weight='bold', color='black')
ax.set_ylabel('People fully vaccinated (%)', fontsize=15, weight='bold', color='black')
plt.show()


# top 10 and top 3 countries - Fully vaccinated people per million

full_vacc_per_mill=data.groupby(['ReportingCountry'])['fullyvaccinated_perm'].sum().reset_index()
full_mill_top10=full_vacc_per_mill.sort_values(['fullyvaccinated_perm'], ascending=False).iloc[0:10].reset_index()
print(full_mill_top10)
print(full_mill_top10.iloc[0:3, :])

# Plotting

sns.set_style('darkgrid')
fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=full_mill_top10, y="fullyvaccinated_perm", x="ReportingCountry")
ax.set_title('Top 10 Countries - Fully Vaccinated People per million', color='black', fontsize=20, weight='bold')
ax.set_xlabel('Country', fontsize=15, weight='bold', color='black')
ax.set_ylabel('People fully vaccinated (%)', fontsize=15, weight='bold', color='black')
plt.show()


# Total number of doses received by each country

total_received=data.groupby(['ReportingCountry'])['NumberDosesReceived'].sum().reset_index()
total_received=total_received.sort_values(['NumberDosesReceived'], ascending=False).reset_index()
print(total_received)


# Ireland
vacc_Ireland= Covid.loc[Covid.ReportingCountry == 'IE']
print(vacc_Ireland.head())
vacc_Ireland.set_index('YearWeekISO', inplace=True)
print(vacc_Ireland.head())
print(vacc_Ireland.shape)
print(vacc_Ireland.info())
print(vacc_Ireland.describe())
print(vacc_Ireland.columns)


sns.set_style("darkgrid")
plt.figure(figsize=(20,6))
sns.lineplot(data=vacc_Ireland['total_vac_administered'], ci=None, label='Total vaccines administered')
sns.lineplot(data=vacc_Ireland['FirstDose'], ci=None, label='Partially vaccinated')
sns.lineplot(data=vacc_Ireland['SecondDose'], ci=None, label='Fully Vaccinated')
plt.title('Ireland Weekly Vaccination', fontsize=20, color='black', weight='bold')
plt.xlabel('Date', fontsize=15, color='black', weight='bold')
plt.ylabel('Weekly vaccinations', fontsize=15, color='black', weight='bold')
plt.legend()
plt.show()

#
print(vacc_Ireland[['SecondDose', 'FirstDose', 'NumberDosesReceived', 'total_vac_administered', 'FirstDose_perpop%', 'fullyvaccinated_perpop%', 'fullyvaccinated_perm']].agg(total))

#
Ireland=vacc_Ireland.groupby('Vaccine').sum().sort_values(['total_vac_administered'], ascending=False).reset_index()

#
sns.set_style('white')
plt.figure(figsize=(6,12))
sns.barplot(x="Vaccine", y="total_vac_administered", data=Ireland, ci=None, hue='Vaccine')
plt.ylabel("People Vaccinated",color="black", fontsize=15, weight='bold')
plt.xlabel("Vaccines",color = "black", fontsize=15, weight='bold')
plt.title("Total People Vaccinated by vaccine type",color = "black", fontsize=20, weight='bold')
plt.show()

