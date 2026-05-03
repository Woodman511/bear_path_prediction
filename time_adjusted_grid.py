import numpy as np 
import pandas as pd
from datetime import datetime
from datetime import time

def time_difference(user_input, scale, index_time = 1, index_row = 1):
    h, m = map(int, user_input.split(':'))
    input_time = time(hour=h, minute=m)

    BlackBear2012 = pd.read_csv('bear_path_prediction/BlackBear2012_data.csv')

    time_12hr = str(BlackBear2012.iat[index_row, 4])

    dt_obj = datetime.strptime(time_12hr, "%I:%M %p")
    military_time = dt_obj.strftime("%H:%M")

    dt_input = datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M")
    dt_csv   = datetime.strptime(military_time, "%H:%M")

    difference =  ((dt_input - dt_csv).seconds)/60 + index_time(10)
    if difference < 0:
        difference += 24 
    
    if difference == 0:
        return 1
    else:
        return 1 / (difference / scale)

print(time_difference("12:00"))
