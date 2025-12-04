# Generated with SMOP  0.41
from libsmop import *
# matrice.m

    
@function
def matrice(x=None,shape=None,add=None,*args,**kwargs):
    varargin = matrice.varargin
    nargin = matrice.nargin

    ## definition of the "matrix" shape: encephale
    if shape == 'quadratic':
        yecm=4 + add
# matrice.m:4
        xecm=1 + add
# matrice.m:5
        y=multiply(dot(- yecm / (dot(xecm,xecm)),x),x) + yecm
# matrice.m:6
    
    return y
    
if __name__ == '__main__':
    pass
    
