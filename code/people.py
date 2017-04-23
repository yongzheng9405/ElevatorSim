import numpy as np  
import random
from numpy import random as rm 
import matplotlib.pyplot as plt  

def generate_arriving(num_people, top_floor):

    people_arriving_time_dict = {}
    people_arriving_time = []
    rm.seed = 666
    # people will arrive between 0-2700 interation (say 3 hours 8:00-11:00 in morning), obey poisson (exponential) distirbution
    for i in range(num_people):
        people_arriving_time.append(int(rm.exponential(500,1)))

    for people in people_arriving_time:

        # conver outlier to 2700
        if people > 2700:
            people = 2700
    
    	if people not in people_arriving_time_dict:
        	people_arriving_time_dict[people] = 1
    	else:
        	people_arriving_time_dict[people] += 1

    arriving_time_list = people_arriving_time_dict.keys()

    arriving_time = []
    customer_floor = []
    arriving_time_list.sort()

    for time in arriving_time_list:
      arriving_time.append(time)
    
      aim_floor = []
    
      for i in range(people_arriving_time_dict[time]):
        aim_floor.append(rm.randint(2, top_floor))
        
      customer_floor.append(aim_floor)

    return arriving_time, customer_floor

def generate_normal(num_people, top_floor):

    random.seed(666)

    people_leaving_time = []
    people_back_time = []
    people_floor = []

    # normal leaving time is between [2700, 6300]
    # the leaving time range is [900,1800], say 1-2 hours

    leaving_time_list = random.sample(range(2700,6300),num_people)

    # record leaving time
    for time in leaving_time_list:
        people_leaving_time.append(time)

    people_leaving_time.sort()

    # record back time
    for time in people_leaving_time:
        people_back_time.append(time + random.randint(900,1800))


    # record floor
    for i in range(num_people):
        random.seed(i)
        temp_floor = [random.randint(2,top_floor)]
        people_floor.append(temp_floor)

    return people_back_time, people_floor, people_leaving_time, people_floor

def generate_leaving(num_people, top_floor):

    random.seed(666)

    people_leaving_time = []
    people_floor = []

    # normal leaving time is between [8100, 10800], say 3 hours 17:00 - 20:00 in the afternoon
    leaving_time_list = random.sample(range(8100,10800), num_people)

    # record leaving time
    for time in leaving_time_list:
        people_leaving_time.append(time)

    people_leaving_time.sort()

    # record floor
    for i in range(num_people):
        random.seed(i*i)
        temp_floor = [random.randint(2,top_floor)]
        people_floor.append(temp_floor)

    return people_leaving_time, people_floor

# Define the function to combine the action in a day
def generate_day(num_people, top_floor):

    arriving_time = []
    customer_floor = []
    calling_time = []
    customer_current_floor = []

    arriving_time_1, customer_floor_1 = generate_arriving(num_people, top_floor)
    arriving_time_2, customer_floor_2, calling_time_1, customer_current_floor_1 = generate_normal(num_people, top_floor)
    calling_time_2, customer_current_floor_2 = generate_leaving(num_people, top_floor)

    arriving_time.extend(arriving_time_1)
    arriving_time.extend(arriving_time_2)

    customer_floor.extend(customer_floor_1)
    customer_floor.extend(customer_floor_2)

    calling_time.extend(calling_time_1)
    calling_time.extend(calling_time_2)

    customer_current_floor.extend(customer_current_floor_1)
    customer_current_floor.extend(customer_current_floor_2)

    return arriving_time, customer_floor, calling_time, customer_current_floor

def split_day(arriving_time, customer_floor, calling_time, customer_current_floor, ratio):

    random.seed(666)
    sub_size_1 = int(len(arriving_time) * (ratio))
    sub_size_2 = int(len(calling_time) * (ratio))

    index_1 = random.sample(range(len(arriving_time)), sub_size_1)
    index_2 = random.sample(range(len(calling_time)), sub_size_2)

    index_1.sort()
    index_2.sort()

    arriving_time_1 = []
    customer_floor_1 = []
    calling_time_1 = []
    customer_current_floor_1 = []

    arriving_time_2 = []
    customer_floor_2 = []
    calling_time_2 = []
    customer_current_floor_2 = []

    for i in range(len(arriving_time)):
        if i in index_1:
            arriving_time_1.append(arriving_time[i])
            customer_floor_1.append(customer_floor[i])
        else:
            arriving_time_2.append(arriving_time[i])
            customer_floor_2.append(customer_floor[i])

    for i in range(len(calling_time)):
        if i in index_2:
            calling_time_1.append(calling_time[i])
            customer_current_floor_1.append(customer_current_floor[i])
        else:
            calling_time_2.append(calling_time[i])
            customer_current_floor_2.append(customer_current_floor[i])

    return arriving_time_1, customer_floor_1, calling_time_1, customer_current_floor_1, arriving_time_2, customer_floor_2, calling_time_2, customer_current_floor_2
