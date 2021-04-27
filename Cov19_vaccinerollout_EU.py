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
