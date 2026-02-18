
import sys
import math
import numpy as npy

def deplacement( inx, iny ):
    """ final position - initial position """
    last = len(inx)-1
    depx = (inx[last,]-inx[0,]) 
    depy = (iny[last,]-iny[0,]) 
    return npy.sqrt( depx*depx + depy*depy )

def bounding_box( inx, iny ):
    """ final cell width and heigth """
    last = len(inx)-1
    left = inx[0] < 0
    right = inx[0] >= 0
    posx = npy.max(inx[last,left]) - npy.min(inx[last,left])
    negx = npy.max(inx[last,right]) - npy.min(inx[last,right])
    posy = npy.max(iny[last,left]) - npy.min(iny[last,left])
    negy = npy.max(iny[last,right]) - npy.min(iny[last,right])
    return [posx, negx, posy, negy]

def bb_time( intime, inx, iny ):
    """ width and height of the bounding box in time """
    width = npy.array([0.0]*len(npy.unique(intime)))
    height = npy.array([0.0]*len(npy.unique(intime)))
    time = npy.array([0.0]*len(npy.unique(intime)))
    i = 0
    for t in npy.unique(intime):
        keep = (npy.where(intime==t))[0]
        x = inx[keep,]
        y = iny[keep,]
        left = npy.where(x < 0)[0]
        right = npy.where(x >= 0)[0]
        posx = npy.max(x[left]) - npy.min(x[left]) 
        negx = npy.max(x[right]) - npy.min(x[right])
        posy = npy.max(y[left]) - npy.min(y[left])
        negy = npy.max(y[right]) - npy.min(y[right])
        width[i] = npy.mean([posx, negx])
        height[i] = npy.mean([posy, negy])
        time[i] = t
        i = i + 1
    return [time, width, height]

def bounding_box_time(simus, times, xs, ys):
    """ Calculate extend of BB in times for each simus """
    restime = []
    resheight = []
    for simu in npy.unique(simus):
        keep = npy.where(simus==simu)[0]
        time = times[keep]
        x = xs[keep]
        y = ys[keep]
        time, width, height = bb_time(time, x, y)
        restime = npy.concatenate((restime,time),axis=None)
        resheight = npy.concatenate((resheight,height),axis=None)
    return restime, resheight
