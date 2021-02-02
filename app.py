import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
import json


ids = []
lockUnlock = []
offOn = []


resp=requests.get("https://api.thingspeak.com/channels/1091956/feeds.json?results=10") #read all fields, 10 values
#resp=requests.get("https://api.thingspeak.com/channels/645078/fields/2.json?results=10") #to read only field 2, 10 values

print(resp.text)
results=json.loads(resp.text) #convert json into Python object

for x in range(10):
    ids.append(results["feeds"][x]["field1"])
    lockUnlock.append(results["feeds"][x]["field2"])
    offOn.append(results["feeds"][x]["field3"])
    print("Downloaded sample",x,": id =",results["feeds"][x]["field1"],", lockUnlock =",results["feeds"][x]["field2"],", offOn =",results["feeds"][x]["field3"])



st.title('Intruder alert door system')

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': ids,
    'second column': lockUnlock,
    'third column': offOn
}))



chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)



map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)



if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)



df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

option1 = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option1



#option2 = st.sidebar.selectbox(
#    'Which number do you like best?',
#     df['first column'])

#'You selected:', option2



left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")



# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text('hi')
  bar.progress(i + 1)
  time.sleep(0.1)
