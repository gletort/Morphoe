
### Parameters
N = 60  ## nb cells, /6
uniform = 1  ## uniform distribution of initial cells
subN = [4,14,14]  ## if not uniform only
dt = 0.0005 ## time step
tmax = 6 # 7    ## simu time

chemop = 2 #2 #2    ## ampltiude of chemo force
chemoline = 0.02  ## amplitude of chemo for lines
D = 0.001      ## amplitude of random motion
v0 = 0.1     ## amplitude of polarized motion
tau = 10     ## persistence coefficient (memory of past motion)

d_interaction = 1  ## threshold distance to interact
d_eq = 0.5           ## equilibrium dist between cells ~ diameter
cell_cell = 0.7      ## amplitude of cell-cell interactions
cell_mat = 4         ## amplitude of cell-matrix interaction
out = 100            ## coefficient of rep if cell is inside matrix

push = 0

# options
neurogenine_mutant = 0   ## neurogenine mutant: chemo 0 from 0, nstep/2
d_cell_cell = 0          ## cell-cell interactions of different values
d_cell_mat = 0           ## if cell-matrix interactions of diffrent values
no_ecm_adhesion = 0      ## if 1: mutant, cells cannot adhtere to matrix
all_matrix_chemo = 0     ## all matrix (encephale) is source of chemo-attract

central_point_source = 1  ## positive if central point of matrix is source
repulsion_sources = 0    ## add repulsive sources instead of chemo attractive source
line_source = 0         ## vertical source 1, 2 horizontal source
yline  = 0              ## position of horizontal line source
ysource  = 0              ## position of horizontal line source
chemo_cte = 0 #0.5          ## chemotaxis force doesn't depend on distance to the source (cte gradient)

# if repulsion sources, position of the 2 sources
source1x = 0
source1y = 3.8
source2x = -1.25
source2y = -3.8
source3x = 1.25
source3y = -3.8
inhibition_zones = 0     ## if add inhibition zones or not
inh_min = -1.5
inh_max = 1.5
inhib_coeff = 0.5

shape = 'quadratic' ## encephale shape (quadratic~parabole, cylindric)
yecm = 3.8          #3.8 quad, 3 cyl
xecm = 1.0          #1
antlim = 1.5        ## limit ot consider cell as anterior
postlim = -1.5
colant = (0.3,0.85,0.9,1) #"mediumturquoise"
colmid = (0.25, 0.3,0.97,1) #"midnightblue"
colpos = (0.1,0.1,0.5,1) 

make_movie = 1     ## save movie
mfreq = 200        ## frequency of saving image
nrepet = 2        ## nb de repetition (n+1)
dataFreq = 50      ## frequency of saving data point