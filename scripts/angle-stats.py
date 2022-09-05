import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
sys.path.insert(0,'../plot/')
import plot
import archive
import math
# input a directory which contains subforders of data
# python3 angle-stats.py mydird/data
# test the angle between cell orientation and passive force
frame_start = 100
frame_end = 250
N_phase = 72
N_sample = N_phase*(frame_end - frame_start + 1)
dir= sys.argv[1]
ar = archive.loadarchive(dir)

def angle(n,f):
    #n--nematic director with head tail symmetry  np.array
    #f--vector  np.array
    #return value between [0,pi/2]
    dot_prod = n[0]*f[0] + n[1]*f[1]
    n_norm = math.sqrt(n[0]*n[0] + n[1]*n[1])
    f_norm = math.sqrt(f[0]*f[0] + f[1]*f[1])
    theta = math.acos(dot_prod/(n_norm*f_norm))
    if theta > math.pi/2.0:
        theta = math.pi - theta
    return theta/math.pi*180

data = np.zeros(N_sample,dtype = [('S','double'),('angle','double')])
count = 0
for num in range(frame_start,frame_end):
    frame = ar.read_frame(num)
    print('frame {} \n'.format(num))
    #calculate the angle between cell orientation,passive force and velocity
    for i in range(frame.nphases):
        Q00 = frame.S00[i]
        Q01 = frame.S01[i]
        S = math.sqrt(Q00**2 + Q01**2)
        nx = math.sqrt((1 + Q00/S)/2)
        ny = np.sign(Q01)*math.sqrt((1 - Q00/S)/2)
        data[count]['angle'] = angle(frame.Fpassive[i],[nx,ny])
        data[count]['S'] = S
        count += 1 
#avg_angle = sum_angle/(ar._nframes+1 - frame_num0)
data = np.sort(data,order='S')
level = [0,int(N_sample*0.33),int(N_sample*0.66)]
lowest_S = data['angle'][level[0]:level[1]]
middle_S = data['angle'][level[1]+1:level[2]]
highest_S = data['angle'][level[2]+1:N_sample-1]

fig = plt.figure()
ax1 = fig.add_subplot(131)
ax1.hist(lowest_S,bins = 15)
ax1.set_title('lowest 33%')

ax2 = fig.add_subplot(132)
ax2.hist(middle_S,bins = 15)
ax2.set_title('middle 33%')

ax3 = fig.add_subplot(133)
ax3.hist(highest_S,bins = 15)
ax3.set_title('highest 33%')
print(data[0],data[1])
print(data[100],data[101])


plt.show()