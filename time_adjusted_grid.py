import numpy as np 
import pandas as pd
from datetime import datetime
from datetime import time

def time_difference(user_input, time_point, index_time=1):
    """
    Calculate a time-based weight based on the difference between user-specified time and data time.
    Returns higher weights for times closer to the user input time.

    Args:
        user_input (str): User-specified time in "HH:MM" format
        time_point (str): Data time point in "H:MM AM/PM" format
        index_time (int): Additional time index for weighting

    Returns:
        float: Time-based weight (higher for closer times)
    """
    # Parse user input time
    h, m = map(int, user_input.split(':'))
    
    # Parse data time point (12-hour format with AM/PM)
    time_12hr = time_point
    dt_obj = datetime.strptime(time_12hr, "%I:%M %p")
    military_time = dt_obj.strftime("%H:%M")

    # Convert to datetime objects for comparison
    dt_input = datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M")
    dt_csv = datetime.strptime(military_time, "%H:%M")

    # Calculate time difference in minutes
    difference = int(((dt_input - dt_csv).seconds) / 60) + index_time
    if difference < 0:
        difference += 24  # Handle wrap-around for times crossing midnight
    
    # Return weight: 1 for exact match, otherwise 1/difference^3
    if difference == 0:
        return 1
    else:
        weight = 1 / (difference ** 3)
        # Debug print for very high weights
        if weight > 1:
            print(weight)
        return weight

# Example usage (commented out)
# print(time_difference("12:00"))
