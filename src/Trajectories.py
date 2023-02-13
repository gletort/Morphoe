import sys, os, re
sys.path.append('/home/gaelle/Ext/Julie/code/')
import math
import numpy as npy
from params import *
import pandas as pd

def save_trajectory( x, y, time, repnum ):
    """ write datas to txt file """
     
    keep = npy.arange(0, len(x[:,1]), dataFreq, dtype='int')

    first = 1
    ## Chaque cellule
    for i in (range(len(x[1,:]))):
        t = keep * dt
        cellx = x[keep,i]
        celly = y[keep,i]
        tab = npy.asarray( (npy.repeat(i, len(cellx)), t, cellx, celly) )
        if first:
            data = tab
            first = 0
        else:
            data = npy.hstack((data, tab))
   
    outname = './trajectories/simu_'+str(repnum)+'.txt'
    with open(outname, 'w+') as datafile_id:
        npy.savetxt(datafile_id, data.T, header="Track\tTime\tX\tY", delimiter='\t', comments='')
        datafile_id.close()

def is_time( filename, basename='simus_' ):
	""" Check if given file is an output file
	And extract its time information if yes
	"""
	if os.path.isfile( filename ):
		ind = filename.find( basename )
		if ind >= 0:
			num = filename[ind+len(basename):]
			num = num[ 0 : (len(num)-4) ]
			return int(num)
	return -1

def get_simus( datapath, name='/trajectories/', filename='simu_' ):
	""" Return sorted times list """
	fold = datapath+name
	filelist = os.listdir( fold )
	times = []
	for f in filelist:
		res = is_time( os.path.join(fold, f), filename )
		if res != -1:
			times.append( res )
	return npy.sort(npy.unique(times))

def column_names( filein, delim=';' ):
	""" read first line to get the column names """
	try:
		reading = open( filein, 'r' )
		line = reading.readline().strip()
		reading.close()
		col_names = re.split(delim, line)
	except Exception as e:
		raise Exception( "Problem while loading file "+filein+" :"+str(e) )
	return col_names

def read_traj( numsim ):
    """ read trajectory file """
    myfile = './trajectories/simu_'+str(numsim)+'.txt'
    #cnames = column_names( myfile, '\t' )
    #dt = dict(zip( cnames, ('float',)*len(cnames) ))
    #datas = npy.loadtxt( myfile, dt, delimiter='\t', skiprows=1 )
    datas = pd.read_csv( myfile, delimiter='\t')
    return datas


def load_trajectories(mydir):
    """ load directory trajectories files """
    nums = get_simus(mydir)
    times = []
    xs = []
    ys = []
    ids = []
    simus = []
    count = 0
    for n in nums:
        datas = read_traj(n)
        times = npy.concatenate((times, datas['Time']), axis=None)
        xs = npy.concatenate((xs, datas['X']), axis=None)
        ys = npy.concatenate((ys, datas['Y']), axis=None)
        tracky = datas['Track']+count*200 ## no more than 200 cells in one simu, else to change
        ids = npy.concatenate((ids, tracky), axis=None)
        simus = npy.concatenate((simus, npy.repeat(n, len(datas['X']))), axis=None)
        count = count + 1
    return [simus, ids, times, xs, ys]
