import streamlit as st
import pandas as pd
import numpy as np
import sklearn
from matplotlib import pyplot

df = pd.read_csv("us_births_2016_2021.csv")

# finding all parents with undergraduate and below level of education
undergraduate = df[(df['Education Level Code'] < 5) & (df['Education Level Code'] > 0)]
undergraduate.drop(columns=['State', 'Year', 'Gender', 'Education Level of Mother', 'Education Level Code',
                                  'Average Age of Mother (years)', 'Average Birth Weight (g)'], axis=1, inplace=True)
undergrad_by_state_total = undergraduate.groupby("State Abbreviation")
print(undergrad_by_state_total.sum())





