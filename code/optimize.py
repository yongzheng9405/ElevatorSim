# Define the function to re-set the queue (Record the aim_floor value and number in aim_floor )
def reset_queue(queue_origin):
    
    temp = {}
    
    for i in range(len(queue_origin)):
        
        if queue_origin[i] in temp:
            temp[queue_origin[i]] += 1
        else:
            temp[queue_origin[i]] = 1
    
    queue_new = temp.keys()
    queue_new.sort()
        
    return queue_new,temp

# Define the function to decide the elevator state when the people first coming
def queue_initial_state(queue, capaticy, name):
    
    aim_floor_number = {}
    num_customer = 0
    
    if len(queue) <= capaticy:
        aim_floor_queue, aim_floor_number = reset_queue(queue[:])
        num_customer = len(queue)
        #print "!!!" + " There are " + str(num_customer) + " customer in the " + name 
        queue = []
    else:
        aim_floor_queue, aim_floor_number = reset_queue(queue[:capaticy])
        num_customer = capaticy
        #print "!!!" + " There are " + str(num_customer) + " customer in the " + name
        queue = queue[capaticy:]
    
    return queue, aim_floor_queue, num_customer, aim_floor_number

# Define the function to decide the elevator state in the first floor
def queue_first_floor(queue, aim_floor_queue, capacity, name):
    
    num_customer = 0
    aim_floor_number = {}

    if len(queue) <= capacity and len(queue) > 0:
        num_customer = len(queue)
        aim_floor_queue_temp, aim_floor_number = reset_queue(queue[:])
        aim_floor_queue.sort(reverse = True)
        aim_floor_queue_temp.extend(aim_floor_queue)
        aim_floor_queue = aim_floor_queue_temp
        #print "!!!" + " There are " + str(num_customer) + " customer in the " + name
        queue = []  
        direction = "up"
        
    elif len(queue) > capacity:
        num_customer = capacity
        aim_floor_queue_temp, aim_floor_number = reset_queue(queue[:capacity])
        aim_floor_queue.sort(reverse = True)
        aim_floor_queue_temp.extend(aim_floor_queue)
        aim_floor_queue = aim_floor_queue_temp
        #print "!!!" + " There are " + str(num_customer) + " customer in the " + name
        queue = queue[capacity:]
        direction = "up"
    elif len(queue) == 0 and len(aim_floor_queue) > 0:
        direction = "up" 
    else:
        direction = "stay"
    
    return queue, aim_floor_queue, num_customer, aim_floor_number, direction 

# Optimize the elevator state.
# when elevator is "down", it could carry the people wanting "down" 
# if the people's floor is lower than elevator's current floor
def optimize_down(direction, floor_call, elevator_current_floor, aim_floor_queue, num_customer, leave_count, num_in_el):

    # in the initial state, start to pick people
    if direction == "stay" and len(aim_floor_queue) == 0:
        aim_floor_queue.append(floor_call)
        leave_count[floor_call] = num_customer
        direction = "up"

    # carry the one who comes but in a lower floor
    elif direction == "down" and floor_call < elevator_current_floor:
        
        # if someone was waiting, add to the floor queue
        try:
           leave_count[floor_call] = num_customer + leave_count[floor_call]
        except:
           aim_floor_queue.append(floor_call)
           aim_floor_queue.sort(reverse = True)
           leave_count[floor_call] = num_customer

    # pick the highest one who is coming
    elif direction == "up" and floor_call > max(aim_floor_queue) and num_in_el == 0:

        # if someone was waiting, add to the floor queue
        aim_floor_queue.append(floor_call)
        aim_floor_queue.sort(reverse = True)
        leave_count[floor_call] = num_customer

    else:
        try:
            leave_count[floor_call] = num_customer + leave_count[floor_call]
        except:
            aim_floor_queue.append(floor_call)
            leave_count[floor_call] = num_customer
    
    return aim_floor_queue, leave_count, direction

# Manage the elevator state when it hits the aim floor 
def manage_aim_floor(direction, current_floor, aim_floor_queue, leave_count, num_in_el, capaticy, name, aim_floor_number, queue):
    
    # send people from 1st to the aim floor
    if direction == "up" and (current_floor == aim_floor_queue[0] or current_floor == max(aim_floor_queue)):
            
        try:
            in_number = aim_floor_number[aim_floor_queue[0]]
            aim_floor_number[aim_floor_queue[0]] = 0 # have to re-set
        except:
            in_number = 0
                
        # optimize - if people in the higher floor is calling, elevator will go up to pick
        out_number = 0 
            
        if current_floor == max(aim_floor_queue):
                
            try:
                out_number = leave_count[max(aim_floor_queue)]
                out_number_copy = leave_count[max(aim_floor_queue)]
            except:
                out_number = 0
                
            temp_value = num_in_el - in_number + out_number 
                
            if temp_value > capaticy:  
                out_number = capaticy - num_in_el + in_number
                leave_count[max(aim_floor_queue)] = out_number_copy - out_number
                queue = queue[out_number:]
                num_in_el = capaticy
                #print "!!!" + " There are " + str(num_in_el) + " customer in the " + name
                aim_floor_queue.sort(reverse = True)
            else:  
                num_in_el = temp_value
                try:
                    del leave_count[aim_floor_queue[0]]
                except:
                    pass
                queue = queue[out_number:]
                #print "!!!" + " There are " + str(num_in_el) + " customer in the " + name
                aim_floor_queue.sort(reverse = True)
                aim_floor_queue.pop(0)
            
        else:
            num_in_el = num_in_el - in_number + out_number
            #print "!!!" + " There are " + str(num_in_el) + " customer in the " + name
            aim_floor_queue.pop(0)
                        
        # Re-define the elevator state
        if len(aim_floor_queue) == 0 or current_floor >= max(aim_floor_queue):
            direction = "down"
        else:
            direction = "up"
            
            
        # optimize - pick the people who are calling but is in the floor lower than elevator's current floor 
    elif direction == "down" and current_floor == aim_floor_queue[0]:

        try:
            out_number = leave_count[aim_floor_queue[0]]
        except:
            out_number = 0
            
        if num_in_el + out_number > capaticy:
            temp_number = capaticy - num_in_el
            leave_count[aim_floor_queue[0]] = out_number - temp_number
            num_in_el = capaticy
            queue = queue[out_number:]
            #print "!!!" + " There are " + str(num_in_el) + " customer in the " + name
            
        else:
            num_in_el = num_in_el + out_number
            #print "!!!" + " There are " + str(num_in_el) + " customer in the " + name
            try:
                del leave_count[aim_floor_queue[0]]
            except:
                pass
            queue = queue[out_number:]
            aim_floor_queue.pop(0)
    else:
        pass
                
    return aim_floor_number, leave_count, aim_floor_queue, direction, num_in_el, queue