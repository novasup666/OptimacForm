from Optimac import allocate_action_to_participant,update_action_proportions
import pandas as pan
import portalocker
from participant_real import Participant

allocated_actions_file_name = "../data/allocated_actions.csv"
action_stats_file_name = "../data/action_stats.csv"
'''
This is used to create forms etc

data.csv stores the allocated actions with following columns: n, action_label, motivation (of the participant for said action)
'''

def add_participant(motivations):

    with open(allocated_actions_file_name, "r+") as f :
        portalocker.lock(f, portalocker.LOCK_EX)  # Lock to protect data.csv and ensure the right order of the action assignment
        with open(action_stats_file_name,"r+") as g: 
            portalocker.lock(g, portalocker.LOCK_EX)  # Lock to protect data.csv and ensure the right order of the action assignment
            
            
            #transform the csv files to compatible format for the algorithm
            allocationDF = pan.read_csv(allocated_actions_file_name)
            allocated_actions  = allocationDF.values.tolist()

            actionstatsDF = pan.read_csv(action_stats_file_name)
            list_actions = {line[0]:{'target':line[1], 'current':line[2],'minimum':line[3]} for line in actionstatsDF.values}

            n = len(allocationDF)

            new_participant = Participant(n,motivations)
            allocate_action_to_participant(new_participant.to_dict(),n,list_actions, allocated_actions)
            allocated_action = allocated_actions[-1]
            allocationDF.loc[n] = allocated_action

            #update_action_proportions(n,list_actions,allocated_action[1])

            for i in range(len(actionstatsDF)):
                print(list_actions[ actionstatsDF.loc[i,"action_name"]]["current"])
                actionstatsDF.loc[i,"current_proportion"] = list_actions[ actionstatsDF.loc[i,"action_name"]]["current"]

            actionstatsDF.to_csv(action_stats_file_name,index=False)
            allocationDF.to_csv(allocated_actions_file_name, index= False)

            return allocated_action[1]
            portalocker.unlock(g)  # Lock to protect data.csv and ensure the right order of the action assignment

        portalocker.unlock(f)  # Libère le verrou (optionnel, libéré à la fermeture)

