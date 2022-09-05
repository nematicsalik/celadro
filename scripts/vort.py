#
# This is a simple example file to show the plotting capabilities of the
# program. Uses python2.
#
# Usage:
#
#   python2 plot-cells.py input [output]
#
#  where
#
#    intput -- the input file or directory
#    output -- (optional) if present saves the animation as a video to show to
#              your mom.
import sys
import os
import numpy as np

sys.path.insert(0, "../plot/")
import plot
import archive
##################################################
# Init

if len(sys.argv) == 1:
    print("Please provide an input file.")
    exit(1)

# load archive from file
ar = archive.loadarchive(sys.argv[1])

oname = ""
if len(sys.argv) == 3:
    oname = sys.argv[1]+"/w_field/"
    print("Output name is", sys.argv[2])

if not os.path.isdir(oname):
    os.makedirs(oname)

#for i in np.arange(int(0.3*ar._nframes), ar._nframes+1, step=1):
for i in range(1, ar._nframes+1):
#for i in range(ar._nframes, ar._nframes+1):
#for i in range(1, 3):
    print("frame ", i)
    frame = ar.read_frame(i)
       
    vx, vy = plot.get_velocity_field(frame.phi, frame.velocity, size = 1)
    w = plot.get_vorticity_field(vx, vy)    
    
    np.savetxt(oname + "w_frame" + str(i).zfill(3) + '_' + 
               sys.argv[2] + ".csv", w)    