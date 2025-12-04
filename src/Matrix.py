import sys
import math
import numpy as npy
import importlib
sys.path.append(".")
import params 
importlib.reload(params)
from params import *

def distance(inx,iny):
    """distance for each points of vectors """
    return npy.sqrt( inx*inx + iny*iny )

def distancePt(inx,iny, x2, y2):
    """distance for each points of vectors """
    return npy.sqrt( (inx-x2)*(inx-x2) + (iny-y2)*(iny-y2) )

def matrice(inv, shape, add=0):
    ## definition of the "matrix" shape: encephale
    if shape == 'quadratic':
        yaecm = yecm + add
        xaecm = xecm + add
        res = -yaecm/(xaecm*xaecm) * inv*inv + yaecm
    if shape == 'cylindric':
        curN = len(inv)
        neg = npy.arange(0, curN/2)
        #xecm = 1.0
        #yecm = 3.0
        res = npy.repeat( xecm, curN )
        top = inv>yecm
        y1 = npy.copy(inv)
        y1[top] = inv[top] - yecm
        surtop = top & (y1>xecm)
        y1[surtop] = xecm
        res[top] = npy.sqrt( xecm*xecm - y1[top]*y1[top] )
        res[neg] = -res[neg] 
    return res

def xmatricepoint( y, shape ):
    ## get x coordinates for y
    if shape == 'quadratic':
        x = npy.sqrt( abs(y - yecm) / (yecm / (xecm*xecm)) )
    return x

def ymatricepoint( x, shape ):
    ## get x coordinates for y
    if shape == 'quadratic':
        y = x*x * (-yecm/(xecm*xecm)) + yecm
    return y

def dematrice( y0, shape, add, N, limH=N/2):
    ## definition of the "matrix" shape: encephale
    if shape == 'quadratic':
        #yecm = 3.8
        #xecm = 1.0
        x0 = npy.sqrt( abs(y0 - yecm) / (yecm / (xecm*xecm)) )
        neg = (y0 - yecm) > 0
        x0[neg] = npy.random.uniform(-0.001,0.001,1)
        x0[npy.arange(0,limH, dtype='int')] = -x0[npy.arange(0,limH, dtype='int')]
        a = -yecm / (xecm*xecm)
        nshift = add / math.sqrt(1 + 4*a*a)
        resx = x0 - 2*a*nshift
        resx[npy.arange(0,limH, dtype='int')] = x0[npy.arange(0,limH, dtype='int')] + 2*a*nshift
        resy = y0 + nshift
    if shape == 'cylindric':
        curN = len(y0)
        neg = npy.arange(0, curN/2)
        #xecm = 1.0 + add
        #yecm = 3.0 
        xaecm = xecm + add
        resx = npy.repeat( xaecm, curN )
        resy = npy.copy(y0)
        top = y0>yecm
        y1 = npy.copy(y0)
        y1[top] = y0[top] - yecm
        resx[top] = npy.sqrt( xaecm*xaecm - y1[top]*y1[top] )
        resx[neg] = -resx[neg] 
    return [resx,resy]
    
    
def closest( xin, yin, mx, my ):
    """ return closest point in the [mx, my] list of points from points"""
    xp = list(range(len(xin)))
    yp = list(range(len(yin)))
    for i in range(len(xin)):
        d = distance( mx-xin[i], my-yin[i] )
        ind = npy.argmin(d) 
        xp[i] = mx[ind]
        yp[i] = my[ind]

    return [npy.array(xp), npy.array(yp)]

def insidematrice( inx, iny, shape, shift ):
    """ definition of the "matrix" shape: encephale """
    if shape == 'quadratic':
        ymat = matrice( inx, shape, 0)
        ins = npy.zeros( (1, len(ymat)) )[0]
        ins[ iny < ymat ] = 1
    if shape == 'cylindric':
        xmat = matrice( iny, shape, 0)
        ins = npy.zeros( (1, len(iny)) )[0]
        ins[ npy.abs(inx) < npy.abs(xmat) ] = 1
    return ins

def insidematricePt( inx, iny, shape, shift ):
    """ definition of the "matrix" shape: encephale """
    if shape == 'quadratic':
        ymat = matrice( inx, shape, 0)
        if iny < ymat:
            return 1
        else:
            return -1
    if shape == 'cylindric':
        xmat = matrice( iny, shape, 0)
        ins = npy.zeros( (1, len(iny)) )[0]
        ins[ npy.abs(inx) < npy.abs(xmat) ] = 1
    return ins
