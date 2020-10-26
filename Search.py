#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Data Manipulation
import pandas as pd

# System
import sys

# Packages to upload to firebase
import json
import requests


# In[2]:


# Inputs
sys.argv[1] = ['Koreatown', 'Bel Air']
sys.argv[2] = ['CrimeCount', 'CrimeScore']

NEIGHBORHOODS = sys.argv[1]
FEATURES = sys.argv[2]


# In[3]:


def search_neighborhoods_features(NEIGHBORHOODS, FEATURES):

    query_output_dict = {}

    # First populate the query_output_dict
    for feat in FEATURES:
        for neig in NEIGHBORHOODS:
            query_output_dict[neig] = {feat: None}

    # Then query
    for feat in FEATURES:
        for neig in NEIGHBORHOODS:
            query = f'https://neighborhood-score-la.firebaseio.com/{feat}/{neig}.json'
            json_query = requests.get(query)
            dict_query = json.loads(json_query.text)
            query_output_dict[neig][feat] = dict_query

    df_output = pd.DataFrame.from_dict(query_output_dict).T 
    
    return df_output


# In[4]:


def search_neighborhoods(NEIGHBORHOODS):

    query_output_dict = {}

    for neig in NEIGHBORHOODS:
        query = f'https://neighborhood-score-la.firebaseio.com/NeighborhoodData/{neig}.json'
        json_query = requests.get(query)
        dict_query = json.loads(json_query.text)
        query_output_dict[neig] = dict_query

    df_output = pd.DataFrame.from_dict(query_output_dict).T
    
    return df_output


# In[5]:


def search_features(FEATURES):

    query_output_dict = {}

    for feat in FEATURES:
        query = f'https://neighborhood-score-la.firebaseio.com/{feat}.json'
        json_query = requests.get(query)
        dict_query = json.loads(json_query.text)
        query_output_dict[feat] = dict_query

    df_output = pd.DataFrame.from_dict(query_output_dict)
    
    return df_output


# In[6]:


#search_neighborhoods_features(NEIGHBORHOODS, FEATURES)


# In[7]:


#search_neighborhoods(NEIGHBORHOODS)


# In[8]:


#search_features(FEATURES)


# In[ ]:




