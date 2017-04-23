import matplotlib.pyplot as plt
import numpy as np

def plot_time_move(total_move, average_waiting_time, building):

    x = range(1,5)
    y1 = total_move
    y2 = average_waiting_time

    fig = plt.figure()

    ax1 = fig.add_subplot(111)
    ax1.plot(x, y1, "b")
    ax1.set_ylabel(" Total move of the elevators ")
    ax1.set_xlabel(" Number of elevators ")

    title_name = " The ideal number of elevators for " + building.name + " ( " + str(building.num_people) + " " + str(building.top_floor) + " ) "

    ax1.set_title(title_name)

    ax2 = ax1.twinx()  
    ax2.plot(x, y2, "r")
    ax2.set_ylabel(" Average waiting time per person (s) ")
    ax2.set_xlabel(" Number of elevators ")
    plt.show()

def plot_time_empty(total_move, total_empty_move, average_waiting_time, building):

    empty_percentage = []

    for i in range(4):
        empty_percentage.append(round(total_empty_move[i]/float(total_move[i]),2))

    x = range(1,5)
    y1 = empty_percentage
    y2 = average_waiting_time

    fig = plt.figure()

    ax1 = fig.add_subplot(111)
    ax1.plot(x, y1, "b")
    ax1.set_ylabel(" Empty percentage (%) ")
    ax1.set_xlabel(" Number of elevators ")

    title_name = " The ideal number of elevators for " + building.name + " ( " + str(building.num_people) + " " + str(building.top_floor) + " ) "

    ax1.set_title(title_name)

    ax2 = ax1.twinx()  
    ax2.plot(x, y2, "r")
    ax2.set_ylabel(" Average waiting time per person (s) ")
    ax2.set_xlabel(" Number of elevators ")
    plt.show()




