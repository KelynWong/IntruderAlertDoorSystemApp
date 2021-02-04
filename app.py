import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
import json
import datetime
import _strptime

dateList = []
numberList = []

dates = []
noOfEnter = []

count = 0
totalOfThatDay = 0

resp=requests.get("https://api.thingspeak.com/channels/1230188/fields/1.json") #to read only field 2, 10 values


results=json.loads(resp.text) #convert json into Python object
feeds = results["feeds"]

for x in range(len(feeds)):
    if feeds[x]["field1"] != None:
        date_time_obj = datetime.datetime.strptime(feeds[x]["created_at"], '%Y-%m-%dT%H:%M:%SZ')
        dateList.append(date_time_obj.date())
        numberList.append(int(results["feeds"][x]["field1"]))

for x in range(len(numberList)):
    temp = dateList[x]
    if x + 1 != len(numberList):
        if dateList[x + 1] == temp:
            totalOfThatDay = totalOfThatDay + 1
            if x == 1:
                totalOfThatDay = totalOfThatDay + 1
        else:
            dates.append(temp.strftime('%d/%m/%Y'))
            noOfEnter.append(totalOfThatDay)
            totalOfThatDay = 0
        temp = dateList[x + 1]
    else:
        totalOfThatDay = totalOfThatDay + 1
        dates.append(temp.strftime('%d/%m/%Y'))
        noOfEnter.append(totalOfThatDay)

st.title('Intruder alert door system')

df = pd.DataFrame({
  'date': dates,
  'noOfEnter': noOfEnter
})

df = df.rename(columns={'date':'index'}).set_index('index')

df

st.line_chart(df)


buzzerOnButton = st.button('On buzzer');
buzzerOffButton = st.button('Off buzzer');
doorUnlockButton = st.button('Unlock door');
doorLockButton = st.button('Lock door');

if buzzerOnButton:
    st.write('The buzzer is currently on')
    requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&field3=1")

if buzzerOffButton:
    st.write('The buzzer is currently off')
    requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&field3=0")

if doorUnlockButton:
    st.write('The door is currently unlocked')
    requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&field2=1")

if doorLockButton:
    st.write('The door is currently locked')
    requests.get("https://api.thingspeak.com/update?api_key=Q539CRA8JC5EWP86&field2=0")

