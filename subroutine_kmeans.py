#!/usr/bin/env python
# coding: utf-8

# ## 1.0 Libraries

# In[1]:


from IPython.display import display # get ipython for nicer output
import pandas as pd # to build dataframe
from tkinter import * # to have drop.down menues
import numpy as np
from tkinter import ttk
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib import pyplot
from sklearn.metrics import silhouette_score
from IPython.display import IFrame


# ## 1.1 Load Data

# In[2]:


df=pd.read_csv('data/song_data.csv')


# In[3]:


# drop old index column
df = df.drop(['Unnamed: 0'], axis=1)


# In[4]:


df['type'].head()


# In[5]:


df.info()


# In[6]:


# merge song title and artist together and write to a list
df['title_artist'] = df['track_name'].str.cat(others=df['artist_name'],sep='  BY  ')
# make lower case
df['title_artist'] = df['title_artist'].str.lower()
# drop duplicates
print(df['title_artist'].count())
df.drop_duplicates(subset=['title_artist'], keep='first', inplace=True, ignore_index=True)
print(df['title_artist'].count())


# In[7]:


df['title_artist'].head()


# In[8]:


# Create an alphabetical list of all the available songs
#songlist = []
#for i in range(len(df['title_artist'])):
#    songlist.append(df['title_artist'][i])
#songlist = sorted(songlist)


# ## 2. Building the KMeans Model

# ## 2.1. Preparing the data

# In[9]:


# compiling the features into a designated dataframe
df_features = df.drop(['type','id','uri','track_href','analysis_url','duration_ms','time_signature','track_name','artist_name','artist_id','title_artist'],axis=1)
df_features.head()                       


# ## 2.2 Scaling the features

# In[10]:


scaler = StandardScaler()
scaler.fit(df_features)
X_scaled = scaler.transform(df_features)
X_scaled_df = pd.DataFrame(X_scaled, columns = df_features.columns)
display(X_scaled_df.head())


# ## 2.3 Clustering the songs

# In[11]:


kmeans = KMeans(n_clusters=15, random_state=666)
kmeans.fit(X_scaled_df)


# In[12]:


# assign a cluster to each example
labels = kmeans.predict(X_scaled_df)
# retrieve unique clusters
clusters = np.unique(labels)
# create scatter plot for samples from each cluster
for cluster in clusters:
    # get row indexes for samples with this cluster
    row_ix = np.where(labels == cluster)
    # create scatter of these samples
    pyplot.scatter(df_features.to_numpy()[row_ix, 0], df_features.to_numpy()[row_ix, 1])
    # show the plot
pyplot.show()


# ##### Not much to see here

# In[13]:


# count number of songs per cluster

clusters = kmeans.predict(X_scaled_df)
#clusters
pd.Series(clusters).value_counts().sort_index()


# ## 2.4 Find optimal K

# K = range(2, 21)
# inertia = []
# 
# for k in K:
#     print("Training a K-Means model with {} clusters! ".format(k))
#     print()
#     kmeans = KMeans(n_clusters=k,
#                     random_state=666)
#     kmeans.fit(X_scaled_df)
#     inertia.append(kmeans.inertia_)
# 
# import numpy as np
# import matplotlib.pyplot as plt
# %matplotlib inline
# 
# plt.figure(figsize=(16,8))
# plt.plot(K, inertia, 'bx-')
# plt.xlabel('k')
# plt.ylabel('inertia')
# plt.xticks(np.arange(min(K), max(K)+1, 1.0))
# plt.title('Elbow Method showing the optimal k')

# ## 2.5 Bring the songs and the clusters together

# In[14]:


df['cluster'] = clusters
df.head()


# 
# 
# ## 3 Loading Spotify

# In[15]:


# Import credentials

import config

# Load Libraries and pass credentials to spotify API

import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.c_id, client_secret=config.c_se))


# user_input = input("What's you favorite Song:") # user input
# user_input = user_input.lower()
# if (df['Title'].str.lower() == user_input).any():
#     #df_exclude = df.drop(user_input.title(),axis=0)
#     print('You might also like:')
#     print(df['title_artist'].sample(n=1).values[0])
# else:
#     print('Unfortunately, the song is not in the hot list!')
