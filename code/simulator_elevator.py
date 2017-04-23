from building import *
from elevator import *
from optimize import *
from people import *


# Define the funciton to simulate 1 elevators
def simulator_elevator_1(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, total_customer):
    
    in_queue = []
    out_queue = []
    aim_floor_queue_1 = [] 
    leave_count_1 = {}
    aim_floor_number_1 = {}

    count_coming = 0
    count_calling = 0
    count_move_1 = 0
    count_move_1_empty = 0
    total_customer = total_customer * 4
    total_waiting_time = 0

    # start simulation
    for i in range(simulation_time):

        # Record the process
        #if i >= 0 and i < 300:
            #print "Time - " + str(i) + " " + e1.name + " : "+ str(e1.current_floor) + " floor " + str(e1.num_customer) + " customer " 
        
        # consider the elevator state in the first floor, only in_queue people could enter by the order of arriving time
        if e1.current_floor == 1:
            e1.direction = "stay"
            
            if len(aim_floor_queue_1) > 0:
                e1.direction = "up"
                aim_floor_queue_1.sort(reverse = True) # Re-order the aim_floor

            in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1, e1.direction = queue_first_floor(in_queue, aim_floor_queue_1, 15, e1.name)
        
        # get the queue of people coming, build "in_queue"
        try:
            if i == arriving_time[count_coming]:
            
                in_queue.extend(customer_floor[count_coming])
                count_coming = count_coming + 1
                #print "!!!" + " one customer group is coming"
                
                # consider which elevator is in the initial state, if both, e1 first
                if e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                    e1.direction = "up"
                    in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1 = queue_initial_state(in_queue, 15, e1.name)         
                else:
                    pass
        except:
            pass
        
        # get the queue of people leaving, build "out_queue"
        try:
            if i == calling_time[count_calling]:
                
                out_queue.extend(customer_current_floor[count_calling])
                floor_customer_numer = len(customer_current_floor[count_calling])
                floor_value = out_queue[-1]
                
                # call e1 to pick
                aim_floor_queue_1, leave_count_1, e1.direction = optimize_down(e1.direction, floor_value, e1.current_floor, aim_floor_queue_1, floor_customer_numer, leave_count_1, e1.num_customer)
                count_calling = count_calling + 1
                #print "!!!" + " one customer group is calling"     
        except:
            pass
         
        # manage the e1, when it hits the aim_floor   
        if len(aim_floor_queue_1) > 0:
            
            aim_floor_number_1, leave_count_1, aim_floor_queue_1, e1.direction, e1.num_customer, out_queue = manage_aim_floor(e1.direction, e1.current_floor, aim_floor_queue_1, leave_count_1, e1.num_customer, e1.capaticy, e1.name, aim_floor_number_1, out_queue) 
                                                                                            
        else:
            if e1.current_floor == 1:
                e1.direction = "stay"
            else:
                e1.direction = "down"
        
        # record the total move and empty move of the elevator
        if e1.direction != "stay":
            count_move_1 += 1
            if e1.num_customer == 0:
                count_move_1_empty += 1

        # record the waiting time
        if len(in_queue) > 0:
            total_waiting_time += len(in_queue)

        if len(out_queue) > 0:
            total_waiting_time += len(out_queue)

        e1.move()

    total_move = count_move_1
    total_empty_move = count_move_1_empty
    avg_waiting_time = round(total_waiting_time/float(total_customer),2)

    return total_move, total_empty_move, avg_waiting_time

# Define the funciton to simulate 2 elevators
def simulator_elevator_2(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, e2, total_customer):
    
    in_queue = []
    out_queue = []

    aim_floor_queue_1 = [] 
    aim_floor_queue_2 = []

    queue_calling = []
    in_queue = []

    count_coming = 0
    count_calling = 0

    aim_floor_number_1 = {}
    aim_floor_number_2 = {}

    leave_count_1 = {}
    leave_count_2 = {}

    count_move_1 = 0
    count_move_2 = 0

    count_move_1_empty = 0
    count_move_2_empty = 0

    total_customer = total_customer * 4
    total_waiting_time = 0

    # start simulation
    for i in range(simulation_time):
        
        #if i > 0 and i < 500:
            #print "Time - " + str(i) + " " + e1.name + " : "+ str(e1.current_floor) + " floor " + str(e1.num_customer) + " customer "
            #print "Time - " + str(i) + " " + e2.name + " : "+ str(e2.current_floor) + " floor " + str(e2.num_customer) + " customer "
        #print "At time " + str(i) + " " + e1.name + " is in " + str(e1.current_floor) + " floor"
        #print "At time " + str(i) + " " + e2.name + " is in " + str(e2.current_floor) + " floor"
        
        # consider the elevator state in the first floor, only in_queue people could enter by the order of timestamp
        if e1.current_floor == 1:
            e1.direction = "stay"
            
            if len(aim_floor_queue_1) > 0:
                e1.direction = "up"
                aim_floor_queue_1.sort(reverse = True) 
            
            in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1, e1.direction = queue_first_floor(in_queue, aim_floor_queue_1, 15, e1.name)
        
        if e2.current_floor == 1:
            e2.direction = "stay"
            
            if len(aim_floor_queue_2) > 0:
                e2.direction = "up"
                aim_floor_queue_2.sort(reverse = True) 
            
            in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2, e2.direction = queue_first_floor(in_queue, aim_floor_queue_2, 15, e2.name)
        
        # get the queue of people coming, build "in_queue"
        try:
            if i == arriving_time[count_coming]:
            
                in_queue.extend(customer_floor[count_coming])
                count_coming = count_coming + 1
                #print "!!!" + " one customer group is coming"
                
                # consider which elevator is in the initial state, if both, e1 first
                if e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                    e1.direction = "up"
                    in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1 = queue_initial_state(in_queue, 15, e1.name)
                    
                    # for the extra people use e2
                    if len(in_queue) > 0 and e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                        e2.direction = "up"
                        in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2 = queue_initial_state(in_queue, 15, e2.name)

                # if e1 is not ok, than comes to e2
                elif e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                    e2.direction = "up"
                    in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2 = queue_initial_state(in_queue, 15, e2.name)
                
                else:
                    pass
        except:
            pass
        
        # get the queue of people leaving, build "out_queue"
        try:
            if i == calling_time[count_calling]:
                
                out_queue.extend(customer_current_floor[count_calling])
                floor_customer_numer = len(customer_current_floor[count_calling])
                floor_value = out_queue[-1]
                
                # decide which elevator to pick the people calling
                if e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                    aim_floor_queue_1, leave_count_1, e1.direction = optimize_down(e1.direction, floor_value, e1.current_floor, aim_floor_queue_1, floor_customer_numer, leave_count_1, e1.num_customer)
                elif e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                    aim_floor_queue_2, leave_count_2, e2.direction = optimize_down(e2.direction, floor_value, e2.current_floor, aim_floor_queue_2, floor_customer_numer, leave_count_2, e2.num_customer)
                
                # if botn are busy, than the one neay the people's calling floor is assigned to pick
                elif abs(e1.current_floor - floor_value) <= abs(e2.current_floor - floor_value):
                    aim_floor_queue_1, leave_count_1, e1.direction = optimize_down(e1.direction, floor_value, e1.current_floor, aim_floor_queue_1, floor_customer_numer, leave_count_1, e1.num_customer)  
                else:
                    aim_floor_queue_2, leave_count_2, e2.direction = optimize_down(e2.direction, floor_value, e2.current_floor, aim_floor_queue_2, floor_customer_numer, leave_count_2, e2.num_customer)
                  
                count_calling = count_calling + 1
                #print "!!!" + " one customer group is calling"     
        except:
            pass
         
        # manage the e1, when it hits the aim_floor   
        if len(aim_floor_queue_1) > 0:
            
            aim_floor_number_1, leave_count_1, aim_floor_queue_1, e1.direction, e1.num_customer, out_queue = manage_aim_floor(e1.direction, e1.current_floor, aim_floor_queue_1, leave_count_1, e1.num_customer, e1.capaticy, e1.name, aim_floor_number_1, out_queue) 
                                                                                            
        else:
            if e1.current_floor == 1:
                e1.direction = "stay"
            else:
                e1.direction = "down"
        
        # manage the e2, when ti hits the aim_floor
        if len(aim_floor_queue_2) > 0:
            
            aim_floor_number_2, leave_count_2, aim_floor_queue_2, e2.direction, e2.num_customer, out_queue = manage_aim_floor(e2.direction, e2.current_floor, aim_floor_queue_2, leave_count_2, e2.num_customer, e2.capaticy,e2.name, aim_floor_number_2, out_queue) 
                                                                                            
        else:
            if e2.current_floor == 1:
                e2.direction = "stay"
            else:
                e2.direction = "down"

        # record the total move of the elevator
        if e1.direction != "stay":
            count_move_1 += 1
            if e1.num_customer == 0:
                count_move_1_empty += 1

        if e2.direction != "stay":
            count_move_2 += 1
            if e2.num_customer == 0:
                count_move_2_empty += 1

        # record the waiting time
        if len(in_queue) > 0:
            total_waiting_time += len(in_queue)

        if len(out_queue) > 0:
            total_waiting_time += len(out_queue)
          
        e1.move()
        e2.move()

    total_move = count_move_1 + count_move_2 
    total_empty_move = count_move_1_empty + count_move_2_empty
    avg_waiting_time = round(total_waiting_time/float(total_customer),2)

    return total_move, total_empty_move, avg_waiting_time

def simulator_elevator_3_1(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, e2, e3, total_customer):
    arriving_time_1, customer_floor_1, calling_time_1, customer_current_floor_1, arriving_time_2, customer_floor_2, calling_time_2, customer_current_floor_2 = split_day(arriving_time, customer_floor, calling_time, customer_current_floor, 0.3)

    count_move_1, count_move_1_empty, total_waiting_time_1 = simulator_elevator_1(arriving_time_1, calling_time_1, customer_floor_1, customer_current_floor_1, simulation_time, e1, total_customer)
    count_move_2, count_move_3, count_move_2_empty, count_move_3_empty, total_waiting_time_2 = simulator_elevator_2(arriving_time_2, calling_time_2, customer_floor_2, customer_current_floor_2, simulation_time, e2, e3, total_customer)

    total_waiting_time = total_waiting_time_1 + total_waiting_time_2
    total_customer = total_customer * 4

    total_move = count_move_1 + count_move_2 + count_move_3
    total_empty_move = count_move_1_empty + count_move_2_empty + count_move_3_empty
    avg_waiting_time = round(total_waiting_time/float(total_customer),2)

    return total_move, total_empty_move, avg_waiting_time

def simulator_elevator_3_2(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, e2, e3, total_customer):
    
    in_queue = []
    out_queue = []

    aim_floor_queue_1 = [] 
    aim_floor_queue_2 = []
    aim_floor_queue_3 = []

    queue_calling = []
    in_queue = []

    count_coming = 0
    count_calling = 0

    leave_count_1 = {}
    leave_count_2 = {}
    leave_count_3 = {}

    aim_floor_number_1 = {}
    aim_floor_number_2 = {}
    aim_floor_number_3 = {}

    count_move_1 = 0
    count_move_2 = 0
    count_move_3 = 0

    count_move_1_empty = 0
    count_move_2_empty = 0
    count_move_3_empty = 0

    total_customer = total_customer * 4
    total_waiting_time = 0

    # start simulation
    for i in range(simulation_time):
        
        #if i >= 1000 and i < 3000:
            #print "Time - " + str(i) + " " + e1.name + " : " + str(e1.current_floor) + " floor " + str(e1.num_customer) + " customer " 
            #print "Time - " + str(i) + " " + e2.name + " : " + str(e2.current_floor) + " floor " + str(e2.num_customer) + " customer " 
            #print "Time - " + str(i) + " " + e3.name + " : " + str(e3.current_floor) + " floor " + str(e3.num_customer) + " customer " 
        #print "At time " + str(i) + " " + e1.name + " is in " + str(e1.current_floor) + " floor"
        #print "At time " + str(i) + " " + e2.name + " is in " + str(e2.current_floor) + " floor"
        
        # consider the elevator state in the first floor, only in_queue people could enter by the order of timestamp
        if e1.current_floor == 1:
            e1.direction = "stay"
            
            if len(aim_floor_queue_1) > 0:
                e1.direction = "up"
                aim_floor_queue_1.sort(reverse = True) 
            
            in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1, e1.direction = queue_first_floor(in_queue, aim_floor_queue_1, 15, e1.name)
        
        if e2.current_floor == 1:
            e2.direction = "stay"
            
            if len(aim_floor_queue_2) > 0:
                e2.direction = "up"
                aim_floor_queue_2.sort(reverse = True) 
            
            in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2, e2.direction = queue_first_floor(in_queue, aim_floor_queue_2, 15, e2.name)

        if e3.current_floor == 1:
            e3.direction = "stay"
            
            if len(aim_floor_queue_3) > 0:
                e2.direction = "up"
                aim_floor_queue_3.sort(reverse = True) 
            
            in_queue, aim_floor_queue_3, e3.num_customer, aim_floor_number_3, e3.direction = queue_first_floor(in_queue, aim_floor_queue_3, 15, e3.name)
        
        # get the queue of people coming, build "in_queue"
        try:
            if i == arriving_time[count_coming]:
            
                in_queue.extend(customer_floor[count_coming])
                count_coming = count_coming + 1
                #print "!!!" + " one customer group is coming"
                
                # consider which elevator is in the initial state, if both, e3 first
                if e3.current_floor == 1 and len(aim_floor_queue_3) == 0:
                    e3.direction = "up"
                    in_queue, aim_floor_queue_3, e3.num_customer, aim_floor_number_3 = queue_initial_state(in_queue, 15, e3.name)
                    
                    # for the extra people use e2
                    if len(in_queue) > 0 and e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                        e2.direction = "up"
                        in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2 = queue_initial_state(in_queue, 15, e2.name)

                        # for the extra people use e1
                        if len(in_queue) > 0 and e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                            e1.direction = "up"
                            in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1 = queue_initial_state(in_queue, 15, e1.name)

                # if e3 is not ok, than comes to e2
                elif e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                    e2.direction = "up"
                    in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2 = queue_initial_state(in_queue, 15, e2.name)

                #  if e2 is not ok, than comes to e1
                elif e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                    e1.direction = "up"
                    in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1 = queue_initial_state(in_queue, 15, e1.name)
                
                else:
                    pass
        except:
            pass
        
        # get the queue of people leaving, build "out_queue"
        try:
            if i == calling_time[count_calling]:
                
                out_queue.extend(customer_current_floor[count_calling])
                floor_customer_numer = len(customer_current_floor[count_calling])
                floor_value = out_queue[-1]
                
                # decide which elevator to pick the people calling
                if e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                    aim_floor_queue_1, leave_count_1, e1.direction = optimize_down(e1.direction, floor_value, e1.current_floor, aim_floor_queue_1, floor_customer_numer, leave_count_1, e1.num_customer)
                elif e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                    aim_floor_queue_2, leave_count_2, e2.direction = optimize_down(e2.direction, floor_value, e2.current_floor, aim_floor_queue_2, floor_customer_numer, leave_count_2, e2.num_customer)
                elif e3.current_floor == 1 and len(aim_floor_queue_3) == 0:
                    aim_floor_queue_3, leave_count_3, e3.direction = optimize_down(e3.direction, floor_value, e3.current_floor, aim_floor_queue_3, floor_customer_numer, leave_count_3, e3.num_customer)
                
                # if botn are busy, than the one near the people's calling floor is assigned to pick
                elif abs(e1.current_floor - floor_value) <= abs(e2.current_floor - floor_value) and abs(e1.current_floor - floor_value) <= abs(e3.current_floor - floor_value):
                    aim_floor_queue_1, leave_count_1, e1.direction = optimize_down(e1.direction, floor_value, e1.current_floor, aim_floor_queue_1, floor_customer_numer, leave_count_1, e1.num_customer)  
                elif abs(e2.current_floor - floor_value) <= abs(e3.current_floor - floor_value):
                    aim_floor_queue_2, leave_count_2, e2.direction = optimize_down(e2.direction, floor_value, e2.current_floor, aim_floor_queue_2, floor_customer_numer, leave_count_2, e2.num_customer)  
                else:
                    aim_floor_queue_3, leave_count_3, e3.direction = optimize_down(e3.direction, floor_value, e3.current_floor, aim_floor_queue_3, floor_customer_numer, leave_count_3, e3.num_customer)
                  
                count_calling = count_calling + 1
                #print "!!!" + " one customer group is calling"     
        except:
            pass
         
        # manage the e1, when it hits the aim_floor   
        if len(aim_floor_queue_1) > 0:
            
            aim_floor_number_1, leave_count_1, aim_floor_queue_1, e1.direction, e1.num_customer, out_queue = manage_aim_floor(e1.direction, e1.current_floor, aim_floor_queue_1, leave_count_1, e1.num_customer, e1.capaticy, e1.name, aim_floor_number_1, out_queue) 
                                                                                            
        else:
            if e1.current_floor == 1:
                e1.direction = "stay"
            else:
                e1.direction = "down"
        
        # manage the e2, when ti hits the aim_floor
        if len(aim_floor_queue_2) > 0:
            
            aim_floor_number_2, leave_count_2, aim_floor_queue_2, e2.direction, e2.num_customer, out_queue = manage_aim_floor(e2.direction, e2.current_floor, aim_floor_queue_2, leave_count_2, e2.num_customer, e2.capaticy, e2.name, aim_floor_number_2, out_queue) 
                                                                                            
        else:
            if e2.current_floor == 1:
                e2.direction = "stay"
            else:
                e2.direction = "down"

        # manage the e3, when it hits the aim_floor
        if len(aim_floor_queue_3) > 0:
            
            aim_floor_number_3, leave_count_3, aim_floor_queue_3, e3.direction, e3.num_customer, out_queue = manage_aim_floor(e3.direction, e3.current_floor, aim_floor_queue_3, leave_count_3, e3.num_customer, e3.capaticy, e3.name, aim_floor_number_3, out_queue) 
                                                                                            
        else:
            if e3.current_floor == 1:
                e3.direction = "stay"
            else:
                e3.direction = "down"

        # record the total move of the elevator
        if e1.direction != "stay":
            count_move_1 += 1
            if e1.num_customer == 0:
                count_move_1_empty += 1

        if e2.direction != "stay":
            count_move_2 += 1
            if e2.num_customer == 0:
                count_move_2_empty += 1

        if e3.direction != "stay":
            count_move_3 += 1
            if e3.num_customer == 0:
                count_move_3_empty += 1

        # record the waiting time
        if len(in_queue) > 0:
            total_waiting_time += len(in_queue)

        if len(out_queue) > 0:
            total_waiting_time += len(out_queue)

        #if i >= 1000 and i < 3000:
            #print aim_floor_queue_2
          
        e1.move()
        e2.move()
        e3.move()

    total_move = count_move_1 + count_move_2 + count_move_3
    total_empty_move = count_move_1_empty + count_move_2_empty + count_move_3_empty
    avg_waiting_time = round(total_waiting_time/float(total_customer),2)

    return total_move, total_empty_move, avg_waiting_time

def simulator_elevator_4_1(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, e2, e3, e4, total_customer):
    arriving_time_1, customer_floor_1, calling_time_1, customer_current_floor_1, arriving_time_2, customer_floor_2, calling_time_2, customer_current_floor_2 = split_day(arriving_time, customer_floor, calling_time, customer_current_floor, 0.5)

    count_move_1, count_move_2, count_move_1_empty, count_move_2_empty, total_waiting_time_1 = simulator_elevator_2(arriving_time_1, calling_time_1, customer_floor_1, customer_current_floor_1, simulation_time, e1, e2, total_customer)
    count_move_3, count_move_4, count_move_3_empty, count_move_4_empty, total_waiting_time_2 = simulator_elevator_2(arriving_time_2, calling_time_2, customer_floor_2, customer_current_floor_2, simulation_time, e3, e4, total_customer)

    total_waiting_time = total_waiting_time_1 + total_waiting_time_2
    total_customer = total_customer * 4

    total_move = count_move_1 + count_move_2 + count_move_3 + count_move_4
    total_empty_move = count_move_1_empty + count_move_2_empty + count_move_3_empty + count_move_4_empty
    avg_waiting_time = round(total_waiting_time/float(total_customer),2)

    return total_move, total_empty_move, avg_waiting_time

def simulator_elevator_4_2(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, e2, e3, e4, total_customer):
    
    in_queue = []
    out_queue = []

    aim_floor_queue_1 = [] 
    aim_floor_queue_2 = []
    aim_floor_queue_3 = []
    aim_floor_queue_4 = []

    queue_calling = []
    in_queue = []

    count_coming = 0
    count_calling = 0

    leave_count_1 = {}
    leave_count_2 = {}
    leave_count_3 = {}
    leave_count_4 = {}

    aim_floor_number_1 = {}
    aim_floor_number_2 = {}
    aim_floor_number_3 = {}
    aim_floor_number_4 = {}

    count_move_1 = 0
    count_move_2 = 0
    count_move_3 = 0
    count_move_4 = 0

    count_move_1_empty = 0
    count_move_2_empty = 0
    count_move_3_empty = 0
    count_move_4_empty = 0

    total_customer = total_customer * 4
    total_waiting_time = 0

    # start simulation
    for i in range(simulation_time):
            
        # consider the elevator state in the first floor, only in_queue people could enter by the order of timestamp
        if e1.current_floor == 1:
            e1.direction = "stay"
            
            if len(aim_floor_queue_1) > 0:
                e1.direction = "up"
                aim_floor_queue_1.sort(reverse = True) 
            
            in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1, e1.direction = queue_first_floor(in_queue, aim_floor_queue_1, 15, e1.name)
        
        if e2.current_floor == 1:
            e2.direction = "stay"
            
            if len(aim_floor_queue_2) > 0:
                e2.direction = "up"
                aim_floor_queue_2.sort(reverse = True) 
            
            in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2, e2.direction = queue_first_floor(in_queue, aim_floor_queue_2, 15, e2.name)

        if e3.current_floor == 1:
            e3.direction = "stay"
            
            if len(aim_floor_queue_3) > 0:
                e2.direction = "up"
                aim_floor_queue_3.sort(reverse = True) 
            
            in_queue, aim_floor_queue_3, e3.num_customer, aim_floor_number_3, e3.direction = queue_first_floor(in_queue, aim_floor_queue_3, 15, e3.name)

        if e4.current_floor == 1:
            e4.direction = "stay"
            
            if len(aim_floor_queue_4) > 0:
                e4.direction = "up"
                aim_floor_queue_4.sort(reverse = True) 
            
            in_queue, aim_floor_queue_4, e4.num_customer, aim_floor_number_4, e4.direction = queue_first_floor(in_queue, aim_floor_queue_4, 15, e4.name)
        
        # get the queue of people coming, build "in_queue"
        try:
            if i == arriving_time[count_coming]:
            
                in_queue.extend(customer_floor[count_coming])
                count_coming = count_coming + 1
                #print "!!!" + " one customer group is coming"
                
                # consider which elevator is in the initial state, if both, e3 first
                if e3.current_floor == 1 and len(aim_floor_queue_3) == 0:
                    e3.direction = "up"
                    in_queue, aim_floor_queue_3, e3.num_customer, aim_floor_number_3 = queue_initial_state(in_queue, 15, e3.name)
                    
                    # for the extra people use e2
                    if len(in_queue) > 0 and e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                        e2.direction = "up"
                        in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2 = queue_initial_state(in_queue, 15, e2.name)

                        # for the extra people use e1
                        if len(in_queue) > 0 and e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                            e1.direction = "up"
                            in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1 = queue_initial_state(in_queue, 15, e1.name)

                            # for the extra people use e4
                            if len(in_queue) > 0 and e4.current_floor == 1 and len(aim_floor_queue_4) == 0:
                                e4.direction = "up"
                                in_queue, aim_floor_queue_4, e4.num_customer, aim_floor_number_4 = queue_initial_state(in_queue, 15, e4.name)


                # if e3 is not ok, than comes to e2
                elif e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                    e2.direction = "up"
                    in_queue, aim_floor_queue_2, e2.num_customer, aim_floor_number_2 = queue_initial_state(in_queue, 15, e2.name)

                #  if e2 is not ok, than comes to e1
                elif e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                    e1.direction = "up"
                    in_queue, aim_floor_queue_1, e1.num_customer, aim_floor_number_1 = queue_initial_state(in_queue, 15, e1.name)

                #  if e1 is not ok, than comes to e4
                elif e4.current_floor == 1 and len(aim_floor_queue_4) == 0:
                    e4.direction = "up"
                    in_queue, aim_floor_queue_4, e4.num_customer, aim_floor_number_4 = queue_initial_state(in_queue, 15, e4.name)
                
                else:
                    pass
        except:
            pass
        
        # get the queue of people leaving, build "out_queue"
        try:
            if i == calling_time[count_calling]:
                
                out_queue.extend(customer_current_floor[count_calling])
                floor_customer_numer = len(customer_current_floor[count_calling])
                floor_value = out_queue[-1]
                
                # decide which elevator to pick the people calling
                if e1.current_floor == 1 and len(aim_floor_queue_1) == 0:
                    aim_floor_queue_1, leave_count_1, e1.direction = optimize_down(e1.direction, floor_value, e1.current_floor, aim_floor_queue_1, floor_customer_numer, leave_count_1, e1.num_customer)
                elif e2.current_floor == 1 and len(aim_floor_queue_2) == 0:
                    aim_floor_queue_2, leave_count_2, e2.direction = optimize_down(e2.direction, floor_value, e2.current_floor, aim_floor_queue_2, floor_customer_numer, leave_count_2, e2.num_customer)
                elif e3.current_floor == 1 and len(aim_floor_queue_3) == 0:
                    aim_floor_queue_3, leave_count_3, e3.direction = optimize_down(e3.direction, floor_value, e3.current_floor, aim_floor_queue_3, floor_customer_numer, leave_count_3, e3.num_customer)
                elif e4.current_floor == 1 and len(aim_floor_queue_4) == 0:
                    aim_floor_queue_4, leave_count_4, e4.direction = optimize_down(e4.direction, floor_value, e4.current_floor, aim_floor_queue_4, floor_customer_numer, leave_count_4, e4.num_customer)

                # if botn are busy, than the one near the people's calling floor is assigned to pick
                elif abs(e1.current_floor - floor_value) <= abs(e2.current_floor - floor_value) and abs(e1.current_floor - floor_value) <= abs(e3.current_floor - floor_value) and abs(e1.current_floor - floor_value) <= abs(e4.current_floor - floor_value):
                    aim_floor_queue_1, leave_count_1, e1.direction = optimize_down(e1.direction, floor_value, e1.current_floor, aim_floor_queue_1, floor_customer_numer, leave_count_1, e1.num_customer)  
                elif abs(e2.current_floor - floor_value) <= abs(e3.current_floor - floor_value) and abs(e2.current_floor - floor_value) <= abs(e4.current_floor - floor_value):
                    aim_floor_queue_2, leave_count_2, e2.direction = optimize_down(e2.direction, floor_value, e2.current_floor, aim_floor_queue_2, floor_customer_numer, leave_count_2, e2.num_customer)  
                elif abs(e4.current_floor - floor_value) <= abs(e3.current_floor - floor_value) and abs(e4.current_floor - floor_value) <= abs(e3.current_floor - floor_value):
                    aim_floor_queue_4, leave_count_4, e4.direction = optimize_down(e4.direction, floor_value, e4.current_floor, aim_floor_queue_4, floor_customer_numer, leave_count_4, e4.num_customer) 
                else:
                    aim_floor_queue_3, leave_count_3, e3.direction = optimize_down(e3.direction, floor_value, e3.current_floor, aim_floor_queue_3, floor_customer_numer, leave_count_3, e3.num_customer)
                  
                count_calling = count_calling + 1
                #print "!!!" + " one customer group is calling"     
        except:
            pass
         
        # manage the e1, when it hits the aim_floor   
        if len(aim_floor_queue_1) > 0:
            
            aim_floor_number_1, leave_count_1, aim_floor_queue_1, e1.direction, e1.num_customer, out_queue = manage_aim_floor(e1.direction, e1.current_floor, aim_floor_queue_1, leave_count_1, e1.num_customer, e1.capaticy, e1.name, aim_floor_number_1, out_queue) 
                                                                                            
        else:
            if e1.current_floor == 1:
                e1.direction = "stay"
            else:
                e1.direction = "down"
        
        # manage the e2, when ti hits the aim_floor
        if len(aim_floor_queue_2) > 0:
            
            aim_floor_number_2, leave_count_2, aim_floor_queue_2, e2.direction, e2.num_customer, out_queue = manage_aim_floor(e2.direction, e2.current_floor, aim_floor_queue_2, leave_count_2, e2.num_customer, e2.capaticy, e2.name, aim_floor_number_2, out_queue) 
                                                                                            
        else:
            if e2.current_floor == 1:
                e2.direction = "stay"
            else:
                e2.direction = "down"

        # manage the e3, when it hits the aim_floor
        if len(aim_floor_queue_3) > 0:
            
            aim_floor_number_3, leave_count_3, aim_floor_queue_3, e3.direction, e3.num_customer, out_queue = manage_aim_floor(e3.direction, e3.current_floor, aim_floor_queue_3, leave_count_3, e3.num_customer, e3.capaticy, e3.name, aim_floor_number_3, out_queue) 
                                                                                            
        else:
            if e3.current_floor == 1:
                e3.direction = "stay"
            else:
                e3.direction = "down"

        # manage the e4, when it hits the aim_floor
        if len(aim_floor_queue_4) > 0:
            
            aim_floor_number_4, leave_count_4, aim_floor_queue_4, e4.direction, e4.num_customer, out_queue = manage_aim_floor(e4.direction, e4.current_floor, aim_floor_queue_4, leave_count_4, e4.num_customer, e4.capaticy, e4.name, aim_floor_number_4, out_queue) 
                                                                                            
        else:
            if e4.current_floor == 1:
                e4.direction = "stay"
            else:
                e4.direction = "down"

        # record the total move of the elevator
        if e1.direction != "stay":
            count_move_1 += 1
            if e1.num_customer == 0:
                count_move_1_empty += 1

        if e2.direction != "stay":
            count_move_2 += 1
            if e2.num_customer == 0:
                count_move_2_empty += 1

        if e3.direction != "stay":
            count_move_3 += 1
            if e3.num_customer == 0:
                count_move_3_empty += 1

        if e4.direction != "stay":
            count_move_4 += 1
            if e4.num_customer == 0:
                count_move_4_empty += 1

        # record the waiting time
        if len(in_queue) > 0:
            total_waiting_time += len(in_queue)

        if len(out_queue) > 0:
            total_waiting_time += len(out_queue)

        #if i >= 1000 and i < 3000:
            #print aim_floor_queue_2
          
        e1.move()
        e2.move()
        e3.move()
        e4.move()

    total_move = count_move_1 + count_move_2 + count_move_3 + count_move_4
    total_empty_move = count_move_1_empty + count_move_2_empty + count_move_3_empty + count_move_4_empty
    avg_waiting_time = round(total_waiting_time/float(total_customer),2)

    return total_move, total_empty_move, avg_waiting_time

