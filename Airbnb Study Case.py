#!/usr/bin/env python
# coding: utf-8

# In[1]:


#aibnb case study, importing csv data to jupyter notebook, pandas#


# In[2]:


import pandas as pd
import numpy as np
import plotly.express as px
get_ipython().system('pip install folium')
import folium


# In[3]:


df = pd.read_csv('/Users/Ramonpoopy/Desktop/Repos/mini-curso-ds/archive/AB_NYC_2019.csv') #df = dataframe#


# In[4]:


type(df)


# In[5]:


df.shape


# In[6]:


df.isna().sum()


# In[7]:


cols = ['host_name','price']
df.loc[:,cols]
df1=df.loc[:,cols]
df1 = df.dropna()


# In[8]:


df1.shape


# In[9]:


#Q1 - What's the mean of the rent in NYC

cols = ['price']
mean = df1.loc[:,cols]
np.mean(mean)


# In[10]:


#Q2 - how many regions have in NYC

cols=['neighbourhood_group']
quartiers = df1.loc[:,cols]
np.unique(quartiers)
q2=np.unique(quartiers)
print('The number of quartiers in NYC is' + ' ' + str(len(q2)) )


# In[11]:


#Q3 - what's the maximal value of the rent#

cols = ['price']
maxrent=df1.loc[:,cols]
np.max(maxrent)


# In[12]:


#number minimum of nights
cols=['minimum_nights']
md=df1.loc[:,cols]
np.mean(md)


# In[13]:


#different categories of room type
#question 4 of CEO
cols=['room_type']
md=df1.loc[:,cols]
np.unique(md)


# In[14]:


#how many and who are the users
cols=['host_id']
nm=md=df1.loc[:,cols]
np.unique(nm)
len(np.unique(nm))


# In[15]:


#Desvio padrao
cols=['price']
pc=df1.loc[:,cols]
mean=np.mean(pc)
std=np.std(pc)
print(mean)
print(std)


# In[16]:


#histogram price range

px.histogram(df1.loc[df1['price']<1000,:],'price',nbins=300,histnorm='',labels={'Number of appartments':'Price'},title='Number of appartments per price range',color_discrete_sequence=['green'])


# In[20]:


#what is the highest rent rate in every region of NYC?

#selecionar as colunas de interesse, bairro e preco

cols=['neighbourhood_group','price','latitude','longitude']
dataplt=df1.loc[df1['availability_365']>0,cols].groupby('neighbourhood_group').max().reset_index()
px.bar(dataplt, 'neighbourhood_group','price')


# In[21]:


dataplt


# In[22]:


map=folium.Map(zoom_start=14,control_scale=True)
for index, location_info in dataplt.iterrows():
    folium.Marker([location_info['latitude'],location_info['longitude']],popup=location_info['neighbourhood_group'] + ' ' + '$' + str(location_info['price'])).add_to(map)

map
map.fit_bounds(map.get_bounds(), padding=(40, 40))
map


# In[23]:


#adicionando uma nova coluna ao dataframe
cols=['neighbourhood_group','room_type','latitude','longitude']
dataplt=df1.loc[:,cols].sample(100)
dataplt.loc[:,'color']='NA'
dataplt


# In[24]:


#how to do it with for or if*
dataplt.loc[dataplt['room_type']=='Private room','color']='darkgreen'
dataplt.loc[dataplt['room_type']=='Entire home/apt','color']='blue'
dataplt.loc[dataplt['room_type']=='Shared room','color']='red'
dataplt


# In[26]:


for index, location_info in dataplt.iterrows():
    folium.Marker([location_info['latitude'],location_info['longitude']],
                  icon=folium.Icon(color=location_info['color'])).add_to(map)

map
map.fit_bounds(map.get_bounds(), padding=(40, 40))
map


# In[27]:


#Project is over

