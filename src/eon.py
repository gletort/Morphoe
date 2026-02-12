import sys
import os
import importlib
import math
import random
import numpy as npy

## import the source code
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
import Matrix, Plots, Trajectories, Analyse
importlib.reload(Matrix)
importlib.reload(Plots)
importlib.reload(Trajectories)
importlib.reload(Analyse)

from Matrix import * 
from Plots import *
from Trajectories import *
from Analyse import *
extension = ".png"
## import the current simulation parameters
sys.path.append(".")
import params 
importlib.reload(params)
from params import *

#############################################################

def time_step(t):
    """ 
        Perform one time step of cell migration simulation.
    
        This function updates the positions of all cells based on various biological
        forces including random motion, chemotaxis, cell-cell interactions, and
        cell-matrix interactions.
    
        Parameters
        t : int
            Current time step index
        
        Global Variables Updated
        x : numpy.ndarray
            Array of shape (nstep, N) containing x-coordinates of cells at each time step
        y : numpy.ndarray
            Array of shape (nstep, N) containing y-coordinates of cells at each time step
        chemo : float
            Chemotactic sensitivity coefficient
    """
    global x, y, theta, chemo, num, nmat

    chemo = chemop
    
    ### random motion
    x[t,] = x[t-1,] + npy.sqrt(2*D*dt) * npy.random.randn(1,N)
    y[t,] = y[t-1,] + npy.sqrt(2*D*dt) * npy.random.randn(1,N)
    
    ### add vertical force
    y[t,] = y[t-1,] + push*dt
    
    ## add chemotaxis force
    if all_matrix_chemo <= 0:
        if central_point_source > 0:
            # gradient decrease when further from chemotaxis source
            dist = distancePt( x[t-1,], y[t-1,], 0, ysource )
            ampl = (1.0 / npy.power( 1+dist,1 ) )
            if chemo_cte>0:
                ampl = chemo_cte
            x[t,] = x[t,] - chemo*dt * x[t-1,]/dist * ampl
            y[t,] = y[t,] - chemo*dt * (y[t-1,]-ysource)/dist * ampl
        if line_source > 0:
            ## vertical line source
            if line_source == 1:
                nx = 8
                xinf = xyline -dxyline/2
                xsup = xyline + dxyline/2
                for xind in range(nx):
                    xl = xinf + (xsup-xinf)*xind/nx
                    ny = 50
                    ymax = ymatricepoint(xl, shape)
                    dy = yecm*2/ny
                    ys = -yecm
                    chem = chemoline
                    for yind in range(ny):
                        ys = ys + dy
                        if ys <= ymax*1.01:
                            dist1 = distancePt( x[t-1], y[t-1], xl, ys )
                            ampl = (1.0 / npy.power( 1+dist1,1 ) )
                            if chemo_cte>0:
                                ampl = chemo_cte
                            x[t,] = x[t,] - chem*dt * (x[t-1,]-xl)/dist1 * ampl
                            y[t,] = y[t,] - chem*dt * (y[t-1,]-ys)/dist1 * ampl
            ## horizontal line source
            if line_source == 2:
                ny = 8
                yinf = xyline-dxyline/2
                ysup = xyline+dxyline/2
                for yind in range(ny):
                    yl = yinf + (ysup-yinf)*yind/ny
                    nx = 50
                    xs = -xmatricepoint( yl, shape ) 
                    dx = abs(xs)*2/nx
                    chem = chemoline
                    for xind in range(nx):
                        xs = xs + dx
                        dist1 = distancePt( x[t-1], y[t-1], xs, yl )
                        ampl = (1.0 / npy.power( 1+dist1,1 ) )
                        if chemo_cte>0:
                            ampl = chemo_cte
                        x[t,] = x[t,] - chem*dt * (x[t-1,]-xs)/dist1 * ampl
                        y[t,] = y[t,] - chem*dt * (y[t-1,]-yl)/dist1 * ampl
            else:
                x[t,] = x[t,]
                y[t,] = y[t,]

    
    ## add cell-cell interaction
    for i in range(N):
        distance2i = distance(x[t-1,]-x[t-1,i], y[t-1,]-y[t-1,i])
        for j in npy.arange((i + 1),N,1):
            ## cell j and i interact
            if distance2i[j] < d_interaction:
                coef = 1 - d_eq / distance2i[j]
                cur_cell_cell = cell_cell

                # if put different interactions strengths between cells
                if d_cell_cell > 0:
                    cur_cell_cell = (diff_cell_cell[i] + diff_cell_cell[j]) / 2.0
                # strong repulsion if too close
                if coef < 0:
                    cur_cell_cell = -3*coef*coef
                else:
                    cur_cell_cell = coef * cur_cell_cell
                
                # interactions in x
                interx = cur_cell_cell * (x[t-1,j] - x[t-1,i])   # (ri-rj) * coef
                x[t,i] = x[t,i] + dt * interx
                x[t,j] = x[t,j] - dt *interx
                
                # interactions in y
                intery = cur_cell_cell * (y[t-1,j] - y[t-1,i])
                y[t,i] = y[t,i] + dt*intery
                y[t,j] = y[t,j] - dt*intery


    ## add cell-matrice interaction
    [projx,projy] = closest( x[t-1,], y[t-1,], xmat, ymat )
    distance2mat = distance( x[t-1,] - projx, y[t-1,] - projy ) + 5e-05  ## avoid div by 0
    close2mat = distance2mat < 4 * d_interaction
    inter_coeff = cell_mat * 1 * (1 - d_eq/2 / ( distance2mat[close2mat]))

    if d_cell_mat > 0:
        midy = (y[t-1,] <= 1.5 ) & (y[t-1,] >= - 1.5 )
        inter_coeff[midy] = inter_coeff[midy] * 100

    if no_ecm_adhesion > 0:
        inter_coeff[close2mat] = npy.zeros( (1,sum(close2mat)) )

    ## get cells that are inside matrix, and put high coeff
    ins = insidematrice( x[t-1,], y[t-1,], shape, d_eq/2 )
    inter_coeff[ins > 0] = out
    
    x[t,close2mat] = x[t,close2mat] + dt * inter_coeff * (projx[close2mat] - x[t-1,close2mat])
    y[t,close2mat] = y[t,close2mat] + dt * inter_coeff * (projy[close2mat] - y[t-1,close2mat])

    ## take only closer source point
    if all_matrix_chemo == 2:
            ampl = (1.0 / npy.power( 1+distance2mat,1 ) )
            if chemo_cte>0:
                ampl = chemo_cte
            x[t,] = x[t,] - chemo*dt * (x[t-1,] - projx) / distance2mat * ampl
            y[t,] = y[t,] - chemo*dt * (y[t-1,] - projy) / distance2mat * ampl 
    
    ## take all matrix point
    if all_matrix_chemo == 1:
        nx = 50
        ny = 100
        dy = yecm*2/ny
        ys = -yecm
        xs = -xecm*1.5
        chem = chemo/nmat
        for xind in range(nx):
            xs = xs + dy
            ys = -yecm
            for yind in range(ny):
                ys = ys + dy
                if insidematricePt( xs, ys, shape, 0 ):
                    dist1 = distancePt( x[t-1], y[t-1], xs, ys )
                    ampl = (1.0 / npy.power( 1+dist1,1 ) )
                    if chemo_cte>0:
                        ampl = chemo_cte
                    x[t,] = x[t,] - chem*dt * (x[t-1,]-xs)/dist1 * ampl
                    y[t,] = y[t,] - chem*dt * (y[t-1,]-ys)/dist1 * ampl


    ## inhibitrice zones
    if inhibition_zones > 0:
            inhibant = y[t-1,] < inh_min
            y[t,inhibant] = y[t,inhibant] - inhib_coeff * dt * (y[t-1,inhibant] - inh_min)
            inhibpost = y[t-1,] > inh_max
            y[t,inhibpost] = y[t,inhibpost] - inhib_coeff * dt * (y[t-1,inhibpost] - inh_max)

    ## plot
    if make_movie == 1 and t%mfreq == 1:
        plotte_traj( x, y, cols, xmat, ymat, chemo, t, 'final_images/image'+(str(num).zfill(6))+extension )
        num = num + 1


#############################################################
def main_function(cell_cell_interaction=None, cell_mat_interaction=None, D_coeff=None, cell_chem_interaction=None):
    """ 
     Main function to run cell migration simulation.

    This function initializes the simulation environment, sets up initial conditions,
    runs the time stepping loop, and generates output visualizations and data files.

    Parameters
    cell_cell_interaction : float, optional
    Strength of cell-cell interaction forces. If None, uses global cell_cell value.
    cell_mat_interaction : float, optional
    Strength of cell-matrix interaction forces. If None, uses global cell_mat value.
    D_coeff : float, optional
    Diffusion coefficient for random motion. If None, uses global D value.
    cell_chem_interaction : float, optional
    Chemotactic sensitivity coefficient. If None, uses global chemop value.

    Global Parameters Used
    N : int Number of cells in simulation
    tmax : float Maximum simulation time
    dt : float Time step size
    shape : str Matrix geometry ('quadratic' or 'cylindric')
    uniform : bool Whether to distribute cells uniformly
    nrepet : int Number of repetitions/realizations
    make_movie : bool Whether to generate movie frames
    mfreq : int Movie frame frequency

    Simulation Process
    Initializes cell positions based on geometry and distribution
    Sets up extracellular matrix (ECM) structure
    Assigns cell types/colors based on spatial regions
    Runs time stepping loop for nstep iterations
    Generates trajectory plots at start, midpoint, and end
    Creates tracking visualizations for different cell populations
    Saves trajectory data and statistics
       """
    #global cell_cell, cell_mat, D, chemop
    global x, y, theta, chemo, num, nmat, xmat, ymat, cols, N
    if cell_cell_interaction is not None:
        cell_cell = cell_cell_interaction
    if cell_mat_interaction is not None:
        cell_mat = cell_mat_interaction
    if D_coeff is not None:
        D = D_coeff
    if cell_chem_interaction is not None:
        chemop = cell_chem_interaction
    if not uniform:
        N = subN[0]+subN[1]+subN[2]
    n = math.floor(N / 6)
    nstep = int(math.floor(tmax / dt))
    diff_cell_cell = npy.repeat(1, N)  ## cell interactions forces
    depant = []
    deppost = []
    depmid = []
    APl = []
    MLl = []

    if not os.path.exists('./trajectories'):
            os.makedirs('./trajectories')

    if not os.path.exists('./final_images'):
            os.makedirs('./final_images')

    for repe in npy.arange(1,nrepet+1,1):
        
        num = 0
        ### Variables
        x = npy.zeros( (nstep,N) )
        y = npy.zeros( (nstep,N) )
        theta = npy.zeros( (nstep,N) )

        ### Create matrice
        if shape == 'quadratic':
            xmat = npy.linspace(- 1.5,1.5,1200)
            ymat = matrice(xmat,'quadratic',0)
        if shape == 'cylindric':
            ymat = npy.r_[ npy.linspace(-4,yecm+xecm,1200/2), (npy.linspace(-4,yecm+xecm,1200/2))[::-1] ]
            xmat = matrice(ymat,'cylindric',0)

        ### Initial values
        if shape == 'cylindric':
            N1 = N*5/6/2
            N2 = N-(N1*2)
            ang = npy.linspace(0, math.pi, N2)
            ang = ang + npy.random.normal(0, 2.0/N, N2)
            r1 = npy.random.normal(0, 4.0/N, N1)
            r2 = npy.random.normal(0, 4.0/N, N1)
            y[0,] = npy.r_[npy.linspace(-3.8,yecm,N1)+r1, (xecm+d_eq/2.0)*npy.sin(ang) + yecm, npy.linspace(-3.8,yecm,N1)+r2]
            #y[0,] = y[0,]
            [ dx, dy ] = dematrice( y[0,], shape, d_eq/2, N)
            x[0,] = npy.copy(dx)
            y[0,] = npy.copy(dy)
        if shape == 'quadratic':
            if uniform == 1:
                ynew = npy.r_[ npy.linspace(-3.8,3.9,math.floor(N/2)), npy.linspace(-3.8,3.9,math.floor(N/2)) ]
                limH = N/2
            else:
                ## n0 ant, n1 mid, n2 pos
                if subN[0]/2 <= 3:
                    ant = npy.r_[ npy.random.uniform(antlim,3.9, int(subN[0]/2))] 
                else:
                    ant = npy.r_[ npy.linspace(antlim,3.9, int(subN[0]/2))] 
                if subN[1]/2 <= 3:
                    mid = npy.r_[ npy.random.uniform(postlim, antlim, int(subN[1]/2)) ]
                else:
                    mid = npy.r_[ npy.linspace(postlim, antlim, int(subN[1]/2)) ]
                
                if subN[2]/2 <= 3:
                    post = npy.r_[ npy.random.uniform(-3.8, postlim, int(subN[2]/2)) ]
                else:
                    post = npy.r_[ npy.linspace(-3.8, postlim, int(subN[2]/2)) ]
                ynew = npy.r_[ant, mid, post]
                limH = (subN[0]/2+subN[1]/2+subN[2]/2)
                
                nant = int(subN[0] - subN[0]/2)
                if nant <= 3:
                    ant = npy.r_[ npy.random.uniform(antlim, 3.9, nant) ]
                else:
                    ant = npy.r_[ npy.linspace(antlim, 3.9, nant) ]
                
                nmid = int(subN[1] - subN[1]/2)
                if nmid <= 3:
                    mid = npy.r_[ npy.random.uniform(postlim, antlim, nmid) ]
                else:
                    mid = npy.r_[ npy.linspace(postlim, antlim, nmid) ]
                
                npost = int(subN[2] - subN[2]/2)
                if npost <= 3:
                    post = npy.r_[ npy.random.uniform(-3.8, postlim, npost) ]
                else:
                    post = npy.r_[ npy.linspace(-3.8, postlim, npost) ]
                
                ynew = npy.r_[ynew, ant, mid, post]
            
            r = npy.random.normal(0,3.0/N,N)
            ynew = ynew + r
            [ dx, dy ] = dematrice( ynew, shape, d_eq/2, N, limH)
            x[0,] = npy.copy(dx)
            y[0,] = npy.copy(dy)
        
        theta[0,] = npy.random.uniform(-1,1,N) * math.pi
        #theta[0,] = math.pi/2;

        ## Assign the colors: -2<y<0 cyan, 0<y<2 blue, 2<y<4 dark blue
        # blue: 001, ant,3 = 0.5; post,2 = 1
        # green: 010, ant,1=0.6, ant,3=0.6, psot,2=0.75
        #red: 100, ant,1=0.7, ant,2=0.2, ant,3=0.2, post,2=0.55, post,3=0.55
        anterior = y[0,] > antlim
        posterior = y[0,] < postlim
        middle = ( y[0,] >= postlim) & ( y[0,] <= antlim )

        #cols = npy.array( [colmid] * N, dtype="S32" )
        cols = npy.array( [colmid] * N )
        cols[anterior] = colant
        cols[posterior] = colpos

        # if difference of adhesion
        diff_cell_cell[anterior] = 0.5
        diff_cell_cell[posterior] = 0.5
        diff_cell_cell[middle] = 2

        nframe=1
        halft = 1
        
        ## initialize if all matrix point
        nmat = 0
        if all_matrix_chemo == 1:
            nx = 50
            ny = 100
            dy = yecm*2/ny
            ys = -yecm
            xs = -xecm*1.5
            for xind in range(nx):
                xs = xs + dy
                ys = -yecm
                for yind in range(ny):
                    ys = ys + dy
                    if insidematricePt( xs, ys, shape, 0 ):
                        nmat = nmat + 1

        #### Time loop
        for time in npy.arange(1,nstep,1):
            time_step(time)
            if ( time == 1 ):
                plotte_traj( x, y, cols, xmat, ymat, chemo, time, 'final_images/traj_tStart'+extension)
            if (halft == 1) & (time >= nstep/2):
                halft = 0
                plotte_traj( x, y, cols, xmat, ymat, chemo, time, 'final_images/traj_tHalfTime'+extension)
        
        if make_movie == 1:
            make_movie_with_imageio()
        
        if 1:
            plotte_traj(x, y, cols, xmat, ymat, chemo, time, str('final_images/traj_tFinal'+extension))
            plot_track(x[:,anterior], y[:,anterior], cols[anterior], 'final_images/tracks_anterior'+extension)
            plot_track(x[:,posterior], y[:,posterior], cols[posterior], 'final_images/tracks_posterior'+extension)
            plot_track(x[:,middle], y[:,middle], cols[middle], 'final_images/tracks_middle'+extension)
            save_trajectory( x, y, npy.arange(1,nstep,1), repe)
        
        dep = deplacement(x,y)
        depant = npy.r_[depant, npy.mean(dep[anterior])]
        deppost = npy.r_[deppost, npy.mean(dep[posterior])]
        depmid = npy.r_[depmid, npy.mean(dep[middle])]
        bbox = bounding_box(x,y)
        MLl = npy.r_[MLl, bbox[0], bbox[1]]
        APl = npy.r_[APl, bbox[2], bbox[3]]


if __name__ == "__main__":
    main_function(cell_cell, cell_mat, D, chemop)
