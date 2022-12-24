import random
import sys
sys.path.append('../')

from Common_Libraries.p2_sim_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()
update_thread = repeating_timer(2, update_sim)


'''
P2 final code (Fri-42),
Authors:
Hamza Siddiqui (siddih38), Kyler Witvoet (witvoetk), Gordon Tam (tamg3)
'''

#Threshold value and home coordinates
THRESHOLD = 0.5
HOME = [0.406,0.0,0.483]
CONTAINERS = []

'''
Return drop off coordinates of  specified container
'''

# place small containers on top and large containers in the drawers

def identify_autoclave(container_ID):
    if container_ID == 1: # small red container
        return [-0.63,0.254,0.356] 

    elif container_ID == 2: # small green container
        return [0.0,-0.676,0.356]

    elif container_ID == 3: # small blue container
        return [0.0, 0.676, 0.356]

    elif container_ID == 4: # large red container
        return [-0.408,0.165,0.13]

    elif container_ID == 5: # large green container
        return [0.0,-0.5,0.13]
    elif container_ID == 6: # large blue container
        return [0.0,0.5,0.13]

'''
Function that takes the id of a container as input
and returns the coordinates of the corresponding
autoclave and opens or closes the auto clave drawer if needed
'''
def open_autoclave(container_ID,open):
    while True:
        # Open autoclave when R > 0.5 and L= 0 
        if arm.emg_right() > THRESHOLD and arm.emg_left() == 0:
            if open == True:
                if container_ID == 4: # large red container
                    arm.open_red_autoclave(True)
                elif container_ID == 5: # large green container
                    arm.open_green_autoclave(True)
                elif container_ID == 6: # large blue container
                    arm.open_blue_autoclave(True)
            else:
                if container_ID == 4: # large red container
                    arm.open_red_autoclave(False)
                elif container_ID == 5: # large green container
                    arm.open_green_autoclave(False)
                elif container_ID == 6: # large blue container
                    arm.open_blue_autoclave(False)
            break

'''
Function that takes the id of a container as input
and determines how much the control gripper should 
open or close based on the size of the container
'''
def control_gripper(container_ID,open):
    while True:
        # control gripper (opens) L > 0.5 R = 0 
        if arm.emg_right() == 0 and arm.emg_left() > THRESHOLD:
            if open == True:
                if container_ID <= 3: # closes by 30 if the container is small
                    arm.control_gripper(30)
                else: # closes by 25 if the container is large
                    arm.control_gripper(25)
            else:
                if container_ID <= 3: # opens by 30 if the container is small
                    arm.control_gripper(-30)
                else: # opens by 25 if the container is large
                    arm.control_gripper(-25)
            break
        
'''
Function that move the end effector home
and then to specific coordinantes
'''
def move_end_effector(coords):
    while True:
        # move end effector L & R > Threshold
        if arm.emg_right() > THRESHOLD and arm.emg_left() > THRESHOLD:
            arm.move_arm(HOME[0],HOME[1],HOME[2])
            time.sleep(2)
            arm.move_arm(coords[0],coords[1],coords[2])
            break

'''
Main function: randomly spawns a container and places it in
the corresponding autoclave
'''
def main():

    container_coords = []
    container_ID = random.randint(1,6) # randomly chooses a container
    pickup_coords = [0.534, 0.0, 0.044] # coords of container pick up location

    for i in range(6):
        print(CONTAINERS)
        # ensures containers already spawned don't spawn in again
        CONTAINERS.append(container_ID)
        while container_ID in CONTAINERS: 
            container_ID = random.randint(1,6)
        arm.spawn_cage(container_ID)

        container_coords = identify_autoclave(container_ID)

        open_autoclave(container_ID,True)

        move_end_effector(pickup_coords)

        control_gripper(container_ID,True)

        move_end_effector(container_coords)

        control_gripper(container_ID,False)

        move_end_effector(HOME)

        open_autoclave(container_ID,False)



