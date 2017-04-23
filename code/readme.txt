Python 2.7.13 should be used to run the code.

Required package : numpy, matplotlib

The detail description of each file.py is as below

(1) building.py : define the class of building that has the attributes “name”, “top_floor”, “num_people”

(2) elevator.py : define the class of elevator that has the attributes “name”, “direction”, “current_floor”, “capacity”, “num_customer”. There are three direction of elevator, say “up”, “move”, “stay”. For each iteration, elevator will take action based on the direction. For example, if direction is “up”, elevator will go up.

(3) people.py : define the function to generate the time distribution of people coming along with their aim_floor, or where people from (which floor). The time distribution obeys the poisson distribution in the morning time (8:00 - 11:00) , for the other time, the time and floor are generated randomly. In summary, generate_day function combine the distribution all together.

(4) optimize.py : define several functions to help optimise the operation of elevators. More details of optimisation methods could be found in the report.

(5) simulator_elevator.py : define the function to simulate the operation of 1,2,3,4 elevators separately.

(6) plot.py : define the function to visualise the final results to help analyse.

(7) main.py : define the function to control the whole simulation process. you can select your own buildings to evaluate the suitable number of elevators. 