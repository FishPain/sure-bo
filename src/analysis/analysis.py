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
    
duplicatedChecking(dataset)
print(dataset.info()) # Check col datatypes
print(dataset.describe()) 

print(dataset.columns[3]) # salary range

# Data exploration/validation
# 1. Check for cols with missing values dataset.columns[np.sum(dataset.isnull()) != 0]
# 2. we can see that we are able to split col location to Country, State, City etc. 
