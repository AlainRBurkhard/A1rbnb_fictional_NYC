import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.image as mpimg
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster, FeatureGroupSubGroup
from folium import plugins
import streamlit as st


st.set_page_config( page_title= 'A1RBNB Dashboard', page_icon = '📈', layout = 'wide')

from airbnb_study_case import metric1
from airbnb_study_case import metric2
from airbnb_study_case import metric4
from airbnb_study_case import mean
from airbnb_study_case import std
from airbnb_study_case import fig
from airbnb_study_case import fig1
from airbnb_study_case import fig2
from airbnb_study_case import fig3
from airbnb_study_case import fig4
from airbnb_study_case import fig5
from airbnb_study_case import map2

with st.container():
    col1, col2, col3, col4= st.columns(4, gap="medium")
    with col1:
        st.metric(label='Number of Apt. registered',value = metric1, delta = None)
    with col2:
        st.metric(label='Number of Hosts', value = metric2, delta = None)
    with col3:
        st.metric(label='Avg. Price per Night', value = mean, delta = std)
    with col4:
        st.metric(label='Avg. Minimum Nights', value = metric4, delta = None)
 
with st.container():
    col1, col2, col3 = st.columns([0.8,1,1.5])
    with col1:
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        st.plotly_chart(fig1, use_container_width=True)
    with col3:
        st.plotly_chart(fig2,use_container_width=True)

with st.container():
    col1, col2 = st.columns(2, gap= "medium")
    with col1:
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.plotly_chart(fig4, use_container_width=True)

with st.container():
    col1, col2 =st.columns(2, gap= "medium")
    with col1:
        st.plotly_chart(fig5, use_container_width=True)
    #with col2:
     #   st.markdown(map2._repr_html_(), unsafe_allow_html=True)
