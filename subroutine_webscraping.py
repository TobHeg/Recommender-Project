#!/usr/bin/env python
# coding: utf-8

# ## 1.1 Import Libraries

# In[1]:


from bs4 import BeautifulSoup # to extract data from web
import requests # to pull website
import pandas as pd # to build dataframe


# ## 1.1. Web Scraping

# In[2]:


# Select website to scrap
url='https://www.billboard.com/charts/hot-100/'


# In[3]:


# download html with a get request
response = requests.get(url)


# In[4]:


response.status_code # 200 status code means OK!


# In[5]:


# parse html (create the 'soup')
soup = BeautifulSoup(response.content, "html.parser")


# ## 1.2 Build DataFrame

# In[6]:


# title list from h3
title=[]
for i in soup.select('li.o-chart-results-list__item h3'):
    title.append(i.get_text())


# In[7]:


# clean from /n
clean_title_list = []
for element in title:

    clean_title_list.append(element.strip())


# In[8]:


# All the other info into one big list
big_list=[]
for i in soup.select('li.o-chart-results-list__item span'):
    big_list.append(i.get_text())


# In[9]:


# Clean from /n
clean_big_list = []
for element in big_list:

    clean_big_list.append(element.strip())


# In[10]:


# Exclude 'New' and 'Re-Enter' as it screws with the order of elements

while 'NEW' in clean_big_list:
    clean_big_list.remove('NEW')
while 'RE-\nENTER' in clean_big_list:
    clean_big_list.remove('RE-\nENTER')


# In[11]:


# Finally fill all the lists
rank = clean_big_list[0::8]
artist = clean_big_list[1::8]
last_week = clean_big_list[2::8]
peak_pos = clean_big_list[3::8]
wks_on_chart = clean_big_list[4::8]


# In[12]:


# Create a dictionary out of the lists
dic = {'Rank':rank,'Artist':artist,'Title':clean_title_list,'Last Week':last_week,'Peak Position':peak_pos,'Weeks on Chart':wks_on_chart}


# In[13]:


# Create a Dataframe out of the Dictionary
df = pd.DataFrame(dic)


# In[14]:


# combine title and artist into one column
df['title_artist'] = df['Title'].str.cat(others=df['Artist'],sep='  BY  ')
# make lower case
df['title_artist'] = df['title_artist'].str.lower()


# ## 2. Output into csv

# In[15]:


df.to_csv('data/Top100.csv', index = False)

