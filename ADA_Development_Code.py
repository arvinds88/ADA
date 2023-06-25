#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import libraries
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import regex as re
import os
import seaborn as sns
from openpyxl import load_workbook
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import pymysql
from sqlalchemy import create_engine
import gc


# In[4]:


# DEFINE THE DATABASE CREDENTIALS
user = 'arvind.sADRDS'
password = 'ArVind#S#2029345'
host = 'prod-ad-read-replica.ckmtlvym9lwn.ap-south-1.rds.amazonaws.com'
port = 3306
database = 'educatio_educat'
  
# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
  
  
if __name__ == '__main__':
  
    try:
        
        # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
        engine = get_connection()
        print(
            f"Connection to the {host} for user {user} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)


# In[8]:


#Set up the connection with the item database
con = engine.connect()


# In[9]:


#Select all questions for Class 6 Maths which have all information required
query = "SELECT q.qcode, concat(q.question,'  (A)',q.optiona,'  (B)',q.optionb,'  (C)',q.optionc,'  (D)',q.optiond) as Question, q.correct_answer as Ans, q.skill as Topic, qp.difficulty as DI, qp.p_thetha FROM educatio_educat.questions q left join educatio_educat.assetD_questionParameters qp on q.qcode = qp.qcode where q.question_type = 'MCQ' and q.class = 6 and q.subjectno = 2 and q.correct_answer in ('A','B','C','D') and q.skill is not null and q.question is not null and q.optiona is not null and q.optionb is not null and q.optionc is not null and q.optiond is not null and qp.difficulty is not null "


# In[10]:


#Create Question Bank
question_bank = pd.DataFrame(con.execute(query))


# In[24]:


# sort the data by topic and difficulty in ascending order
question_bank.sort_values(by=['Topic','DI'],inplace=True)


# In[27]:


counts = question_bank['Topic'].value_counts()


# In[54]:


#Select the topics which have more than 5 questions
filtered_counts = counts[counts>5]


# In[55]:


#Take the first three topics from the list above
topic_unique = filtered_counts.index.to_list()[:3]


# In[ ]:


# this loops basically finds the starting question of medium deifficulty topic by topic


for topic in topic_unique:
    
    #filter the data for a topic to start with and select the first 3 items. 
    print(topic)
    df=question_bank[question_bank['Topic']==topic].head(5)
    temp_df=df
    temp_df.reset_index(inplace=True,drop=True)

    # finding the middle row with avg difficulty
    first_row=round(len(temp_df)/2)

    # find the index of the row with avg difficult
    i=(temp_df[temp_df['DI'] == temp_df['DI'].iloc[first_row]].index.values)[0]

    # this loops throws the question from a topic according to the answers recieved. 
    # Anytime a student answers the most difficult question correctly, it basically moves to another topic
    
    for j in range(0,5):
        if (i<0):
            # When i is less than 0, set i to 0 and ask question from the first row
            i=0
            q=input(temp_df._get_value(i, 'Question'))

            if (q==temp_df._get_value(i, 'Ans')) and temp_df._get_value(i, 'DI')!=max(temp_df['DI']) :
                # If the answer is correct and difficulty is not maximum, remove the row with same difficulty from temp_df
                temp_df=temp_df[temp_df['DI'] != temp_df._get_value(i, 'DI')]
                temp_df.reset_index(inplace=True,drop=True)
                i=i

            elif (q!=temp_df._get_value(i, 'Ans')) and temp_df._get_value(i, 'DI')!=max(temp_df['DI']):
                # If the answer is incorrect and difficulty is not maximum, remove the row with same difficulty from temp_df
                temp_df=temp_df[temp_df['DI'] != temp_df._get_value(i, 'DI')]
                temp_df.reset_index(inplace=True,drop=True)
                i=i-1

            else:
                # Break the loop if none of the above conditions are met
                break
        else:
            # When i is greater than or equal to 0, ask question from the row at index i
            i=i
            q=input(temp_df._get_value(i, 'Question'))

            if (q==temp_df._get_value(i, 'Ans')) and temp_df._get_value(i, 'DI')!=max(temp_df['DI']) :
                # If the answer is correct and difficulty is not maximum, remove the row with same difficulty from temp_df
                temp_df=temp_df[temp_df['DI'] != temp_df._get_value(i, 'DI')]
                temp_df.reset_index(inplace=True,drop=True)
                i=i

            elif (q!=temp_df._get_value(i, 'Ans')) and temp_df._get_value(i, 'DI')!=max(temp_df['DI']):
                # If the answer is incorrect and difficulty is not maximum, remove the row with same difficulty from temp_df
                temp_df=temp_df[temp_df['DI'] != temp_df._get_value(i, 'DI')]
                temp_df.reset_index(inplace=True,drop=True)
                i=i-1

            else:
                # Break the loop if none of the above conditions are met
                 break


# In[ ]:




