import numpy as np 
import pandas as pd
from datetime import datetime
from datetime import time

def time_difference(user_input, scale, time_point, index_time = 1, ):
    h, m = map(int, user_input.split(':'))
    
    #input_time = time(hour=h, minute=m)

    #BrownBear = pd.read_csv('bear_path_prediction/BrownBear_data.csv')

    time_12hr = time_point

    dt_obj = datetime.strptime(time_12hr, "%I:%M %p")
    military_time = dt_obj.strftime("%H:%M")

    dt_input = datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M")
    dt_csv   = datetime.strptime(military_time, "%H:%M")

    difference =  ((dt_input - dt_csv).seconds)/60
    if difference < 0:
        difference += 24 
    
    if difference == 0:
        return 1
    else:
        return 1 / (difference / scale)

#print(time_difference("12:00"))
