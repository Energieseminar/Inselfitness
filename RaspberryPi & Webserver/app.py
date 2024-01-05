# Import necessary libraries
import streamlit as st
import pandas as pd

# Create a small DataFrame for demonstration
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 22],
        'City': ['New York', 'San Francisco', 'Los Angeles']}

df = pd.DataFrame(data)

# Streamlit app
st.title('Simple DataFrame Viewer')

# Display the DataFrame
st.write('Here is a small DataFrame:')
st.dataframe(df)

# Additional Streamlit features can be added as needed
