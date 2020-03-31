import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
"""
# My first app
Here's our first attempt at using data to create a table:
"""

df = pd.DataFrame({
  'first column': [5, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df


"""
### This is a Checkbox
"""

option = st.selectbox(
    'Which number do you like best?',
     df['first column'], key=1)

'You selected: ', option

"""
### This is a line chart
"""
chart_data = pd.DataFrame(
  np.random.randn(20, 3),
  columns=['a', 'b', 'c'])
st.line_chart(chart_data)
"""
### This is a line chart conditioned with a checkbox
"""

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

option1 = st.sidebar.selectbox(
    'Which number do you like best?',
     df['first column'], key=2)

'You selected:', option1

"""
### This is a progress bar
"""

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'