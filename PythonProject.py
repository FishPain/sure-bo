import pandas as pd
import re

df = pd.read_csv("Dataset.csv")
replacing_columns = ['telecommuting','has_company_logo','has_questions','fraudulent','in_balanced_dataset']
replace_with = {'t': 1, 'f': 0}
columns_tags = ['company_profile', 'description', 'requirements', 'benefits']
def remove_html_tags(tags):
    RemoveTags = re.compile('<.*?>')
    return re.sub(RemoveTags, '', str(tags))

for column in replacing_columns:
    df[column] = df[column].replace(replace_with)

new_df = df.dropna()
new_df.loc[:, columns_tags] = new_df[columns_tags].map(remove_html_tags)
new_df.drop_duplicates(subset = 'title')

print(new_df)
