"""
Marimo interface to run Morphoe simulations: choose parameters, create simulation folder, save param file in it and run it
"""

import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from marimo import ui as moui
    return mo, moui


@app.cell
def _(mo):
    mo.md("##MORPHogenesis of Olfactory Epithelium")
    return


@app.cell
def __():
    def parameter_line( text, para, descr ):
        """ Write a line with parameter name, parameter UI, small description """
        text = text + f"{ para } <span style=\"color:lightgrey\"> *" + descr +"*</span>  \n"
        text = text + "\n"
        return text
    def double_parameter_line( text, paraa, textb, parab, descr):
        """ Two parameters in the same line """
        text = text + f"{ paraa }"+textb+f"{parab} <span style=\"color:lightgrey\"> *" + descr +"*</span>  \n"
        text = text + "\n"
        return text
    return double_parameter_line, parameter_line


@app.cell
def _(double_parameter_line, mo, moui, parameter_line):
    ### Proposes all parameters
    parameters = {}

    ## initial configuration
    parameters["Nb"] = moui.slider( 6, 320, 6, 60 )
    parameters["subN"] = moui.text("[4,14,14]")
    parameters["uniform"] = moui.checkbox( True )

    init_config = ""+parameter_line("Nb of cells", parameters["Nb"], "Total number of cells simulated")     
    init_config += ""+parameter_line("Uniform initial distribution", parameters["uniform"], "Randomly place the cells with a similar distribution along the y-axis")
    init_config += ""+parameter_line("For non uniform, precise the distribution as [anterior, middle, posterior] :", parameters["subN"], "For a non uniform distribution, precise the number of cells in each compartements: anterior, middle and posterior" )

    ## Ecm shape
    parameters["shape"] = moui.dropdown(options=["quadratic", "cylindric"], value="quadratic")
    parameters["xecm"] = moui.number(-6,20,0.1, 1.0)
    parameters["yecm"] = moui.number(-6,20,0.1, 3.8)
    ecm_config = ""+parameter_line("ECM shape", parameters["shape"], "Mathematical shape of the horse-shoe like of the ECM")
    ecm_config += double_parameter_line("Coordinates: x",parameters["xecm"], ", y", parameters["yecm"], "Coordinates of the ECM remarkable point (quadratic equation)")
    ## simu configuration
    parameters["dt"] = moui.number(0.0000001, 10, 0.00000001, 0.0005)
    parameters["tmax"] = moui.slider(0,150,0.1,6)
    parameters["make_movie"] = moui.checkbox( True )
    parameters["mfreq"] = moui.number(0,2000,1,200)
    parameters["nrepet"] = moui.slider(0,200,1,2)
    ## chemotaxis parameters
    parameters["neurogenine_mutant"] = moui.checkbox(False)
    parameters["chemop"] = moui.number(0,20,0.1,2)
    parameters["chemoline"] = moui.number(0,20,0.001,0.02)
    parameters["all_matrix_chemo"] = moui.checkbox(False)
    parameters["central_point_source"] = moui.checkbox(True)
    parameters["repulsion_sources"] = moui.checkbox(False)
    parameters["line_source"] = moui.dropdown(options=["No", "Vertical line", "Horizontal line"], value="No")
    parameters["yline"] = moui.slider(-10,10,0.1,0)
    parameters["ysource"] = moui.slider(-10,10,0.1,0)
    parameters["chemo_cte"] = moui.slider(0,10,0.05,0.5)

    #parameters["v0"]
    #parameters["tau"]
    #parameters["D"]
        
    mo.accordion(
        {
            "**Initial configuration**": mo.md( f""" {init_config} """ ),
            "**Matrix (ECM) shape**": mo.md( f""" {ecm_config}   """),
            "**Simulation configuration**": mo.md( f"""
                Time step {parameters["dt"]} \n
                Final time {parameters["tmax"]} \n
                Saving frequency {parameters["mfreq"] } \n
                Generate movie {parameters["make_movie"]} \n
                Repeat simulation {parameters["nrepet"]} 
            """),
               "**Chemotaxis parameters**": mo.md( f"""
                Neurogenine mutant {parameters["neurogenine_mutant"]} <span style="color:lightgrey"> * *</span>\n 
                Chemotaxis force {parameters["chemop"]}  <span style="color:lightgrey"> * *</span>\n 
                Chemotaxis line force {parameters["chemoline"] } <span style="color:lightgrey"> * *</span>\n 
                Use all ECM as chemo source {parameters["all_matrix_chemo"]}  <span style="color:lightgrey"> * *</span>\n 
                Chemotaxis source as a central point {parameters["central_point_source"]}  <span style="color:lightgrey"> * *</span>\n 
            """),
        }
    )


    return ecm_config, init_config, parameters


@app.cell
def __(mo, parameters):
    parameters

    tableau = mo.ui.array([mo.ui.slider(0.35,1.4, label="Coefficient cell_cell", show_value=True, step=0.35/2),
                           mo.ui.slider(2,8, label="Coefficient cell_mat", show_value=True, step=1),
                           mo.ui.slider(0.001,0.009, label="Coefficient diffusion D", show_value=True, step=0.001),
                           mo.ui.slider(0,1, label="Is there chemotaxis force ? (No 0/Yes 1)", show_value=True, step=1)]
                         )

    tableau
    return (tableau,)


@app.cell
def _(mo):
    # Lancer le code avec les paramètres et afficher les résultats
    bouton = mo.ui.run_button(label="Start the experiment")
    bouton
    return (bouton,)


@app.cell
def _(bouton, tableau):
    if bouton.value:
        cell_cell, cell_mat, D, chemo = tableau.value[:]
        print("Started experiment with parameters:")
        print(f"Coefficient cell_cell: {cell_cell}")
        print(f"Coefficient cell_mat: {cell_mat}")
        print(f"Coefficient diffusion D: {D}")
        if chemo:
            print("Wiht chemotaxis force")
        else:
            print("No chemotaxis force")
        from eon import main_function
        main_function(cell_cell, cell_mat, D, chemo+1)
    return D, cell_cell, cell_mat, chemo, main_function


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
