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
    mo.md("""#MORPHogenesis of Olfactory Epithelium""")
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
    ecm_config = ""+parameter_line("ECM shape", parameters["shape"], "Mathematical shape of the horse-shoe like of the ECM")
    ecm_config += double_parameter_line("Coordinates: x",parameters["xecm"], ", y", parameters["yecm"], "Coordinates of the ECM remarkable point (quadratic equation)")

    ## simu configuration
    parameters["dt"] = moui.number(0.0000001, 1, 0.00000001, 0.0005)
    parameters["tmax"] = moui.slider(0,50,0.1,6, show_value=True)
    parameters["make_movie"] = moui.checkbox( True )
    parameters["mfreq"] = moui.number(0,2000,1,200)
    parameters["dataFreq"] = moui.number(0,2000,1,10)
    parameters["nrepet"] = moui.slider(0,100,1,1, show_value=True)
    parameters["name"] = moui.text("default")
    simu_config = ""
    simu_config += parameter_line("Simulation name: ", parameters["name"], "Give a name to the current simulation. A folder with this name will be created")
    simu_config += parameter_line("Time step: ", parameters["dt"], "Simulation time step: interval between each calculated time") 
    simu_config += parameter_line("Final time: ", parameters["tmax"], "Simulation final time")
    simu_config += parameter_line("Saving image frequency: ", parameters["mfreq"], "Save simulation plot every n steps")
    simu_config += parameter_line("Saving data frequency: ", parameters["dataFreq"], "Save simulation state every n steps")
    simu_config += parameter_line("Generate movie", parameters["make_movie"], "Create a movie at the end of the simulation with all the saved time steps")
    simu_config += parameter_line("Repeat simulation", parameters["nrepet"], "Do n simulations with the same parameter set") 

    ## chemotaxis parameters
    parameters["neurogenine_mutant"] = moui.checkbox(False)
    parameters["chemop"] = moui.number(0,20,0.1,2)
    parameters["chemoline"] = moui.number(0,20,0.001,0.02)
    parameters["all_matrix_chemo"] = moui.checkbox(False)
    parameters["central_point_source"] = moui.checkbox(True)
    parameters["repulsion_sources"] = moui.checkbox(False)
    parameters["line_source"] = moui.dropdown(options=["No", "Vertical line", "Horizontal line"], value="No")
    parameters["yline"] = moui.slider(-10,10,0.1,0, show_value=True)
    parameters["ysource"] = moui.slider(-10,10,0.1,0, show_value=True)
    parameters["chemo_cte"] = moui.slider(0,10,0.05,0.5, show_value=True)
    chemo_config = parameter_line("Chemotaxis force: ", parameters["chemop"], "Strength of chemotaxis attraction on cells")
    chemo_config += parameter_line("Chemotaxis line force:", parameters["chemoline"], "Strength of chemotaxis attraction on cells when using a line source")            
    chemo_config += parameter_line("Neurogenine mutant", parameters["neurogenine_mutant"], "Simulate neurogenine mutant: no chemotaxis until half of the simulation when chemotaxis is put back")
    chemo_config += parameter_line("Use all ECM as chemo source", parameters["all_matrix_chemo"], "All points inside the ECM are chemotaxis source")
    chemo_config += parameter_line("Chemotaxis source as a central point", parameters["central_point_source"], "Use only a point as chemotaxis source")
    chemo_config += parameter_line("Use repulsion sources", parameters["repulsion_sources"], "Instead of one attractive source, put two repulsive sources")
    chemo_config += parameter_line("Line source", parameters["line_source"], "Use a line as chemotaxis source instead of a point. Choose its direction")
    chemo_config += parameter_line("Line position", parameters["yline"], "Set the position of the line along the corresponding axis")
    chemo_config += parameter_line("Point Y position", parameters["ysource"], "Position of the point source of chemo along the Y axis")
    chemo_config += parameter_line("Constant chemotaxis:", parameters["chemo_cte"], "if >0, consider the chemotaxis force to be the same wherever the cell is. Otherwise, it depends on the distance between the cell and the chemotaxis source.")

    ## cell parameters
    cell_config = ""
    parameters["cell_cell"] = moui.slider(0,20,0.001,0.7, show_value=True)
    cell_config += parameter_line("Strength of cell-cell interaction", parameters["cell_cell"], "Amplitude of force of attraction/repulsion between neighboring cells (within interaction threshold)")
    parameters["cell_mat"] = moui.slider(0,100,0.01,4, show_value=True)
    cell_config += parameter_line("Strength of cell-ECM interaction", parameters["cell_mat"], "Amplitude of force of attraction/repulsion between a cell and neighboring ECM (within interaction threshold)")

    parameters["d_interaction"] = moui.slider(0, 20, 0.001, 1, show_value=True)
    cell_config += parameter_line("Interaction distance", parameters["d_interaction"], "Threshold distance for cell to interact with another cell/ECM")
    parameters["d_eq"] = moui.slider(0, 20, 0.001, 0.5, show_value=True)
    cell_config += parameter_line("Cell diameter", parameters["d_eq"], "Equilibrium distance between two cells: ~ cell diameter")
    parameters["out"] = moui.number(0,1000,0.5,100)
    cell_config += parameter_line("ECM inpenetrability", parameters["out"], "Strongly eject cell out of ECM if they enter it")
    parameters["D"] = moui.number(0.00001, 5, 0.00001, 0.001)
    cell_config += parameter_line("Amplitude of random motion", parameters["D"], "Strength of the random motion component of each cell")
    parameters["tau"] = moui.number(0.1, 100, 0.1, 10)
    cell_config += parameter_line("Persistence coefficient", parameters["tau"], "Persistence of motion coefficient (memory of past motion due to cell polarity)")
    parameters["v0"] = moui.number(0.001, 100, 0.001, 0.1)
    cell_config += parameter_line("Amplitude of polarized motion", parameters["v0"], "Strength of directed motion, directed by cell polarization")

    extra_options = ""
    parameters["push"] = moui.number(0,20,0.01,0)
    extra_options += parameter_line("Vertical shift", parameters["push"], "Amplitude of motion towards the top (0: non active)")
    parameters["d_cell_cell"] = moui.checkbox(False)
    extra_options += parameter_line("Heterogenous cell-cell interactions", parameters["d_cell_cell"], "To use cell that have different interaction strenghts (for different cell types)")
    parameters["d_cell_mat"] = moui.checkbox(False)
    extra_options += parameter_line("Heterogenous cell-ECM interactions", parameters["d_cell_mat"], "To use cell that have different interaction strenghts with the matrix (for different cell types)")
    parameters["no_ecm_adhesion"] = moui.checkbox(False)
    extra_options += parameter_line("Non adherent cells", parameters["no_ecm_adhesion"], "Cells don't adhere to the ECM") 
    parameters["source1x"] = moui.number(-10,10,0.05,0)
    parameters["source1y"] = moui.number(-10,10,0.05,3.8)
    extra_options += double_parameter_line("Multi-sources, coordinate point 1: x ", parameters["source1x"], ", y ", parameters["source1y"], "If use repulsion sources option, position of the first source")
    parameters["source2x"] = moui.number(-10,10,0.05,-1.25)
    parameters["source2y"] = moui.number(-10,10,0.05,-3.8)
    extra_options += double_parameter_line("Multi-sources, coordinate point 2: x ", parameters["source2x"], ", y ", parameters["source2y"], "If use repulsion sources option, position of the second source")
    parameters["source3x"] = moui.number(-10,10,0.05,1.25)
    parameters["source3y"] = moui.number(-10,10,0.05,3.8)
    extra_options += double_parameter_line("Multi-sources, coordinate point 3: x ", parameters["source3x"], ", y ", parameters["source3y"], "If use repulsion sources option, position of the thrid source")
    parameters["inhibition_zones"] = moui.checkbox(False)
    extra_options += parameter_line("Add zone of inhibition", parameters["inhibition_zones"], "Add a repulsive zone")
    parameters["inh_min"] = moui.number(-10,10,0.05,-1.5)
    extra_options += parameter_line("Inhibition zone min", parameters["inh_min"], "If there is an inhibition zone, lower limit in the Y-axis of this zone")
    parameters["inh_max"] = moui.number(-10,10,0.05,1.5)
    extra_options += parameter_line("Inhibition zone max", parameters["inh_max"], "If there is an inhibition zone, upper limit in the Y-axis of this zone")
    parameters["inh_coeff"] = moui.number(0,20,0.001,0.5)
    extra_options += parameter_line("Inhibition coefficient", parameters["inh_coeff"], "If there is inhibition, strength of the repulsion")

    ## display para
    display_cfg = ""
    parameters["show_inter"] = moui.checkbox(False)
    display_cfg += parameter_line("Show intermediare plot", parameters["show_inter"], "Pops-up a window with current plot")
    parameters["antlim"] = moui.number(-20,20,0.1,1.5)
    display_cfg += parameter_line("Limit of anterior cells", parameters["antlim"], "Display cells as anterior if they were above this limit initially")
    parameters["postlim"] = moui.number(-20,20,0.1,-1.5)
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
            "**Matrix (ECM) shape**": mo.md( f""" {ecm_config}   """),
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
def _(bouton, mo, os, parameters):
    main = os.getcwd()
    simu_name = None

    with mo.redirect_stdout():
        if bouton.value:
            print("Simulation status:")
            simu_name = parameters["name"].value
            print("Creating simulation: "+simu_name)
            simdir = os.path.join("simus", simu_name)
            if not os.path.exists(simdir):
                os.mkdir(simdir)
            parapath = os.path.join( simdir, "params.py")
            with open(parapath, 'w') as parfile:
                parfile.write("## Parameters file for simulation "+simu_name+"\n")
                for paraname, paraval in parameters.items():
                    ## special case: line source
                    if paraname == "line_source":
                        if paraval.value == "No":
                            val = "0"
                        elif paraval.value == "Vertical":
                            val = "1"
                        else:
                            val = "2"
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
        from eon import main_function

        with mo.redirect_stdout():
            print("Starting simulation...")
            main_function()

        os.chdir(main)
    return (
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
def __(bouton, btn_plot, mo, os, parameters):
    if btn_plot.value or bouton.value:
        plot_fold0 = os.path.join("simus", parameters["name"].value, "final_images")
        plot0 = mo.output.replace(mo.md("**Initial time**"))
        plot0 = mo.output.append( mo.image(os.path.join(plot_fold0, "traj_0.png")))
    else:
        plot0=None
    plot0
    return plot0, plot_fold0


@app.cell
def __(btn_plot, mo, os, parameters):
    if btn_plot.value:
        plot_fold1 = os.path.join("simus", parameters["name"].value, "final_images")
        plot1 = mo.output.replace(mo.md("**Half time**"))
        plot1 = mo.output.append( mo.image(os.path.join(plot_fold1, "traj_half.png")))
    else:
        plot1=None
    plot1
    return plot1, plot_fold1


@app.cell
def __(btn_plot, mo, os, parameters):
    if btn_plot.value:
        plot_fold = os.path.join("simus", parameters["name"].value, "final_images")
        plot2 = mo.output.replace(mo.md("**Final time**"))
        plot2 = mo.output.append( mo.image(os.path.join(plot_fold, "traj.png")))
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


if __name__ == "__main__":
    app.run()
