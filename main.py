import numpy as np
import streamlit as st
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from matplotlib import pyplot

df = pd.read_csv("us_births_2016_2021.csv")

st.title("Visualization of Birth Data Related to Education Level")
# finding all parents with undergraduate and below level of education
undergraduate = df[(df['Education Level Code'] <= 5) & (df['Education Level Code'] > 0)].copy()
undergraduate.drop(columns=['State', 'Year', 'Gender', 'Education Level of Mother', 'Education Level Code',
                            'Average Age of Mother (years)', 'Average Birth Weight (g)'], axis=1, inplace=True)
undergrad_by_state_total = undergraduate.groupby("State Abbreviation")

# creating streamlit display for undergrad state totals
st.header("Total Number of Births by State (2016-2021)")
st.subheader("Education Level: Undergraduate and Below")
undergrad_options = ['Most Births', 'Least Births']
undergrad_display = st.radio('Sort by states with:', undergrad_options)
if undergrad_display == 'Most Births':
    st.bar_chart(undergrad_by_state_total.sum().sort_values('Number of Births').tail(15))
else:
    st.bar_chart(undergrad_by_state_total.sum().sort_values('Number of Births').head(15))

# finding all parents with graduate and above education level
graduate = df[df['Education Level Code'] > 5].copy()
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

# Line plot segment begins
avg_year = df[['State Abbreviation', 'Year', 'Average Age of Mother (years)']].copy()

# Obtaining information regarding selected abbreviation

# dropping state abbreviation


# streamlit display
st.subheader("View the average age of mother by state from 2016-2021")
state_abbreviations = df['State Abbreviation'].unique()
# creating select box
option_choice = st.selectbox('Select State', state_abbreviations)

# selecting information correlating to selected option
avg_year = avg_year[avg_year['State Abbreviation'] == option_choice]

avg_year.drop(columns=['State Abbreviation'], axis=1, inplace=True)

# displaying pyplot
pyplot.plot(avg_year.groupby('Year').median())
pyplot.ylabel("Average Age")
pyplot.xlabel("Year")
pyplot.title("Average age of mother from 2016-2021")
st.pyplot(pyplot)

# streamlit display for prediction
st.subheader("Predict education level of mother for given year and age")
option_choice_year = st.selectbox('Select Year', [2016, 2017, 2018, 2019, 2020, 2021], key=21)
age = st.slider('An age between 22 and 40', min_value=24, max_value=40)
st.write('Age: ', age)
submit = st.button("Predict Education Level")
for_prediction = df[df['Education Level Code'] > 0].copy()
if submit:
    # training the model
    mylin_model = LinearRegression()
    for_prediction = df[df['Education Level Code'] > 0].copy()
    for_prediction.drop(for_prediction.index[for_prediction['Year'] != int(option_choice_year)], inplace=True)
    x_train, x_test, y_train, y_test = train_test_split(for_prediction['Average Age of Mother (years)'],
                                                        for_prediction['Education Level Code'])
    mylin_model.fit(x_train.values.reshape(-1, 1), y_train.values)

    # Obtaining prediction and writing display message
    prediction = mylin_model.predict(np.array([[age]]))[0]
    prediction = round(prediction)
    if prediction < 3:
        sout = 'Some High School'
    elif prediction == 3:
        sout = 'High School Diploma or GED'
    elif prediction == 4:
        sout = 'Some college'
    elif prediction == 5:
        sout = 'Associate\'s Degree'
    elif prediction == 6:
        sout = 'Bachelor\'s Degree'
    elif prediction == 7:
        sout = 'Master\'s Degree'
    elif prediction >= 8:
        sout = 'Doctorate\'s Degree'
    st.write('Approximate Education Level Prediction:', sout)


