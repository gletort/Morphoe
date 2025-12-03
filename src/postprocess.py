import sys, os
import math
import random
import numpy as npy

def postprocess_simu(simuname):
    """ Run postprocessing on one simulation (folder) """
    print("Running")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(dir_path)
    print("Post-processing simulation "+simuname)
    mainfolder = os.getcwd()
    print(mainfolder)
    
    #" go to the simulation folder and read local parameters
    os.chdir( simuname )
    sys.path.append(".")
    print(os.getcwd())
    
    #from Matrix import *
    from Plots import plot_some_track, plot_mean_track, plot_time_bb 
    from Trajectories import load_trajectories 
    from Analyse import bounding_box_time 
    
    from params import N, tmax, colant, colmid, colpos, dt, antlim, postlim
    n = math.floor(N / 6)
    nstep = int(math.floor(tmax / dt))

    #############################################################
    """ Main function """
    if not os.path.exists('./post_process'):
        os.makedirs('./post_process')

    [simus, tracks, times, xs, ys] = load_trajectories(".")


    bbtime, bbhei = bounding_box_time(simus, times, xs, ys)
    plot_time_bb(bbtime, bbhei)

    utrack = npy.unique(tracks)

    # do anterior
    anty = []
    antx = []
    anttrack = []
    first = 0
    n = 0
    for t in utrack:
        keep = [ i for i in range(len(tracks)) if tracks[i]==t ]
        x = xs[keep]
        y = ys[keep]
        if y[0] > antlim:
            anty = npy.concatenate( (anty, y), axis=None)
            antx = npy.concatenate( (antx, x), axis=None)
            if npy.mean(x)<x[0]:
                x=-x
            if first == 0:
                antmeanx = x-x[0]
                antmeany = y-y[0]
                first = 1
            else:
                antmeanx = antmeanx + (x-x[0])
                antmeany = antmeany + (y-y[0])
            n = n + 1
            anttrack = npy.concatenate( (anttrack, npy.repeat(t, len(x))), axis=None )
    plot_some_track( anttrack, antx, anty, colant, "post_process/pool_tracks_anterior.png", 10)
    antmeanx = antmeanx/n
    antmeany = antmeany/n

    # do posterior
    posty = []
    postx = []
    posttrack = []
    first = 0
    n = 0
    for t in utrack:
        keep = [ i for i in range(len(tracks)) if tracks[i]==t ]
        x = xs[keep]
        y = ys[keep]
        if y[0] < postlim:
            posty = npy.concatenate( (posty, y), axis=None)
            postx = npy.concatenate( (postx, x), axis=None)
            if npy.mean(x)<x[0]:
                x=-x
            if first == 0:
                postmeanx = x-x[0]
                postmeany = y-y[0]
                first = 1
            else:
                postmeanx = postmeanx + (x-x[0])
                postmeany = postmeany + (y-y[0])
            n = n + 1
            posttrack = npy.concatenate( (posttrack, npy.repeat(t, len(x))), axis=None )
    plot_some_track( posttrack, postx, posty, colpos, "post_process/pool_tracks_posterior.png", 10)
    postmeanx = postmeanx / n
    postmeany = postmeany/n

    # do middle
    midy = []
    midx = []
    midtrack = []
    first = 0
    n = 0
    for t in utrack:
        keep = [ i for i in range(len(tracks)) if tracks[i]==t ]
        x = xs[keep]
        y = ys[keep]
        if y[0] >= postlim and y[0] <= antlim:
            midy = npy.concatenate( (midy, y), axis=None)
            midx = npy.concatenate( (midx, x), axis=None)
            if npy.mean(x)<x[0]:
                x=-x
            if first == 0:
                midmeanx = x-x[0]
                midmeany = y-y[0]
                first = 1
            else: 
                midmeanx = midmeanx + (x-x[0])
                midmeany = midmeany + (y-y[0])
            n = n + 1
            midtrack = npy.concatenate( (midtrack, npy.repeat(t, len(x))), axis=None )
    plot_some_track( midtrack, midx, midy, colmid, "post_process/pool_tracks_middle.png", 10)
    midmeanx = midmeanx/n
    midmeany = midmeany/n

    plot_mean_track( antmeanx, antmeany, colant, postmeanx, postmeany, colpos, midmeanx, midmeany, colmid, "post_process/pool_meantracks.png")

    os.chdir(mainfolder)
    print("Finished. Files saved in post_process folder in the simulation directory.")

if __name__ == "__main__":
    simuname = sys.argv[1]
    postprocess_simu(simuname)
