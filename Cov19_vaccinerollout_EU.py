# Import packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
print(os.getcwd())
# the data csv ito Pandas DataFrame
Covid = pd.read_csv('data.csv')
# set option for getting all the rows and columns when printing
pd.set_option('display.max_rows', None, 'display.max_columns', None)
# printing data head and tail
print(Covid.head(10))
print(Covid.tail(10))
# checking the shape of the data set
print(Covid.shape)
# observing data
print(Covid.describe())
print(Covid.describe(include='object'))
print(Covid.isnull().sum())
# Filling the missing values with 0
Covid.fillna(value = 0, inplace=True)
print(Covid.isnull().sum())
pd.set_option('display.max_rows', None, 'display.max_columns', None)
# printing the list of the columns name
print(Covid.columns)
# drop the columns not useful
Covid.drop(columns=["Denominator", "Region"], axis=0, inplace=True)
print(Covid.shape)
# New columns
Covid['total_vac_administered']=Covid['FirstDose'] + Covid['SecondDose'] + Covid['UnknownDose']
Covid['FirstDose_perpop%']=100*Covid['FirstDose']/Covid['Population']
Covid['fullyvaccinated_perpop%']=100*Covid['SecondDose']/Covid['Population']
Covid['fullyvaccinated_perm']=10000008*Covid['SecondDose']/Covid['Population']
print(Covid.head(1))

# Slice the original dataframe to display the 'vaccines' and 'country' columns only.

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


vacc_per_mil = Covid.groupby('ReportingCountry').sum().sort_values('fullyvaccinated_perm', ascending=False)\
    .reset_index()
print(vacc_per_mil.head())

fig, ax = plt.subplots(figsize=(14, 7))
sns.barplot(ax=ax, data=vacc_per_mil, y="fullyvaccinated_perm", x="ReportingCountry")
plt.show()
plt.clf()


def total(column):
    return column.sum()


print(Covid[['SecondDose', 'FirstDose', 'Population', 'NumberDosesReceived']].agg(total))
# finding the total population for each country
df2=Covid.groupby('ReportingCountry')['Population'].unique().reset_index()
print(df2)
# finding the total population of EU/EEA [453090377]
print(df2['Population'].sum())

# Total partially and fully vaccinated by age group in EU/EEA

df3=Covid.groupby('TargetGroup').sum().sort_values(['SecondDose', 'FirstDose'], ascending=[False, False]).reset_index()
print(df3)

