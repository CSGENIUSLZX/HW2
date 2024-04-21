# PPHA 30537
# Spring 2024
# Homework 2

# YOUR NAME HERE
#Zixuan Lan
# YOUR GITHUB USER NAME HERE
#CSGENIUSLZX

# Due date: Sunday April 21st before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.  Using functions for organization will be rewarded.

##################

# To answer these questions, you will use the csv document included in
# your repo.  In nst-est2022-alldata.csv: SUMLEV is the level of aggregation,
# where 10 is the whole US, and other values represent smaller geographies. 
# REGION is the fips code for the US region. STATE is the fips code for the 
# US state.  The other values are as per the data dictionary at:
# https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2020-2022/NST-EST2022-ALLDATA.pdf
# Note that each question will build on the modified dataframe from the
# question before.  Make sure the SettingWithCopyWarning is not raised.
import os

import pandas as pd
import us

os.chdir('D:/Github/homework-2-CSGENIUSLZX')
# PART 1: Macro Data Exploration
# Question 1.1: Load the population estimates file into a dataframe. Specify
# an absolute path using the Python os library to join filenames, so that
# anyone who clones your homework repo only needs to update one for all
# loading to work.
df=pd.read_csv('NST-EST2022-ALLDATA.csv')
df.head()

# Question 1.2: Your data only includes fips codes for states (STATE).  Use 
# the us library to crosswalk fips codes to state abbreviations.  Drop the
# fips codes.
df['state abbreviations']=df['STATE'].apply(lambda a:us.states.lookup(str(a)).abbr if us.states.lookup(str(a)) else None)
df['state abbreviations']

# Question 1.3: Then show code doing some basic exploration of the
# dataframe; imagine you are an intern and are handed a dataset that your
# boss isn't familiar with, and asks you to summarize for them.  Do not 
# create plots or use groupby; we will do that in future homeworks.  
# Show the relevant exploration output with print() statements.
df.head()
pd.set_option('display.max_columns',None)
summary=df.describe()
print(summary)

# Question 1.4: Subset the data so that only observations for individual
# US states remain, and only state abbreviations and data for the population
# estimates in 2020-2022 remain.  The dataframe should now have 4 columns.
df_subset=df[['state abbreviations','POPESTIMATE2020','POPESTIMATE2021','POPESTIMATE2022']]

# Question 1.5: Show only the 10 largest states by 2021 population estimates,
# in decending order.
df_10largest=df.sort_values('POPESTIMATE2021',ascending=False).head(10)
print(df_10largest)

# Question 1.6: Create a new column, POPCHANGE, that is equal to the change in
# population from 2020 to 2022.  How many states gained and how many lost
# population between these estimates?
df['POPCHANGE']=df['POPESTIMATE2022']-df['POPESTIMATE2020']
states_gained_number=(df['POPCHANGE']>0).sum()
states_lost_number=(df['POPCHANGE']<0).sum()

# Question 1.7: Show all the states that had an estimated change in either
# direction of smaller than 1000 people. 
small_change_statedateframe=df[abs(df['POPCHANGE'])<1000]
small_change_statedateframe['state abbreviations']

# Question 1.8: Show the states that had a population growth or loss of 
# greater than one standard deviation.  Do not create a new column in your
# dataframe.  Sort the result by decending order of the magnitude of 
# POPCHANGE.
std_popchange=df['POPCHANGE'].std()
qualitied_state=df[abs(df['POPCHANGE'])>std_popchange]
sorted_dataframe=qualitied_state.sort_values(by='POPCHANGE',key=abs,ascending=False)
print(sorted_dataframe)
#PART 2: Data manipulation

# Question 2.1: Reshape the data from wide to long, using the wide_to_long function,
# making sure you reset the index to the default values if any of your data is located 
# in the index.  What happened to the POPCHANGE column, and why should it be dropped?
# Explain in a brief (1-2 line) comment.
df_reset=df.reset_index()
df_reset['index']=range(len(df_reset))
df_long=pd.wide_to_long(df_reset, stubnames= 'POPESTIMATE', i='index', j='year')
#EXplain:Because we change the format of the dataframe,popchange is a col that added or subtraced by other cols, After the wide to long , it doesn't meet the change of our need.
df_long.drop('POPCHANGE', axis=1, inplace=True)
print(df_long)

# Question 2.2: Repeat the reshaping using the melt method.  Clean up the result so
# that it is the same as the result from 2.1 (without the POPCHANGE column).
df_reset=df.reset_index()
df_reset['index']=range(len(df_reset))
df_reset.set_index('index',inplace=True)
id_var=[col for col in df_reset.columns if col not in ['POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022']]
df_long_new=pd.melt(df_reset,id_vars=id_var,value_vars=['POPESTIMATE2020', 'POPESTIMATE2021', 'POPESTIMATE2022'])

# Question 2.3: Open the state-visits.xlsx file in Excel, and fill in the VISITED
# column with a dummy variable for whether you've visited a state or not.  If you
# haven't been to many states, then filling in a random selection of them
# is fine too.  Save your changes.  Then load the xlsx file as a dataframe in
# Python, and merge the VISITED column into your original wide-form population 
# dataframe, only keeping values that appear in both dataframes.  Are any 
# observations dropped from this?  Show code where you investigate your merge, 
# and display any observations that weren't in both dataframes.
df_stv=pd.read_excel('state-visits.xlsx')
df['STATE'] = df['STATE'].astype(str)
df_stv['STATE']=df_stv['STATE'].astype(str)
df_merged=df.merge(df_stv[['STATE','VISITED']],on='STATE',how='outer')
print(df_merged)
# Question 2.4: The file policy_uncertainty.xlsx contains monthly measures of 
# economic policy uncertainty for each state, beginning in different years for
# each state but ending in 2022 for all states.  The EPU_National column esimates
# uncertainty from national sources, EPU_State from state, and EPU_Composite 
# from both (EPU-N, EPU-S, EPU-C).  Load it as a dataframe, then calculate 
# the mean EPU-C value for each state/year, leaving only columns for state, 
# year, and EPU_Composite, with each row being a unique state-year combination.
df_policy=pd.read_excel('policy_uncertainty.xlsx')
df_policy.head(10)
df_new1=df_policy.groupby(['state','year'])['EPU_Composite'].mean().reset_index()
df_final=df_new1[['state','year','EPU_Composite']]
print(df_final)
# Question 2.5) Reshape the EPU data into wide format so that each row is unique 
# by state, and the columns represent the EPU-C values for the years 2022, 
# 2021, and 2020. 
df_selected_years = df_final[df_final['year'].isin([2020, 2021, 2022])]
df_wide = df_selected_years.pivot(index='state', columns='year', values='EPU_Composite')
df_wide['STATE']=df_wide['STATE'].apply(lambda a:us.states.lookup(str(a)).abbr if us.states.lookup(str(a)) else None)
print(df_wide)
# Question 2.6) Finally, merge this data into your merged data from question 2.3, 
# making sure the merge does what you expect.
df_merged.set_index('STATE', inplace=True)
df_wide.reset_index(inplace=True)
df_mergedfinal=df_merged.merge(df_wide,on='STATE',how='outer')
print(df_mergedfinal)
# Question 2.7: Using groupby on the VISITED column in the dataframe resulting S
# from the previous question, answer the following questions and show how you  
# calculated them: a) what is the single smallest state by 2022 population  
# that you have visited, and not visited?  b) what are the three largest states  
# by 2022 population you have visited, and the three largest states by 2022 
# population you have not visited? c) do states you have visited or states you  
# have not visited have a higher average EPU-C value in 2022?
df_new5=df_mergedfinal[['STATE','VISITED',2022]]
smallest_visited_state = df_new5[df_new5['VISITED'] == 1][2022].idxmin()
smallest_not_visited_state = df_new5[df_new5['VISITED'] == 0][2022].idxmin()
largest_visited_states = df_new5[df_new5['VISITED'] == 1].nlargest(3, 2022)['STATE']
largest_not_visited_states = df_new5[df_new5['VISITED'] == 0].nlargest(3, 2022)['STATE']
avg_epu_c_visited = df_new5[df_new5['VISITED'] == 1][2022].mean()
avg_epu_c_not_visited = df_new5[df_new5['VISITED'] == 0][2022].mean()
print(avg_epu_c_not_visited)
# Question 2.8: Transforming data to have mean zero and unit standard deviation
# is often called "standardization", or a "zscore".  The basic formula to 
# apply to any given value is: (value - mean) / std
# Return to the long-form EPU data you created in step 2.4 and then, using groupby
# and a function you write, transform the data so that the values for EPU-C
# have mean zero and unit standard deviation for each state.  Add these values
# to a new column named EPU_C_zscore.

mean_std = df_final.groupby('state')['EPU_Composite'].agg(['mean', 'std'])

z_scores = df_final.groupby('state')['EPU_Composite'].transform(
    lambda x: (x - x.mean()) / x.std()
)

df_final['EPU_C_zscore'] = z_scores

print(df_final.head())
