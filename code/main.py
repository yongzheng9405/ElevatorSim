from building import *
from elevator import *
from optimize import *
from people import *
from simulator_elevator import *
from plot import *

# Define the global value
e1 = elevator("elevator 1", "stay", 1, 15, 0)
e2 = elevator("elevator 2", "stay", 1, 15, 0)
e3 = elevator("elevator 3", "stay", 1, 15, 0)
e4 = elevator("elevator 4", "stay", 1, 15, 0)

b1 = building("building 1", 10, 500)
b2 = building("building 2", 15, 750)
b3 = building("building 3", 20, 1000)
b4 = building("building 4", 25, 1250)
b5 = building("building 5", 30, 1500)

simulation_time = 10800

def main():

	# Set the initial parameters
	building_dict = {"1":b1, "2":b2, "3":b3, "4":b4, "5":b5}

	num_building = raw_input(" Select the building you want to analyze: " )
	building = building_dict[num_building]

	# Generate the people
	arriving_time, customer_floor, calling_time, customer_current_floor = generate_day(building.top_floor, building.num_people)

	# Start simulation
	total_move_1, total_empty_move_1, average_waiting_time_1 = simulator_elevator_1(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, building.num_people)
	total_move_2, total_empty_move_2, average_waiting_time_2 = simulator_elevator_2(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, e2, building.num_people)
	total_move_3, total_empty_move_3, average_waiting_time_3 = simulator_elevator_3_2(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, e2, e3, building.num_people)
	total_move_4, total_empty_move_4, average_waiting_time_4 = simulator_elevator_4_2(arriving_time, calling_time, customer_floor, customer_current_floor, simulation_time, e1, e2, e3, e4, building.num_people)

	total_move = [total_move_1, total_move_2, total_move_3, total_move_4]
	total_empty_move = [total_empty_move_1, total_empty_move_2, total_empty_move_3, total_empty_move_4]
	average_waiting_time = [average_waiting_time_1, average_waiting_time_2, average_waiting_time_3, average_waiting_time_4]

	plot_time_move(total_move, average_waiting_time, building)
	plot_time_empty(total_move, total_empty_move, average_waiting_time, building)

if __name__ == '__main__':
	main()
