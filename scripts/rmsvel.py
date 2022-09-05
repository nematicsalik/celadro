#
# This is a simple example file to show the plotting capabilities of the
# program. Uses python2.
#
# Usage:
#
#   python2 rmsvel.py input
#
#  where
#
#    intput -- the input file or directory

import matplotlib.pyplot as plt
import sys
import numpy as np
#from math import sqrt

# import local libs
sys.path.insert(0, "../plot/")
import plot
import archive

##################################################
# Init

#if len(sys.argv) == 1:
#    print("Please provide an input file.")
#    exit(1)
rmsvel = []

for w in range(25,33):
# load archive from file
    ar = archive.loadarchive(str(w))

##################################################
# plot simple animation of phases
    rms = []
    vxfull = []
    vyfull = []

#    rms = np.zeros(ar._nframes+1)
#    tox = np.zeros(ar._nframes+1)
#    toy = np.zeros(ar._nframes+1)
    c=0
    for i in range(100, ar._nframes+1):
        frame = ar.read_frame(i)
        print("{}/{}".format(i, ar._nframes),)
        vx, vy = plot.get_velocity_field(frame.phi, frame.velocity, size=24)
        vxfull.append(vx)
        vyfull.append(vy)
    #    print("vx={}, vy={}, rms={}".format(tox[c], toy[c], rms[c]))
        c += 1
    vxfull = np.array(vxfull)
    vyfull = np.array(vyfull)
    rms = (np.sqrt(np.mean(vxfull**2+vyfull**2)))
    print("rms velocity = {}".format(rms))
    rmsvel.append(rms)
rmsvel = np.array(rmsvel)
np.savetxt("rmsvel_omega=0.020.csv", rmsvel, delimiter = ',')

    
#plt.plot(np.arange(0, len(rms)), rms)
#plt.plot(np.arange(0, len(rms)), tox)
#plt.plot(np.arange(0, len(rms)), toy)
#plt.show()
