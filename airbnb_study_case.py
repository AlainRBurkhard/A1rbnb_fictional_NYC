import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.image as mpimg
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster, FeatureGroupSubGroup
from folium import plugins
import plotly.graph_objects as go

df = pd.read_csv('AB_NYC_2019.csv') #df = dataframe#

""" cleaning the date, nan empty cells
"""
cols = ['host_name','price']
df.loc[:,cols]
df1=df.loc[:,cols]
df1 = df.dropna()

metric1 = df1.loc[:,'id'].nunique()
metric2 = df1.loc[:,'host_id'].nunique()
# 3 - avg price of rent in NYC

mean = round(df1['price'].mean(), 2)
std = round(df1['price'].std(), 2)

# 4 avg metrics number minimum of nights

metric4=round(df1.loc[:,'minimum_nights'].mean(),2)

#  5 different categories of room type
#question 4 of CEO
md=df1.groupby('room_type')['id'].count()
fig = go.Figure(data=[go.Pie(labels=md.index, values=md.values)])
fig.update_layout(title='Distribution of Room Types')
# top hosts

top_host = df1.host_id.value_counts().head(10)
top_host_df = pd.DataFrame({'Host_ID': top_host.index.astype(str),
                            'Properties': top_host.values})

top_host = df1.host_id.value_counts().head(10)
top_host_df = pd.DataFrame({'Host_ID': top_host.index.astype(str),
                            'Properties': top_host.values})

fig1 = px.bar(top_host_df, x='Host_ID', y='Properties', 
             color='Properties', color_continuous_scale='Reds')
fig1.update_layout(title='Hosts with most properties in NYC', 
                  xaxis_title='Host ID', yaxis_title='Count of properties',
                  xaxis_tickangle=-45)

fig2 = px.histogram(df1.loc[df1['price']<1000,:], x='price', nbins=300, histnorm='', labels={'price':'Price'}, 
                    title='Distribution of Apartment Prices', 
                    color_discrete_sequence=['#00bcd4'], 
                    template='simple_white')
fig2.update_layout(
    font=dict(size=12),
    xaxis=dict(tickprefix="$", ticksuffix=""),
    yaxis=dict(title="Count"),
    margin=dict(l=50, r=50, t=50, b=50),
)
df2=df1[df1.price < 500]

fig3 = go.Figure(
    go.Violin(
        x=df2['neighbourhood_group'],
        y=df2['price'],
        box_visible=True,
        meanline_visible=True
    )
)

fig3.update_layout(
    title='Density and distribution of prices for each neighbourhood group',
    xaxis_title='Neighborhood Group',
    yaxis_title='Price'
)


sns.set_style('whitegrid')   # Set the style to whitegrid for a cleaner look
sns.set_palette('Set1')      # Choose a color palette that works well with the data

# Create the bar plot
g = sns.catplot(x='neighbourhood_group', y='price', hue='room_type', kind='bar', data=df, height=5, aspect=1.5)

# Extract the axes object
ax = g.ax

# Customize the plot
ax.set_xlabel('Neighbourhood Group')  # Set the x-axis label
ax.set_ylabel('Price per Night')  # Set the y-axis label
ax.set_title('Average Listing Prices by Neighbourhood Group and Room Type')  # Set the title
ax.legend(title='Room Type', loc='upper right', labels=['Entire home/apt', 'Private room', 'Shared room'], bbox_to_anchor=(1.15, 1)) # Adjust the legend position
fig4 = plt.tight_layout()  # Adjust the layout to prevent overlapping text

# Group the data by neighborhood group and find the top 10 apartments with highest price for each group
top_10 = (df1.groupby('neighbourhood_group').apply(lambda x: x.nlargest(5, 'price')))
# Reset the index to remove the multi-level grouping
top_10 = top_10.reset_index(drop=True)

# Create a scatter mapbox plot with markers for the top 10 apartments in each neighborhood group
fig5 = px.scatter_mapbox(top_10, lat="latitude", lon="longitude", hover_name="neighbourhood_group", hover_data=["price"],
                        color="neighbourhood_group", zoom=10, height=500, size=[1]*len(top_10))

# Customize the map layout
fig5.update_layout(mapbox_style="open-street-map")
fig5.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

colors = {
    'Entire home/apt': 'blue',
    'Private room': 'green',
    'Shared room': 'red'
}

# Create a map
map2 = folium.Map(location=[40.73, -73.98], zoom_start=10)

# Create a MarkerCluster layer for each neighborhood group
for neighborhood_group in df1['neighbourhood_group'].unique():

    # Filter the data for the current neighborhood group
    df_ng = df1[df1['neighbourhood_group'] == neighborhood_group]

    # Add a MarkerCluster layer for the current neighborhood group
    marker_cluster = MarkerCluster(name=neighborhood_group)
    map2.add_child(marker_cluster)

    # Add markers with pie charts for each room type
    for index, row in df_ng.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            icon=folium.Icon(color=colors[row['room_type']]),
            popup='<b>{}</b><br>Room type: {}<br>Avg price: ${:,.0f}<br>Count: {:,.0f}'.format(
                neighborhood_group, row['room_type'], row['price'], row['id']),
            tooltip='Neighborhood group: {}'.format(neighborhood_group)
        ).add_to(marker_cluster)

# Add a layer control to the map
folium.LayerControl().add_to(map2)

