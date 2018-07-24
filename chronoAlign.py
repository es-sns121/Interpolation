from datetime import datetime, timedelta

'''
chronoAlign : Takes a variable number of time value pair tuples and aligns them 
all on the same time.

Each time value pair should be a tuple (time, value)

The order of returned values is identical to the order of passed values. 
The first passed value will be the first returned value, etc.

Prototype:

    (earliest_time, value, value, ....) chronoAlign((time, value), (time, value), ...)


'''
def chronoAlign(*time_value_pairs):
    time_values = []
    first = 0
    for time_value_pair in time_value_pairs:

        time  = time_value_pair[0] # datetime
        value = time_value_pair[1] # float
    
        # Find earliest time to align on
        if first == 0:
            earliest = time
            first += 1

        # Collect all the values.
        time_values.append(value)
        
        # Determine the earliest time.
        if time < earliest:
            earliest = time
    
    time_values.insert(0, earliest)
    return tuple(time_values)


'''
# TEST
print chronoAlign( (datetime.now() - timedelta(seconds=20), 1.0),
                   (datetime.now() - timedelta(seconds=30), 2.0), 
                   (datetime.now() - timedelta(seconds=30), 3.0), 
                   (datetime.now() - timedelta(seconds=40), 4.0) )
'''
