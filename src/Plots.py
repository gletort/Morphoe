import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import pathlib
import numpy as npy
import random 

import importlib
import Matrix
importlib.reload(Matrix)
from Matrix import *

sys.path.append(".")
extension = ".png"
import params 
importlib.reload(params)
from params import *


def bfig():
    """ Create figure """
    fig = plt.figure(dpi=300)

def efig_all( filename, sh ):
    """ save figure """
    fig = plt.gcf()
    fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9 )
    fig.tight_layout()
    plt.xlim(-4,5)
    plt.ylim(-4,5)
    if filename.endswith(".svg"):
        fig.savefig( filename, bbox_inches="tight", format="svg" )
    else:
        fig.savefig( filename, bbox_inches="tight" )
    if sh:
        print(''+filename+' saved')
    elif 'traj' not in filename:
        pass
    else:
        plt.gca().set_aspect('equal')
        plt.show(block=False)
        plt.pause(3)
    plt.close(fig)

def efig( filename, sh ):
    """ save figure """
    fig = plt.gcf()
    fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9 )
    fig.tight_layout()
    if filename.endswith(".svg"):
        fig.savefig( filename, bbox_inches="tight", format="svg" )
    else:
        fig.savefig( filename, bbox_inches="tight" )
    if sh:
        print(''+filename+' saved')
    else:
        plt.gca().set_aspect('equal')
        plt.show(block=False)
    plt.close(fig)
    
def plotte_traj(x, y, colors, xmat, ymat, chemo, time, name, msize=7, linew=2):
    """ plot cell trajectories """
    rad = d_eq/2
    # bfig()
    fig = plt.gcf()
    ax = fig.gca()
    for i in range(len(x[0,])):
        plt.plot( x[0,i], y[0,i], mfc='none', mec="black", marker="o", markersize=msize )
        plt.plot( x[range(time),i], y[range(time),i], color=colors[i], linestyle="-", linewidth=linew )
        circ = plt.Circle( (x[time,i],y[time,i]), rad, color=colors[i], fill=True )
        ax.add_artist(circ)
        ax.yaxis.tick_left()
        ax.xaxis.tick_bottom()

    if no_ecm_adhesion <= 0:
        plt.plot( xmat, ymat, color="black", linestyle="-" )
    else:
        plt.plot( xmat, ymat, color="black", linestyle="--" )

    #print(all_matrix_chemo)
    if chemo > 0:
        
        ## take all matrix point
        if all_matrix_chemo == 1:
            nx = 50
            ny = 100
            dy = yecm*2/ny
            ys = -yecm
            xs = -xecm*1.5
            chem = chemo
            for xind in range(nx):
                xs = xs + dy
                ys = -yecm
                for yind in range(ny):
                    ys = ys + dy
                    if insidematricePt( xs, ys, shape, 0 ) > 0:
                        plt.plot( xs, ys, color="black", marker="^", markersize=2 )
            
        if line_source > 0:
            ## vertical line
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
                            plt.plot( xl, ys, color="black", marker="^", markersize=8 )
            ## horizontal line
            if line_source == 2:
                ny = 8
                yinf = xyline-dxyline/2
                ysup = xyline+dxyline/2
                for yind in range(ny):
                    yl = yinf + (ysup-yinf)*yind/ny
                    nx = 50
                    xs = -xmatricepoint(yl, shape)
                    dx = abs(xs)*2/nx
                    for xind in range(nx):
                        xs = xs + dx
                        plt.plot( xs, yl, color="black", marker="^", markersize=8 )

                #if line_source <=0:
                #    plt.plot( source1x, source1y, color="black", marker="^", markersize=10 )
                #    plt.plot( source2x, source2y, color="black", marker="^", markersize=10 )
                 #   if repulsion_sources >= 2:
                  #      plt.plot( source3x, source3y, color="black", marker="^", markersize=10 )
        if central_point_source>0:
            plt.plot( 0, ysource, color="black", marker="*", markersize=15 )

    pr = 1
    if name == 'traj_half'+extension:
        pr = 1-show_inter
    if name == 'traj'+extension:
        pr = 1-show_inter
    efig_all(name, pr)
    plt.close()


def plot_track(x,y, colors, name):
    bfig()
    for i in range(len(x[0,])):
        if npy.mean(x[:,i]) < x[0,i]:
            x[:,i] = -x[:,i]
        x[:,i] = x[:,i] - x[0,i]
        y[:,i] = y[:,i] - y[0,i]
        n = len(x[:,i])
        plt.plot( x[1:math.floor(n/2),i], y[1:math.floor(n/2),i], linestyle="-", color=colors[i] )
        plt.plot( x[math.floor(n/2):,i], y[math.floor(n/2):,i], linestyle="-", color='grey' )
    
    plt.axhline( 0, color="black" )
    plt.axvline( 0, color="black" )
    efig_all(name, 1)
    plt.close()

def plot_some_track(track, xs, ys, col, name, ntrack):
    bfig()
    utrack = list(npy.unique(track))
    ktrack = random.sample( utrack, ntrack)

    for t in ktrack:
        keep = [ i for i in range(len(track)) if track[i]==t ]
        
        x = xs[keep]
        y = ys[keep]
        if npy.mean(x) < x[0]:
            x = -x
        x = x - x[0]
        y = y - y[0]
        
        n = len(x)
        plt.plot( x[1:math.floor(n/2)], y[1:math.floor(n/2)], linestyle="-", color=col, linewidth=2.5 )
        plt.plot( x[math.floor(n/2):], y[math.floor(n/2):], linestyle="-", color='grey', linewidth=2.5 )
    
    plt.axhline( 0, color="black" )
    plt.axvline( 0, color="black" )
    efig_all(name, 1)
    plt.close()

def plot_mean_track(mtrackx, mtracky, col, mtrackpx, mtrackpy, colp, mtrackmx, mtrackmy, colm, name):
    bfig()

    x = mtrackx #- mtrackx[0]
    y = mtracky #- mtracky[0]
    n = len(x)
    lw = 5
    plt.plot( x[1:math.floor(n/2)], y[1:math.floor(n/2)], linestyle="-", linewidth=lw, color=col )
    plt.plot( x[math.floor(n/2):], y[math.floor(n/2):], linestyle="-", linewidth=lw, color='grey' )
    
    x = mtrackpx #- mtrackpx[0]
    y = mtrackpy #- mtrackpy[0]
    n = len(x)
    plt.plot( x[1:math.floor(n/2)], y[1:math.floor(n/2)], linestyle="-", linewidth=lw, color=colp )
    plt.plot( x[math.floor(n/2):], y[math.floor(n/2):], linestyle="-", linewidth=lw, color='grey' )
    
    x = mtrackmx #- mtrackmx[0]
    y = mtrackmy #- mtrackmy[0]
    n = len(x)
    plt.plot( x[1:math.floor(n/2)], y[1:math.floor(n/2)], linestyle="-", linewidth=lw, color=colm )
    plt.plot( x[math.floor(n/2):], y[math.floor(n/2):], linestyle="-", linewidth=lw, color='grey' )
    
    plt.axhline( 0, color="black" )
    plt.axvline( 0, color="black" )
    
    # plt.show()
    fig = plt.gcf()
    fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9 )
    fig.tight_layout()
    plt.xlim(-0.1,0.7)
    plt.ylim(-3,3)
    fig.savefig( name, bbox_inches="tight" )
    print(''+name+' saved')
    plt.close()

def plot_time_bb(time, height, filename="post_process/AP_size_evolution"+extension):
    bfig()
    xtime = []
    ystd = []
    ymean = []
    maxt = npy.max(npy.unique(time))
    for t in npy.unique(time):
        keep = npy.where(time==t)[0]
        ystd.append(npy.std(height[keep]))
        ymean.append(npy.mean(height[keep]))
        xtime.append(t/maxt)
    plt.errorbar(xtime, ymean, yerr=ystd)
    efig(filename, 1)
    plt.close()
    plotdata = npy.column_stack((xtime, ymean, ystd))
    outname = "post_process/AP_size_evolution.csv"
    with open(outname, 'w+') as fileid:
        npy.savetxt(fileid, plotdata, header="Time\tMean\tStd", delimiter="\t")
        fileid.close()

def boxstrip( x, ys, nc, mycol, filename='boxplot'+extension, yl=1, xname='', yname='', intitle='', splot=111):
    """ 
	boxplot + stripchart of ys sort by x 
		n : number of ys bar to plot
		x : names of the categories
		ys: list of ys values
    """

    bfig()
    plt.subplot(splot)
    mywidth = npy.repeat( 0.75, nc )
    bp = plt.boxplot(ys, widths=mywidth)
    plt.ylim(0,yl)
    for element in bp['medians']:
        element.set_color('grey')
        element.set_linewidth(5)
    for element in bp['boxes']:
        element.set_color('grey')
        #element.set_facecolor('yellow')
        element.set_linewidth(3)
        element.set_linestyle('solid')
	    #element.set_fill(True)
	    #element.set_hatch('/')
    for element in bp['whiskers']:
        element.set_color('grey')
        element.set_linewidth(3)
    for element in bp['caps']:
        element.set_color('grey')
    for i in range(nc):
        ycur = ys[i]
        xcur = npy.random.normal(i+1, 0.2, len(ycur))
        plt.plot(xcur, ycur, mycol[i], ls='None', marker='o', markersize=9)

    plt.xticks([])
    plt.xlabel( xname )
    plt.ylabel( yname )
    plt.locator_params(axis='y', nbins=6)
    plt.title( intitle )
    efig(filename, 1)
    plt.close()

def make_movie_with_imageio(folder='final_images', prefix="image", fps=5):
    folder = pathlib.Path(folder)
    images = sorted(folder.glob(f"{prefix}*"+extension))
    output = folder / "movie.mp4"

    if extension == ".svg":
        print("Warning, cannot create movie with .svg plots")
        return

    writer = imageio.get_writer(output, format='ffmpeg', fps=fps, codec='libx264')
    for img_path in images:
        im = imageio.imread(img_path)
        writer.append_data(im)
    writer.close()

    # Delete images
    for img in images:
        img.unlink()

    print("Movie saved :", output)
