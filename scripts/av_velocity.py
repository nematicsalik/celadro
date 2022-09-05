#
# Script for averaging vx over x and vy over y
#
# Usage:
#
#   python3 av_velocity.py input [output] start_frame_index
#
#  where
#
#    intput -- the input file or directory
#    output -- (optional) if present saves the animation as a video to show to
#              your mom.
#    start_frame_index index of the frame from which the processing should begin
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "../plot/")
import animation
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
if len(sys.argv) == 4:
    oname = sys.argv[1]+"/velocity_averages/"
    print("Output name is", sys.argv[2])

if not os.path.isdir(oname):
    os.makedirs(oname)

start_frame = int(sys.argv[3])

#this parameter controls the coarse-graining of the velocity field
avg=1

for i in range(start_frame, ar._nframes+1):
    print("frame ", i)
    frame = ar.read_frame(i)
    
    #get the velocity field components
    vx,vy = plot.get_velocity_field(frame.phi, frame.velocity, size = 1)
    
    if i == start_frame:
        vxavoverxmean = np.zeros(shape=frame.parameters['Size'][1])
        vxavoverxsqmean = np.zeros(shape=frame.parameters['Size'][1])
        vyavoverymean = np.zeros(shape=frame.parameters['Size'][0])
        vyavoverysqmean = np.zeros(shape=frame.parameters['Size'][0])
        
    #average vx over x by integrating over that variable; average the result
    #over all considered frames as well
    vxavoverxmean += np.trapz(vx, axis=1)/frame.parameters['Size'][0] \
        / (ar._nframes + 1 -start_frame)
   
    #calculate the average square of vx (useful for calculating the standard 
    #deviation later)
    vxavoverxsqmean += np.square(np.trapz(vx, axis=1))/ \
        frame.parameters['Size'][0]/(ar._nframes + 1 -start_frame)   
        
    #average vy over y
    vyavoverymean += np.trapz(vy, axis=0)/frame.parameters['Size'][1] \
        / (ar._nframes + 1 -start_frame)
   
    #calculate the average square of vy (useful for calculating the standard 
    #deviation later)
    vyavoverysqmean += np.square(np.trapz(vy, axis=0))/ \
        frame.parameters['Size'][1]/(ar._nframes + 1 -start_frame)         
        
    #v = pow(pow(vx, 2) + pow(vy, 2), .5)

#calculate the sample standard deviation of the average of vx over x
stdevvx = np.power((vxavoverxsqmean-np.square(vxavoverxmean))*
                   (ar._nframes+1-start_frame)/(ar._nframes-start_frame),.5)
#calculate the standard deviation of the average of vy over y
stdevvy = np.power((vyavoverysqmean-np.square(vyavoverymean))*
                   (ar._nframes+1-start_frame)/(ar._nframes-start_frame), .5)

figvx, axs = plt.subplots(1)

#plot the mean vx averaged over x and time +/- a standard deviation
axs.plot(np.arange(0, frame.parameters['Size'][1], step=avg), vxavoverxmean,
          label="$v_{x}$ averaged over $x$ and $t$",color='black')

axs.plot(np.arange(0, frame.parameters['Size'][1], step=avg), 
           vxavoverxmean + stdevvx, '--', 
           color='black')
axs.plot(np.arange(0, frame.parameters['Size'][1], step=avg), 
           vxavoverxmean - stdevvx, '--', 
           color='black')

axs.legend(loc="lower right")
axs.set_xlabel('$y$')
axs.set_ylabel('$v_{x}(y)$')

#save the figure
figvx.savefig(oname+sys.argv[2]+'_av_vx_frame_'+str(start_frame)+\
           '_to_'+str(ar._nframes+1)+'.pdf')

#save the data to a text files
np.savetxt(oname+sys.argv[2]+"_vxavoverxmean_frame_"+str(start_frame)+\
           "_to_"+str(ar._nframes+1)+".csv", vxavoverxmean)
np.savetxt(oname+sys.argv[2]+"_vxavoverxstdev_frame_"+str(start_frame)+\
           "_to_"+str(ar._nframes+1)+".csv", stdevvx)

##################################################
figvy, axs = plt.subplots(1)

#plot the mean vy averaged over y and time +/- a standard deviation
axs.plot(np.arange(0, frame.parameters['Size'][1], step=avg), vyavoverymean,
          label="$v_{y}$ averaged over $y$ and $t$",color='black')

axs.plot(np.arange(0, frame.parameters['Size'][1], step=avg), 
           vyavoverymean + stdevvy, '--', 
           color='black')
axs.plot(np.arange(0, frame.parameters['Size'][1], step=avg), 
           vyavoverymean - stdevvy, '--', 
           color='black')

axs.legend(loc="lower right")
axs.set_xlabel('$x$')
axs.set_ylabel('$v_{y}(x)$')

#save the figure
figvy.savefig(oname+sys.argv[2]+'_av_vy_frame_'+str(start_frame)+\
           '_to_'+str(ar._nframes+1)+'.pdf')

#save the data to a text files
np.savetxt(oname+sys.argv[2]+"_vyavoverymean_frame_"+str(start_frame)+\
           "_to_"+str(ar._nframes+1)+".csv", vyavoverymean)
np.savetxt(oname+sys.argv[2]+"_vyavoverystdev_frame_"+str(start_frame)+\
           "_to_"+str(ar._nframes+1)+".csv", stdevvy)