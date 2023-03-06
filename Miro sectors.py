#!/usr/bin/env python
# coding: utf-8

# ## Import Packages

# In[1]:


import pandas as pd



# ## Import Data and prepare data

# In[13]:


# Just remember to replace the file paths for the paths in your computer

# get inflation rate data
data_inf = pd.read_csv(r"D:\Work\Random Work\miro_inf_data.csv")


# get sector returns data
data_sectors = pd.read_csv(r"D:\Work\Random Work\miro_sector_data.csv")


# get benchmark returns data
data_bench = pd.read_csv(r"D:\Work\Random Work\miro_benchmark_data.csv")

# set dates as date_time 
data_inf['date'] = pd.to_datetime(data_inf['date'] )
data_sectors['date'] = pd.to_datetime(data_sectors['date'] )
data_bench['date'] = pd.to_datetime(data_bench['date'] )


# set date column as index for both dataframes
data_sectors.set_index('date', inplace=True)
data_bench.set_index('date', inplace=True)
data_inf.set_index('date', inplace=True)


# calculate excess returns vs benchmark
data_sectors_xsret = data_sectors.subtract(data_bench['benchmark'], axis=0)

# print to double check
print(data_sectors_xsret)
print(data_inf)


# ## Divide inflation into quartiles

# In[14]:


# calculate quartile cutoffs
q1_cutoff = data_inf['inflation_rate'].quantile(0.25)
q2_cutoff = data_inf['inflation_rate'].quantile(0.5)
q3_cutoff = data_inf['inflation_rate'].quantile(0.75)

# create function to classify periods into quartiles
def classify_inflation(row):
    if row['inflation_rate'] <= q1_cutoff:
        return '1st quartile'
    elif row['inflation_rate'] <= q2_cutoff:
        return '2nd quartile'
    elif row['inflation_rate'] <= q3_cutoff:
        return '3rd quartile'
    else:
        return '4th quartile'

# apply function to create new column with quartile classification
data_inf['inflation_regime'] = data_inf.apply(classify_inflation, axis=1)

# print to check
print(data_inf)


# ## Calculate average returns by inflation regime

# In[25]:


# merge inflation and sector returns dataframes
merged_data = pd.merge(left=data_sectors_xsret,right=data_inf, left_index=True, right_index=True)


# group returns by sector and inflation regime and calculate mean return for each group
grouped_data= merged_data.groupby(['inflation_regime']).mean().drop(columns=['inflation_rate'])


# group data by inflation regime and calculate annualized mean for each sector
sector_returns_by_regime = merged_data.groupby('inflation_regime').mean() * 12

# print results
print(sector_returns_by_regime)

sector_returns_by_regime.to_csv(r"D:\Work\Random Work\miro_results.csv")







