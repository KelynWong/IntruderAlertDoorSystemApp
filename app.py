import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
import json
import datetime
import _strptime
from PIL import Image

dateList = []
numberList = []

dates = []
noOfEnter = []

count = 0
totalOfThatDay = 0

resp=requests.get("https://api.thingspeak.com/channels/1230188/fields/1.json?results=8000") #to read only field 2, 10 values
results=json.loads(resp.text) #convert json into Python object
feeds = results["feeds"]
for x in range(len(feeds)):
    if feeds[x]["field1"] != None:
        date_time_obj = datetime.datetime.strptime(feeds[x]["created_at"], '%Y-%m-%dT%H:%M:%SZ')
        dateList.append(date_time_obj.date())
        numberList.append(int(feeds[x]["field1"]))

for x in range(len(numberList)):
    temp = dateList[x]
    if x + 1 != len(numberList):
        if dateList[x + 1] == temp:
            totalOfThatDay = totalOfThatDay + 1
        else:
            totalOfThatDay = totalOfThatDay + 1
            dates.append(temp.strftime('%d/%m/%Y'))
            noOfEnter.append(totalOfThatDay)
            totalOfThatDay = 0
        temp = dateList[x + 1]
    else:
        totalOfThatDay = totalOfThatDay + 1
        dates.append(temp.strftime('%d/%m/%Y'))
        noOfEnter.append(totalOfThatDay)


st.title('Intruder alert door system')
st.header('Live video')
st.markdown("""
<iframe width="560" height="315" src="https://youtu.be/HMlbBscdvzs" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
""", unsafe_allow_html=True)

st.header('Analytics')

col1, col2 = st.beta_columns([1.5,3])
df = pd.DataFrame({
  'date': dates,
  'noOfEnter': noOfEnter
})


df = df.rename(columns={'date':'index'}).set_index('index')
col1.subheader("Table of data")
col1.write(df)
col2.subheader("Chart of data")
col2.line_chart(df)


st.header('Controls')

st.subheader('Send message to display on LCD')
user_input = st.text_input("Message")
sendMessage = st.button('Send');
if sendMessage:
    print('Send message')
    requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&status={}".format(user_input))

col3, col4 = st.beta_columns(2)
st.text('Buttons can only trigger every 15 secs')
with col3:
    st.subheader('Buzzer')
    buzzerOnButton = st.button('On buzzer');
    buzzerOffButton = st.button('Off buzzer');
    if buzzerOnButton:
        image = Image.open('switch-on.png')
        st.image(image, caption='Buzzer On', width=100)
        requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&field3=1")
    if buzzerOffButton:
        image = Image.open('switch-off.png')
        st.image(image, caption='Buzzer Off', width=100)
        requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&field3=0")
    #get data from thingspeak to check if buzzer is currently on or off
    resp=requests.get("https://api.thingspeak.com/channels/1230188/fields/3.json") #to read only field 2, 10 values
    results=json.loads(resp.text) #convert json into Python object
    feeds = results["feeds"]
    for x in range(len(feeds)):
        if feeds[x]["field3"] != None:
            numberList.append(int(feeds[x]["field3"]))
    if buzzerOffButton == False and buzzerOnButton == False:
        if numberList[len(numberList)-1] == 1:
            image = Image.open('switch-on.png')
            st.image(image, caption='Buzzer is currently on', width=100)
        else:
            image = Image.open('switch-off.png')
            st.image(image, caption='Buzzer is currently off', width=100)


with col4:
    st.subheader('Door')
    doorUnlockButton = st.button('Unlock door');
    doorLockButton = st.button('Lock door');
    if doorUnlockButton:
        image = Image.open('unlocked.png')
        st.image(image, caption='Door unlocked', width=100)
        requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&field2=1")
    
    if doorLockButton:
        image = Image.open('lock.png')
        st.image(image, caption='Door locked', width=100)
        requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&field2=0")
    
    #get data from thingspeak to check if door is currently unlock or locked
    resp=requests.get("https://api.thingspeak.com/channels/1230188/fields/2.json") #to read only field 2, 10 values
    results=json.loads(resp.text) #convert json into Python object
    feeds = results["feeds"]
    for x in range(len(feeds)):
        if feeds[x]["field2"] != None:
            numberList.append(int(feeds[x]["field2"]))
    if doorUnlockButton == False and doorLockButton == False:    
        if numberList[len(numberList)-1]:
            image = Image.open('unlocked.png')
            st.image(image, caption='Door is currently unlocked', width=100)
        else:
            image = Image.open('lock.png')
            st.image(image, caption='Door is currently locked', width=100)

