import sys
import numpy as np
import pandas as pd

print("init")

dataset = pd.read_csv("src\datasets\emscad_v1.csv")
#print(dataset.head())
#print(dataset.shape)

def duplicatedChecking(df):
    print("Number of duplicated rows detected",df.duplicated().sum()) # Check for Duplicated rows
    df.drop_duplicates(inplace=True) #Remove dupes
    print("Duplicated rows removed, updated rows",df.shape)

dataset[['country', 'state', 'city']] = dataset['location'].str.split(', ', expand=True, n = 2) #Seperating location column into respective categories 
location_to_fill_na = ['country', 'state', 'city'] 
dataset[location_to_fill_na] = dataset[location_to_fill_na].replace('', np.nan) #Fill empty fields with NaN

dataset[['min_salary', 'max_salary']] = dataset['salary_range'].str.split('-', expand=True, n = 1) #Seperating salary column into respective categories 
salary_to_fill_na = ['min_salary', 'max_salary']
dataset[salary_to_fill_na] = dataset[salary_to_fill_na].replace('', np.nan) #Fill empty fields with NaN   

dataset = dataset.drop(['location', 'salary_range'], axis=1)

duplicatedChecking(dataset)
print(dataset.info()) # Check col datatypes
print(dataset.describe()) 

print(dataset.columns[3]) # salary range



# Data exploration/validation
# 1. Check for cols with missing values dataset.columns[np.sum(dataset.isnull()) != 0]
# 2. we can see that we are able to split col location to Country, State, City etc. 

