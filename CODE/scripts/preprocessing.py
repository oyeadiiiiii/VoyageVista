import numpy as np
import pandas as pd
from scipy import stats
from sklearn import preprocessing

# Load the dataset
df = pd.read_csv("D:\PROJECTS\VoyageVista\CODE\data\h1b_kaggle.csv")

# Dropping unnecessary columns
df.drop(['Unnamed: 0', 'EMPLOYER_NAME', 'JOB_TITLE', 'WORKSITE', 'lon', 'lat'], axis=1, inplace=True)

# Handling missing values
df['CASE_STATUS'].fillna(df['CASE_STATUS'].mode().iloc[0], inplace=True)
df['SOC_NAME'].fillna(df['SOC_NAME'].mode().iloc[0], inplace=True)
df['FULL_TIME_POSITION'].fillna(df['FULL_TIME_POSITION'].mode().iloc[0], inplace=True)
df['YEAR'].fillna(df['YEAR'].mode().iloc[0], inplace=True)
df['PREVAILING_WAGE'].fillna(df['PREVAILING_WAGE'].median(), inplace=True)

# Mapping categorical variables
df['CASE_STATUS'] = df['CASE_STATUS'].map({'CERTIFIED': 0, 'CERTIFIED-WITHDRAWN': 1, 'DENIED': 2,
                                           'WITHDRAWN': 3, 'PENDING QUALITY AND COMPLIANCE REVIEW - UNASSIGNED': 4,
                                           'REJECTED': 5, 'INVALIDATED': 6})
df['FULL_TIME_POSITION'] = df['FULL_TIME_POSITION'].map({'N': 0, 'Y': 1})

# SOC_NAME encoding
df['SOC_NAME_NEW'] = 'others'
df.loc[df['SOC_NAME'].str.contains('CHIEF|EXECUTIVES', na=False), 'SOC_NAME_NEW'] = 'Executives'
df.loc[df['SOC_NAME'].str.contains('Computer|Software', na=False), 'SOC_NAME_NEW'] = 'IT'
df.loc[df['SOC_NAME'].str.contains('Chief|Management|MANAGERS', na=False), 'SOC_NAME_NEW'] = 'Manager'
df.loc[df['SOC_NAME'].str.contains('Mechanical', na=False), 'SOC_NAME_NEW'] = 'Mechanical'
df.loc[df['SOC_NAME'].str.contains('Database', na=False), 'SOC_NAME_NEW'] = 'Database'

# Encode SOC_NAME_NEW
le = preprocessing.LabelEncoder()
df['SOC_N'] = le.fit_transform(df['SOC_NAME_NEW'])
df.drop(['SOC_NAME', 'SOC_NAME_NEW'], axis=1, inplace=True)

# Removing outliers
z = np.abs(stats.zscore(df))
df_no_outliers = df[(z <= 3).all(axis=1)]

# Bifurcating dependent and independent variables
selcols = ["FULL_TIME_POSITION", "PREVAILING_WAGE", "YEAR", "SOC_N"]
x = df_no_outliers[selcols]
y = df_no_outliers['CASE_STATUS']

# Save preprocessed data for training
x.to_csv("D:\PROJECTS\VoyageVista\CODE\data/x_preprocessed.csv", index=False)
y.to_csv("D:\PROJECTS\VoyageVista\CODE\data/y_preprocessed.csv", index=False)

#import pandas as pd

#df = pd.read_csv("D:\PROJECTS\VoyageVista\CODE\data\y_preprocesse.csv")  

#df.replace({1: 0, 2: 1}, inplace=True)

# print(df.head())

#df.to_csv("D:\PROJECTS\VoyageVista\CODE\data\y_preprocessed.csv", index=False)
