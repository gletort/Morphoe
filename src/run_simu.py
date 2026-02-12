"""
Marimo interface to run Morphoe simulations: choose parameters, create simulation folder, save param file in it and run it
"""

import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium", layout_file="layouts/run_simu.grid.json")


@app.cell
def _():
    import marimo as mo
    from marimo import ui as moui
    return mo, moui


@app.cell
def _(mo):
    mo.md("""#MORPHOE: MORPHogenesis of Olfactory Epithelium""")
    return


@app.cell
def __():
    def parameter_line( text, para, descr ):
        """ Write a line with parameter name, parameter UI, small description """
        text = text + f" &nbsp; { para }  &nbsp; <span style=\"color:grey\"> *" + descr +"*</span>  \n"
        text = text + "\n"
        return text
    def double_parameter_line( text, paraa, textb, parab, descr):
        """ Two parameters in the same line """
        text = text + f" &nbsp; { paraa }"+textb+f"{parab}  &nbsp; <span style=\"color:grey\"> *" + descr +"*</span>  \n"
        text = text + "\n"
        return text
    return double_parameter_line, parameter_line


@app.cell
def __(mo):
    mo.md("""##Simulation setup""")
    return


@app.cell
def __(mo):
    mo.md("""Simulation status:""")
    return


@app.cell
def _(double_parameter_line, mo, moui, parameter_line):
    ### Proposes all parameters
    parameters = {}

    ## initial configuration
    parameters["N"] = moui.slider( 6, 320, 6, 60, show_value=True )
    parameters["subN"] = moui.text("[4,14,14]")
    parameters["uniform"] = moui.checkbox( True )

    init_config = ""+parameter_line("Nb of cells", parameters["N"], "Total number of cells simulated")     
    init_config += ""+parameter_line("Uniform initial distribution", parameters["uniform"], "Randomly place the cells with a similar distribution along the y-axis")
    init_config += ""+parameter_line("For non uniform, precise the distribution as [anterior, middle, posterior] :", parameters["subN"], "For a non uniform distribution, precise the number of cells in each compartements: anterior, middle and posterior" )

    ## Ecm shape
    parameters["shape"] = moui.dropdown(options=["quadratic", "cylindric"], value="quadratic")
    parameters["xecm"] = moui.number(-6,20,0.1, 1.0)
    parameters["yecm"] = moui.number(-6,20,0.1, 3.8)
    ecm_config = ""+parameter_line("Matrix shape", parameters["shape"], "Mathematical shape of the horse-shoe like of the matrix")
    ecm_config += double_parameter_line("Coordinates: x",parameters["xecm"], ", y", parameters["yecm"], "Coordinates of the matrix remarkable point (quadratic equation)")

    ## simu configuration
    parameters["dt"] = moui.number(0.0000001, 1, 0.00000001, 0.0005)
    parameters["tmax"] = moui.slider(1,50,0.1,6, show_value=True)
    parameters["make_movie"] = moui.checkbox( True )
    parameters["mfreq"] = moui.number(0,2000,1,200)
    parameters["dataFreq"] = moui.number(0,2000,1,10)
    parameters["nrepet"] = moui.slider(0,100,1,1, show_value=True)
    parameters["extension"] = moui.dropdown(options=[".png", ".svg"], value=".png")
    parameters["name"] = moui.text("default")
    simu_config = ""
    simu_config += parameter_line("Simulation name: ", parameters["name"], "Give a name to the current simulation. A folder with this name will be created")
    simu_config += parameter_line("Time step: ", parameters["dt"], "Simulation time step: interval between each calculated time")
    simu_config += parameter_line("Saving cell position frequency: ", parameters["dataFreq"], "Save simulation state of cells positions every n steps")
    simu_config += parameter_line("Final time: ", parameters["tmax"], "Simulation final time")
    simu_config += parameter_line("Generate movie", parameters["make_movie"], "Create a movie at the end of the simulation with all the saved time steps")
    simu_config += parameter_line("Saving movie image frequency: ", parameters["mfreq"], "Save simulation plot for the movie every n steps")
    simu_config += parameter_line("Image extension: ", parameters["extension"], "Choose the extension type for the saved images")
    simu_config += parameter_line("Repeat simulation", parameters["nrepet"], "Do n simulations with the same parameter set") 

    ## chemotaxis parameters
    parameters["chemop"] = moui.number(0,20,0.00001,2)
    parameters["chemoline"] = moui.number(0,20,0.001,0.02)
    parameters["chem_source"] = moui.dropdown(options=["Point source", "Vertical line", "Horizontal line", "All matrix"], value="Point source")
    # parameters["all_matrix_chemo"] = moui.checkbox(False)
    # parameters["central_point_source"] = moui.checkbox(True)
    # parameters["line_source"] = moui.dropdown(options=["No", "Vertical line", "Horizontal line"], value="No")
    parameters["xyline"] = moui.slider(-2,2,0.1,0, show_value=True)
    parameters["ysource"] = moui.slider(-2.5,4,0.1,0, show_value=True)
    parameters["chemo_cte"] = moui.slider(0,10,0.05,0.5, show_value=True)
    chemo_config = parameter_line("Chemotaxis force: ", parameters["chemop"], "Strength of chemotaxis attraction on cells")
    chemo_config += parameter_line("Chemotaxis line force:", parameters["chemoline"], "Strength of chemotaxis attraction on cells when using a line source")
    chemo_config += parameter_line("Type of chemotaxis source", parameters["chem_source"], "Define the type of chemotaxis source")     
    # chemo_config += parameter_line("Use all matrix as chemo source", parameters["all_matrix_chemo"], "All points inside the matrix are chemotaxis source")
    # chemo_config += parameter_line("Chemotaxis source as a central point", parameters["central_point_source"], "Use only a point as chemotaxis source")
    # chemo_config += parameter_line("Line source", parameters["line_source"], "Use a line as chemotaxis source instead of a point. Choose its direction")
    chemo_config += parameter_line("Line position", parameters["xyline"], "Set the position of the line along the corresponding axis")
    chemo_config += parameter_line("Point Y position", parameters["ysource"], "Position of the point source of chemo along the Y axis")
    chemo_config += parameter_line("Constant chemotaxis:", parameters["chemo_cte"], "if >0, consider the chemotaxis force to be the same wherever the cell is. Otherwise, it depends on the distance between the cell and the chemotaxis source.")

    ## cell parameters
    cell_config = ""
    parameters["cell_cell"] = moui.slider(0,20,0.1,0.7, show_value=True)
    cell_config += parameter_line("Strength of cell-cell interaction", parameters["cell_cell"], "Amplitude of force of attraction/repulsion between neighboring cells (within interaction threshold)")
    parameters["cell_mat"] = moui.slider(0,20,0.25,4, show_value=True)
    cell_config += parameter_line("Strength of cell-matrix interaction", parameters["cell_mat"], "Amplitude of force of attraction/repulsion between a cell and neighboring matrix (within interaction threshold)")

    parameters["d_interaction"] = moui.slider(0, 20, 0.25, 1, show_value=True)
    cell_config += parameter_line("Interaction distance", parameters["d_interaction"], "Threshold distance for cell to interact with another cell/matrix")
    parameters["d_eq"] = moui.slider(0, 20, 0.25, 0.5, show_value=True)
    cell_config += parameter_line("Cell diameter", parameters["d_eq"], "Equilibrium distance between two cells: ~ cell diameter")
    parameters["out"] = moui.number(0,1000,0.5,100)
    cell_config += parameter_line("matrix inpenetrability", parameters["out"], "Strongly eject cell out of matrix if they enter it")
    parameters["D"] = moui.number(0.00001, 5, 0.00001, 0.001)
    cell_config += parameter_line("Amplitude of random motion", parameters["D"], "Strength of the random motion component of each cell")
    parameters["tau"] = moui.number(0.1, 100, 0.1, 10)
    cell_config += parameter_line("Persistence coefficient", parameters["tau"], "Persistence of motion coefficient (memory of past motion due to cell polarity)")
    parameters["v0"] = moui.number(0.001, 100, 0.001, 0.1)
    cell_config += parameter_line("Amplitude of polarized motion", parameters["v0"], "Strength of directed motion, directed by cell polarization")

    extra_options = ""
    parameters["push"] = moui.number(0,20,0.25,0)
    extra_options += parameter_line("Vertical shift", parameters["push"], "Amplitude of motion towards the top (0: non active)")
    parameters["d_cell_cell"] = moui.checkbox(False)
    extra_options += parameter_line("Heterogenous cell-cell interactions", parameters["d_cell_cell"], "To use cell that have different interaction strenghts (for different cell types)")
    parameters["d_cell_mat"] = moui.checkbox(False)
    extra_options += parameter_line("Heterogenous cell-ECM interactions", parameters["d_cell_mat"], "To use cell that have different interaction strenghts with the matrix (for different cell types)")
    parameters["no_ecm_adhesion"] = moui.checkbox(False)
    extra_options += parameter_line("Non adherent cells", parameters["no_ecm_adhesion"], "Cells don't adhere to the ECM") 
    parameters["inhibition_zones"] = moui.checkbox(False)
    extra_options += parameter_line("Add zone of inhibition", parameters["inhibition_zones"], "Add a repulsive zone")
    parameters["inh_min"] = moui.number(-10,10,0.5,-1.5)
    extra_options += parameter_line("Inhibition zone min", parameters["inh_min"], "If there is an inhibition zone, lower limit in the Y-axis of this zone")
    parameters["inh_max"] = moui.number(-10,10,0.5,1.5)
    extra_options += parameter_line("Inhibition zone max", parameters["inh_max"], "If there is an inhibition zone, upper limit in the Y-axis of this zone")
    parameters["inh_coeff"] = moui.number(0,20,0.5,0.5)
    extra_options += parameter_line("Inhibition coefficient", parameters["inh_coeff"], "If there is inhibition, strength of the repulsion")

    ## display para
    display_cfg = ""
    parameters["antlim"] = moui.number(-20,20,0.5,1.5)
    display_cfg += parameter_line("Limit of anterior cells", parameters["antlim"], "Display cells as anterior if they were above this limit initially")
    parameters["postlim"] = moui.number(-20,20,0.5,-1.5)
    display_cfg += parameter_line("Limit of posterior cells", parameters["antlim"], "Display cells as posterior if they were below this limit initially")
    parameters["colant"] = moui.text("(0.3,0.85,0.9,1)")
    display_cfg += parameter_line("Color of anterior cells", parameters["colant"], "Display color of anterior cells, as (r,g,b, transparency), each value between 0 and 1")
    parameters["colmid"] = moui.text("(0.25,0.3,0.97,1)")
    display_cfg += parameter_line("Color of middle cells", parameters["colmid"], "Display color of middle cells, as (r,g,b, transparency), each value between 0 and 1")
    parameters["colpos"] = moui.text("(0.1,0.1,0.5,1)")
    display_cfg += parameter_line("Color of posterior cells", parameters["colpos"], "Display color of posterior cells, as (r,g,b, transparency), each value between 0 and 1")

    parameter_interface = mo.accordion(
        {
            "**Cell parameters**": mo.md( f""" {cell_config} """),
            "**Chemotaxis parameters**": mo.md( f""" {chemo_config} """),
            "**Matrix shape**": mo.md( f""" {ecm_config}   """),
            "**Initial configuration**": mo.md( f""" {init_config} """ ),
            "**Simulation configuration**": mo.md( f""" { simu_config } """), 
            "**Display parameters**": mo.md( f""" { display_cfg } """), 
            "**Extra options**": mo.md( f""" { extra_options } """), 

        }
    )
    return (
        cell_config,
        chemo_config,
        display_cfg,
        ecm_config,
        extra_options,
        init_config,
        parameter_interface,
        parameters,
        simu_config,
    )


@app.cell
def __(parameter_interface):
    parameter_interface
    return


@app.cell
def __(bouton):
    bouton
    return


@app.cell
def _(mo):
    # Lancer le code avec les paramètres et afficher les résultats
    bouton = mo.ui.run_button(label="Start simulation")
    return (bouton,)


@app.cell
def _(__file__, bouton, mo, os, parameters):
    main = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    os.chdir(main)
    simu_name = None

    with mo.redirect_stdout():
        if bouton.value:
            print("Simulation status:")
            simu_name = parameters["name"].value
            print("Creating simulation: "+simu_name)
            simdir = os.path.join("simus", simu_name)
            if not os.path.exists(simdir):
                os.makedirs(simdir)
            parapath = os.path.join( simdir, "params.py")
            with open(parapath, 'w') as parfile:
                parfile.write("## Parameters file for simulation "+simu_name+"\n")
                for paraname, paraval in parameters.items():
                    # special case: Chemotaxis source
                    if paraname == "chem_source":
                        if paraval.value == "Point source":
                            parfile.write('all_matrix_chemo = 0'+'\n')
                            parfile.write('central_point_source = 1'+'\n')
                            parfile.write('line_source = 0'+'\n')
                        elif paraval.value == "Vertical line":
                            parfile.write('all_matrix_chemo = 0'+'\n')
                            parfile.write('central_point_source = 0'+'\n')
                            parfile.write('line_source = 1'+'\n')
                            parfile.write('dxyline = 1'+'\n')
                        elif paraval.value == "Horizontal line":
                            parfile.write('all_matrix_chemo = 0'+'\n')
                            parfile.write('central_point_source = 0'+'\n')
                            parfile.write('line_source = 2'+'\n')
                            parfile.write('dxyline = 1'+'\n')
                        elif paraval.value == "All matrix":
                            parfile.write('all_matrix_chemo = 1'+'\n')
                            parfile.write('central_point_source = 0'+'\n')
                            parfile.write('line_source = 0'+'\n')
                            parfile.write('line_source = 0'+'\n')
                        val = paraval.value
                        val = "\""+str(val)+"\""
                        parfile.write(paraname+" = "+val+'\n')
                        continue
                    if paraname == "subN":
                        val = paraval.value
                        parfile.write(paraname+" = "+val+'\n')
                        continue
                    if paraname.startswith("col"):
                        val = paraval.value
                        parfile.write(paraname+" = "+val+'\n')
                        continue
                    ## other cases
                    val = paraval.value
                    if type(val) is str:
                        val = "\""+str(val)+"\""
                    if type(val) is int:
                        val = str(val)
                    if type(val) is float:
                        val = str(val)
                    if type(val) is bool:
                        if val:
                            val = "1"
                        else:
                            val = "0"
                    parfile.write(paraname+" = "+val+'\n')
            print("Parameter file written in "+str(simdir))

    if bouton.value:
        os.chdir(simdir)
        import eon
        import importlib
        importlib.reload(eon)
        from eon import main_function

        with mo.redirect_stdout():
            print("Starting simulation...")
            main_function()

        os.chdir(main)
    return (
        eon,
        importlib,
        main,
        main_function,
        paraname,
        parapath,
        paraval,
        parfile,
        simdir,
        simu_name,
        val,
    )


@app.cell
def __(mo):
    btn_plot = mo.ui.run_button(label="Update output")
    btn_plot
    return (btn_plot,)


@app.cell
def __(mo):
    post_plot = mo.ui.run_button(label="Update post-process plots")
    post_plot
    return (post_plot,)


@app.cell
def __(bouton, btn_plot, mo, os, parameters):
    if btn_plot.value or bouton.value:
        plot_fold0 = os.path.join("simus", parameters["name"].value, "final_images")
        plot0 = mo.output.replace(mo.md("**Initial time**"))
        plot0 = mo.output.append( mo.image(os.path.join(plot_fold0, "traj_tStart"+parameters["extension"].value)))
    else:
        plot0=None
    plot0
    return plot0, plot_fold0


@app.cell
def __(btn_plot, mo, os, parameters):
    if btn_plot.value:
        plot_fold1 = os.path.join("simus", parameters["name"].value, "final_images")
        plot1 = mo.output.replace(mo.md("**Half time**"))
        plot1 = mo.output.append( mo.image(os.path.join(plot_fold1, "traj_tHalfTime"+parameters["extension"].value)))
    else:
        plot1=None
    plot1
    return plot1, plot_fold1


@app.cell
def __(btn_plot, mo, os, parameters):
    if btn_plot.value:
        plot_fold = os.path.join("simus", parameters["name"].value, "final_images")
        plot2 = mo.output.replace(mo.md("**Final time**"))
        plot2 = mo.output.append( mo.image(os.path.join(plot_fold, "traj_tFinal"+parameters['extension'].value)))
    else:
        plot2=None
    plot2
    return plot2, plot_fold


@app.cell
def _(mo):
    quit_button = mo.ui.run_button(label="Shut down the kernel (before closing)")
    quit_button
    return (quit_button,)


@app.cell
def _(quit_button):
    import os
    if quit_button.value:
        os._exit(0)
    return (os,)


@app.cell
def __(mo):
    mo.md("""--- \n #Post-processing""")
    return


@app.cell
def __(moui):
    post_dir = moui.file_browser( "simus", selection_mode="directory", multiple=False, label="Choose simulation to post-process" )
    post_dir
    return (post_dir,)


@app.cell
def __(moui):
    post_go = moui.run_button(label="Postprocess selected simulation")
    post_go
    return (post_go,)


@app.cell
def __(mo, post_dir, post_go):
    with mo.redirect_stdout():
        if post_go.value:
            postsimdir = str(post_dir.path(index=0))
            print("Postprocessing simulation:"+postsimdir)
            from postprocess import postprocess_simu
            postprocess_simu(postsimdir)
    return postprocess_simu, postsimdir


@app.cell
def __(mo, os, post_dir, post_plot, parameters):
    if post_plot.value:
        postdir = str(post_dir.path(index=0))
        plot_ant = os.path.join( postdir, "post_process" )
        plotant = mo.output.replace(mo.md("**Mean tracks**"))
        plotant = mo.output.append( mo.image(os.path.join(plot_ant, "pool_meantracks"+parameters["extension"].value)))
    else:
        plotant=None
    plotant
    return plot_ant, plotant, postdir


@app.cell
def __(mo, os, plot_ant, post_plot, postdir, parameters):
    if post_plot.value:
        plot_ap = os.path.join( postdir, "post_process" )
        plotap = mo.output.replace(mo.md("**Anterior-Posterior Length**"))
        plotap = mo.output.append( mo.image(os.path.join(plot_ant, "AP_size_evolution"+parameters["extension"].value)))
    else:
        plotap=None
    plotap
    return plot_ap, plotap


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
