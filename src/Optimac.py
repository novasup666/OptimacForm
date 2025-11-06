


def get_ordered_actions(motivations,list_actions):
    """
    Return actions orderded by their preferences.
    """
    #return {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}
    sorting_key = lambda item: (item[1],list_actions[item[0]]["target"]-list_actions[item[0]]["current"])
    return sorted(motivations.items(),key=sorting_key, reverse=True)

def assign_action(n, motivations, list_actions, participants_allocated_actions):
    """
    Tries to assign the best action to the current participant.
    Falls back to the first action if none match allocation rules.

    Returns : True if "the best action has been assigned"

    Side-effect:   If it works :
                    - updates action proportions
                    - appends (n,label,value) to participants_allocated_actions
    """
    ordered_actions = get_ordered_actions(motivations,list_actions)


    for label, value in ordered_actions:

        action = list_actions[label]
        if (n/(n+1))*action['current'] < action['target'] or (n * action['current'] < action['minimum']):
                #if (n/(n+1))*action['current'] < action['target_proportion']:
            update_action_proportions(n, list_actions, label)
            participants_allocated_actions.append((n, label, value))
            return True
    return False


# def force_assign_action(n, ordered_actions, list_actions, participants_allocated_actions):
#     """
#     Forces assignment of the first available action in the ordered list.
#     Used when no action meets normal allocation criteria.
#     """
#     print(coucou)
#     label, value = next(iter(ordered_actions.items()))
#     for action in list_actions:
#         if action['action'] == label:
#             update_action_proportions(n, action, list_actions, label)
#             participants_allocated_actions.append((n, label, value))
#             break


def update_action_proportions(n, list_actions, assigned_label):
    """
    Updates the 'current' proportions of all actions after assignment.
    """
    assigned_action = list_actions[assigned_label]
    assigned_action['current'] = (assigned_action['current'] * n + 1) / (n + 1)
    for other in list_actions:
        if other != assigned_label:
            list_actions[other]['current'] = (list_actions[other]['current'] * n) / (n + 1)


def allocate_actions_to_participants(part_df, list_actions):
    """
    Main function to iterate over participants and assign actions.
    Returns the list of allocated actions.
    args:
    -   partdf :: dict panda dataframe | dataframe of Participants objects (in their dict representation)
    -   list_actions :: dict dict | list of actions 
    (represented by a dict {action (:str) :{target (:float), current(:float), minimum (:int) }})
    
    returns : 

    -   participants_allocated_actions :: (int, str, float) list | (value of n, label of the action, motivation of the participant for this action) list


    """
    n = 0
    participants_allocated_actions = []
    #print(part_df)
    for i in range(len(part_df)):
        n = allocate_action_to_participant(part_df.iloc[i], n, list_actions, participants_allocated_actions)
    return participants_allocated_actions

def allocate_action_to_participant(participant, n, list_actions, participants_allocated_actions):
    """
    args:
    -   participant :: dict | object from Participant class in its dict representation
    -   n :: int | counter
    -   list_actions :: dict list | dict of actions : {action_name : {target_proportion: float, current: float, minimum : int}}
    -   participants_allocated_actions :: (int, str, float) list | (value of n, label of the action, motivation of the participant for this action) list

    returns:
    -   n :: int
    
    side-effects:
    -   fills participants_allocated_actions up
    """
    
    motivations = participant["motivations"]
    assigned = assign_action(n, motivations, list_actions, participants_allocated_actions)
    # if not assigned:
    #     force_assign_action(n, ordered_actions, list_actions, participants_allocated_actions)
    n = n + 1
    return n

