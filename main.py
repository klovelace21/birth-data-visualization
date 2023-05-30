import streamlit as st
import pandas as pd
import numpy as np
import sklearn
from matplotlib import pyplot

df = pd.read_csv("us_births_2016_2021.csv")

st.title("Visualization of Birth Data Related to Education Level")
# finding all parents with undergraduate and below level of education
undergraduate = df[(df['Education Level Code'] <= 5) & (df['Education Level Code'] > 0)]
undergraduate.drop(columns=['State', 'Year', 'Gender', 'Education Level of Mother', 'Education Level Code',
                                  'Average Age of Mother (years)', 'Average Birth Weight (g)'], axis=1, inplace=True)
undergrad_by_state_total = undergraduate.groupby("State Abbreviation")

# creating streamlit display for undergrad state totals
st.header("Total Number of Births by State")
st.subheader("Education Level: Undergraduate and Below")
undergrad_options = ['Most Births', 'Least Births']
undergrad_display = st.radio('Sort by states with:', undergrad_options)
if undergrad_display == 'Most Births':
    st.bar_chart(undergrad_by_state_total.sum().sort_values('Number of Births').tail(15))
else:
    st.bar_chart(undergrad_by_state_total.sum().sort_values('Number of Births').head(15))

# finding all parents with graduate and above education level
graduate = df[df['Education Level Code'] > 5]
graduate.drop(columns=['State', 'Year', 'Gender', 'Education Level of Mother', 'Education Level Code',
                                  'Average Age of Mother (years)', 'Average Birth Weight (g)'], axis=1, inplace=True)
graduate_by_state_total = graduate.groupby("State Abbreviation")

# creating streamlit display for graduate state totals
st.subheader("Education Level: Graduate and Above")
grad_options = ['Most Births', 'Least Births']
grad_display = st.radio('Sort by states with:', grad_options, key=10)
if grad_display == 'Most Births':
    st.bar_chart(graduate_by_state_total.sum().sort_values('Number of Births').tail(15))
else:
    st.bar_chart(graduate_by_state_total.sum().sort_values('Number of Births').head(15))








