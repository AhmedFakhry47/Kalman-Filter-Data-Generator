import numpy as np
import math
from matplotlib import pyplot as plt
import random
import decimal


save_path = ""

#define initial position of my object
px_start = 0.11
py_start = 0.1

pi = np.pi

#define time interval ( timestep )
base_time = 1477010443000000
delta_t_us = .5*1e5
print(delta_t_us)
delta_t_sec = delta_t_us/1e6
print(delta_t_sec)
round_time_sec = 25

num_measurements = int(round_time_sec /delta_t_sec)
print(num_measurements)
num_states = 8

#Creation of Ground Truth matrix
GT = np.zeros((num_states,num_measurements),dtype = np.double)

GT[0,0] = px_start
GT[1,0] = py_start

#Create Sensors Matrices
ladar_m = np.zeros((3,num_measurements))
radar_m = np.zeros((4,num_measurements))

#Measurements noise of sensors
std_lad1 = 0.15
std_lad2 = 0.15

std_radr = 0.3
std_radphi = 0.03
std_radrd = 0.3


#Generating velocity ( linear and rotational , ALL GROUND TRUTH)
for count in range(0,num_measurements):
    current_time = base_time + (count * delta_t_us)
    print('the current time is :',current_time)
    #print(current_time)
    GT[7][count]  = current_time

    current_time = count*delta_t_us/1e6
    print('AFTER EVERYTHING : ',current_time)
    #Generate linear velocity
    GT[2][count] = 8 #+ 0.2*np.cos((2*pi/round_time_sec)*current_time)

    #Generate yaw rate ( rotational velocity)
    GT[4][count] = 0.55#*np.sin((2*pi/round_time_sec)*current_time)

#print(GT)


ladar_m[2][0] =base_time
radar_m[3][0] =base_time


# first laser measurement (special case)
ladar_m [0][0] = GT[0][0] + np.random.normal(0, std_lad1,size=None)
ladar_m [1][0] = GT[1][0] + np.random.normal(0, std_lad2,size=None)
ladar_m [2][0] = GT[7][0]

#radar measurements
p1  = GT[0][0]
p2  = GT[1][0]
v   = GT[2][0]
yaw = GT[3][0]

v1 = GT[2][0] * np.cos(GT[3][0])
v2 = GT[2][0] * np.sin(GT[3][0])


radar_m[0][0] = np.sqrt((p1**2) + (p2**2)) + np.random.normal(0, std_radr,size=None)
radar_m[1][0] = np.arctan2(p2,p1) + np.random.normal(0, std_radphi,size=None)
radar_m[2][0] = ( (p1*v1 + p2*v2 ) / np.sqrt((p1**2) + (p2**2)) ) + np.random.normal(0, std_radrd,size=None)
radar_m[3][0] = GT[7][0]

GT[5][0] = np.cos(yaw)* v
GT[6][0] = np.sin(yaw)* v


#Creating Sensor measurements
for count in range(1,num_measurements):

    time_d_s = (GT[7][count] - GT[7][count-1])/1e6

    p1 = GT[0][count-1]
    p2 = GT[1][count-1]
    v  = GT[2][count-1]
    yaw= GT[3][count-1]
    yaw_dot = GT[4][count-1]

    #Creating shape
    #print('yaw is : ',yaw)
    #print('time difference is :',time_d_s)
    '''
    if abs(yaw_dot) > 0.001 :
        p1_p = p1 + v/yaw_dot * ( np.sin (yaw + yaw_dot*time_d_s) - np.sin(yaw))
        p2_p = p2 + v/yaw_dot * ( np.cos(yaw) - np.cos(yaw+yaw_dot*time_d_s) )
    else:
    '''

    p1_p = p1+v * np.cos(yaw)**3 * time_d_s
    #print(p1_p)

    p2_p = p2+ (v * time_d_s)**2
    #print(p2_p)

    v_p = v
    yaw_p = yaw + ( yaw_dot * time_d_s)
    yaw_dot_p = yaw_dot

    GT[0][count] = p1_p
    GT[1][count] = p2_p
    GT[3][count] = yaw_p

    # laser measurements update
    ladar_m[0][count] = GT[0][count] + np.random.normal(0, std_lad1,size=None)
    ladar_m[1][count] = GT[1][count] + np.random.normal(0, std_lad2,size=None)
    ladar_m[2][count] = GT[7][count]

    # radar measurements update
    p1 = GT[0][count]
    p2 = GT[1][count]
    v  = GT[2][count]
    yaw= GT[3][count]

    v1 = GT[2][count] * np.cos(GT[3][count])
    v2 = GT[2][count] * np.sin(GT[3][count])

    radar_m[0][count] = np.sqrt((p1**2) + (p2**2)) + np.random.normal(0, std_radr,size=None)
    radar_m[1][count] = np.arctan2(p2,p1) + np.random.normal(0, std_radphi,size=None)
    radar_m[2][count] = (p1*v1 + p2*v2 ) / np.sqrt((p1**2) + (p2**2)) + np.random.normal(0, std_radrd,size=None)
    radar_m[3][count] = GT[7][count]

    GT[5][count] = np.cos(yaw)* v
    GT[6][count] = np.sin(yaw)* v


plt.plot(GT[0][:],GT[1][:],'.-b')
plt.show()


#Save Data Generated
GTT = GT.T
nrows,ncols = GTT.shape

#Save Ground Truth Only
with open(save_path+"/f100-Ground_Truth",'w')as f :
    for row in range(0,nrows):
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(GTT[row][0],GTT[row][1],GTT[row][2],GTT[row][3],GTT[row][4],GTT[row][5],GTT[row][6],GTT[row][7]))


lad_mt = ladar_m.T
rad_mt = radar_m.T
print(lad_mt[2][0],lad_mt[2][1],lad_mt[2][2])
nros,ncols = lad_mt.shape

#Save everything
with open(save_path+"/f100-sensor_measurements.txt",'w')as f :
    counter = 1
    GT_row = 0
    for row in range(0,nros):
        for key in ['L','R']:
            if (key == 'L' and (counter%2 ==1)):
                #save ladar estimations of P_x P_y and time in addition to corresponding Ground_Truth values
                f.write("L\t{:.5f}\t{:.5f}\t{}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n".format(lad_mt[row][0],lad_mt[row][1],int(lad_mt[row][2]),GTT[GT_row][0],GTT[GT_row][1],GTT[GT_row][5],GTT[GT_row][6]))
                GT_row +=1

            if (key == 'R' and (counter%2 ==0)):
                #save ladar estimations of r phi rd time in addition to corresponding Ground_Truth values
                f.write("R\t{:.5f}\t{:.5f}\t{:.5f}\t{}\t{:.5f}\t{:.5f}\t{:.5f}\t{:.5f}\n".format(rad_mt[row][0],rad_mt[row][1],rad_mt[row][2],int(rad_mt[row][3]),GTT[GT_row][0],GTT[GT_row][1],GTT[GT_row][5],GTT[GT_row][6]))
                GT_row +=1

        counter +=1

#lname = np.chararray((nros,1))
#sname[:] ='l'
