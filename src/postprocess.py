import sys, os
from Matrix import *
from Plots import *
from Trajectories import *
from Analyse import *
import math
import random
import numpy as npy

from params import *
n = math.floor(N / 6)
nstep = int(math.floor(tmax / dt))


#############################################################
""" Main function """

[simus, tracks, times, xs, ys] = load_trajectories('./')


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
plot_some_track( anttrack, antx, anty, colant, "pool_tracks_anterior.png", 10)
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
plot_some_track( posttrack, postx, posty, colpos, "pool_tracks_posterior.png", 10)
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
plot_some_track( midtrack, midx, midy, colmid, "pool_tracks_middle.png", 10)
midmeanx = midmeanx/n
midmeany = midmeany/n

plot_mean_track( antmeanx, antmeany, colant, postmeanx, postmeany, colpos, midmeanx, midmeany, colmid, "pool_meantracks.png")

