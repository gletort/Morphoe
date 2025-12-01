import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)

@app.cell
def _(mo):
    title=mo.md("##Model forces Calibration")
    return title

@app.cell(hide_code=True)
def _(mo):
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
    return



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
    return

if __name__ == "__main__":
    app.run()
