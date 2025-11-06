import datetime
from random import seed
from random import randint,random
from random import gauss
import pandas as pd
#from sklearn.preprocessing import MinMaxScaler

class Participant:

    def __init__(self, participant_id, motivation_dict,measures=0):
        """
        args:
        -   participants: int
        -   action_list: string list (name of the actions)
        -   motivation_dict: (string:int) dict | (name of the action: participant's motivation to do said action)

        self.id :: int | participants id
        self.get_seed :: int -> int | provides a "random" seed for random generator
        self.motivations :: (string:int)dict | stores the motivations corresponding to the different options
        self.initial_measure :: int | stores the measures taken before the experiment
        """
        # Assign the provided participant ID to the object's 'id' attribute
        self.id = participant_id
       
        #list of mowing possibilities
        #mowing_frequencies = ['once_a_day', 'once_every_two_days', 'once_per_week', 'once_every_two_weeks','once_per_month', 'once_every_six_months', 'once_a_year', 'never']

        #new_frequence_dict
        self.motivations = {a:m for (a,m) in action_list.zip(motivations)}

        self.measures = measures
    


       
    def to_dict(self):
        return {
            'participant': self.id,
            'motivations': self.motivations,
            'measures' : self.measures
            #'geo_loc': self.geo_loc,
            #'garden_neighbourg': self.garden_neighbouring,
            #'self_eval': self.self_eval,
        }


class RandomParticipant(Participant):
    
    def __init__(self,participant_id, action_list,i_bias):
            
        # Set the seed for random number generation using a custom seed based on participant data
        self.id  = participant_id
        seed(self.get_seed(self.id))
        
        def motiv_function(mini,maxi,mu, sigma, camel = False): 
            if camel:
                if random()>0.5:
                    res = gauss(1.5,0.75)
                    res=round(res)
                else:
                    res = gauss(-1.5,0.75)
                    res=round(res)
                if res>maxi:
                    return maxi
                elif res < mini:
                    return mini
                else:
                    return res
                
            else:
                res = gauss(mu,sigma)
                res=round(res)
                if res>maxi:
                    return maxi
                elif res < mini:
                    return mini
                else:
                    return res

        if i_bias==-1 or random()<0.5:
            i_bias = randint(0,len(action_list)-1)
        biased_action = action_list[i_bias]
        self.motivations = {a:motiv_function(-3,3,0,1) for a in action_list if a != biased_action}
        self.motivations[biased_action] = motiv_function(-3,3,1.5,1)

        
        
        self.measures = 0
        #biased motivations:

        
    # Create a seed based on time.
    def get_seed(self, cls): 
        time = datetime.datetime.now()
        time_split = f'{time}'.split(':')
        time_split = time_split[2].split('.')
        time_split = time_split[0]+time_split[1]
        time_split = int(time_split)+int(cls)
        return time_split