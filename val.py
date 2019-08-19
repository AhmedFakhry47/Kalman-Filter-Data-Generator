from matplotlib import pyplot as plt
import numpy as np
from tools import polar_to_cartesian

file = "/media/ahmed/Eng and Prgm/After 24-12/MachineLearning/Research/New/Mycode/my_data/other_people_data/obj_pose-laser-radar-synthetic-ukf-input.txt"


with open(file,'r') as f :
    f = f.readlines()
    num_lines = sum(1 for line in f)
    GT = np.zeros((int(num_lines/2),2))
    L  = np.zeros((int(num_lines/2),2))
    R  = np.zeros((int(num_lines/2),3))
    i  = 0
    j  = 0
    for line in f :
        line = line.split('\t')
        if (line[0]=='L'):
            try :
                L[i][0] = line[1]
                L[i][1] = line[2]
                GT[i][0] = line[4]
                GT[i][1] = line[5]
                i+=1
            except Exception as e:
                pass
        else :
            try :
                x,y,vx,vy = polar_to_cartesian (float(line[1]),float(line[2]),float(line[3]))
                R[j][0] = x
                R[j][1] = y
                print(R[j][0],R[j][1])
                GT[j][0] = line[5]
                GT[j][1] = line[6]
                j+=1
            except Exception as e:
                pass



print(L)
GTT = GT.T
LT = L.T
RT = R.T
plt.plot(GTT[0][:],GTT[1][:],'.-b')
plt.plot(LT[0][:],LT[1][:],'.-r')
plt.plot(RT[0][:],RT[1][:],'.-g')
plt.show()
