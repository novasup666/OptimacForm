from Optimac import allocate_action_to_participant,update_action_proportions
import pandas as pan
#import portalocker
import threading
from participant_real import Participant
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

'''
This is the program connecting the front code with the google sheet database
'''

participants_lock = threading.Lock()
motivation_lock = threading.Lock()
feedback_lock = threading.Lock()
suggestion_lock = threading.Lock()

def add_participant(age,gender, social_category,self_eval):
    #Connecting to the google sheet
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Lock to ensure that the action assignment is made in a sequential way
    participants_lock.acquire()

    # Acquiring the data
    participantsDF = conn.read(ttl=0,usecols=[0, 1,2,3,4,5],worksheet="participants")

    # Updating the data
    n = len(participantsDF)
    participantsDF.loc[n] = [datetime.today().strftime('%d-%m-%Y %H:%M:%S'),n+1,age,gender,social_category,self_eval]
       
    # Pushing thus update
    conn.update(worksheet=f"participants",data = participantsDF)
    st.cache_data.clear()

    #Unlock to enable other to access to the data
    participants_lock.release()  
    return n+1

def add_motivations(campaign_id,n,motivations,nb_opt= 0,optional = None):

    conn = st.connection("gsheets", type=GSheetsConnection)

    motivation_lock.acquire()

    motivationsDF = conn.read(ttl=0,usecols=list(range(3+nb_opt)),worksheet=f"motivations_{campaign_id}")

    i = 0
    motivationsDF_size = len(motivationsDF)
    for action in motivations:
        motivationsDF.loc[motivationsDF_size+i] = ([n,action, motivations[action]]+optional) if optional is not None else [n,action, motivations[action]]
        i+=1

    conn.update(worksheet=f"motivations_{campaign_id}",data = motivationsDF)
    st.cache_data.clear()

    motivation_lock.release()  
    


def add_feedback(campaign_id,n,motivations,feedbacks):
    conn = st.connection("gsheets", type=GSheetsConnection)

    feedback_lock.acquire()

    feedbackDF = conn.read(ttl=0,usecols=[0,1,2,3],worksheet=f"feedbacks_{campaign_id}")
    i = 0
    feedbackDF_size = len(feedbackDF)
    for action in motivations:
        feedbackDF.loc[feedbackDF_size + i] = [n,action,motivations[action],feedbacks[action]]
        i+=1
    conn.update(worksheet=f"feedbacks_{campaign_id}",data=feedbackDF)
    st.cache_data.clear()

    feedback_lock.release()

def add_suggestion(n,suggestion):
    conn = st.connection("gsheets", type=GSheetsConnection)
    suggestion_lock.acquire()

    feedbackDF = conn.read(ttl=0,usecols=[0,1],worksheet="suggestions")
    feedbackDF_size = len(feedbackDF)
    feedbackDF.loc[feedbackDF_size ] = [n,suggestion]
    conn.update(worksheet=f"suggestions",data=feedbackDF)
    st.cache_data.clear()

    suggestion_lock.release()