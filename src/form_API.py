from Optimac import allocate_action_to_participant,update_action_proportions
import pandas as pan
#import portalocker
import threading
from participant_real import Participant
import streamlit as st
from streamlit_gsheets import GSheetsConnection


allocated_actions_file_name = "../data/allocated_actions.csv"
action_stats_file_name = "../data/action_stats.csv"
'''
This is used to create forms etc

data.csv stores the allocated actions with following columns: n, action_label, motivation (of the participant for said action)
'''

participants_lock = threading.Lock()
motivation_lock = threading.Lock()
feedback_lock = threading.Lock()
suggestion_lock = threading.Lock()

def add_participant(age,gender, social_category,self_eval):
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Lock to ensure that the action assignment is made in a sequential way
    participants_lock.acquire()

    #Transform the data stored in a google sheet to data structures compatible with the OPTIMAC algorithm
    # allocationDF = conn.read(ttl=0,usecols=[0, 1,2],worksheet="allocated_actions")
    # actionstatsDF = conn.read(ttl=0,usecols=[0, 1,2,3],worksheet="actions_stats")

    participantsDF = conn.read(ttl=0,usecols=[0, 1,2,3,4],worksheet="participants")

    # allocated_actions  = allocationDF.values.tolist()
    # list_actions = {line[0]:{'target':line[1], 'current':line[2],'minimum':line[3]} for line in actionstatsDF.values}

    n = len(participantsDF)

    participantsDF.loc[n] = [n+1,age,gender,social_category,self_eval]
       
    conn.update(worksheet=f"participants",data = participantsDF)
    st.cache_data.clear()

    #Unlock to enable other to access to the data
    participants_lock.release()  
    return n+1

def add_motivations(campaign_id,n,motivations):

    conn = st.connection("gsheets", type=GSheetsConnection)

    # Lock to ensure that the action assignment is made in a sequential way
    motivation_lock.acquire()

    #Transform the data stored in a google sheet to data structures compatible with the OPTIMAC algorithm
    # allocationDF = conn.read(ttl=0,usecols=[0, 1,2],worksheet="allocated_actions")
    # actionstatsDF = conn.read(ttl=0,usecols=[0, 1,2,3],worksheet="actions_stats")

    motivationsDF = conn.read(ttl=0,usecols=[0, 1,2],worksheet=f"motivations_{campaign_id}")

    # allocated_actions  = allocationDF.values.tolist()
    # list_actions = {line[0]:{'target':line[1], 'current':line[2],'minimum':line[3]} for line in actionstatsDF.values}
    i = 0
    motivationsDF_size = len(motivationsDF)
    for action in motivations:
        motivationsDF.loc[motivationsDF_size+i] = [n,action, motivations[action]]
        i+=1
    conn.update(worksheet=f"motivations_{campaign_id}",data = motivationsDF)
    st.cache_data.clear()

    #Unlock to enable other to access to the data
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
    feedback_lock.release()

def add_suggestion(n,suggestion):
    conn = st.connection("gsheets", type=GSheetsConnection)
    suggestion_lock.acquire()

    feedbackDF = conn.read(ttl=0,usecols=[0,1],worksheet="suggestions")
    feedbackDF_size = len(feedbackDF)
    feedbackDF.loc[feedbackDF_size ] = [n,suggestion]
    conn.update(worksheet=f"suggestions",data=feedbackDF)
    suggestion_lock.release()