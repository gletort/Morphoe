import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    tableau = mo.ui.array([mo.ui.slider(0.1,1, label="Coefficient cell_cell", show_value=True, step=0.1),
                           mo.ui.slider(1,9, label="Coefficient cell_mat", show_value=True, step=1),
                           mo.ui.slider(0.001,0.009, label="Coefficient diffusion D", show_value=True, step=0.001)]
                         )

    tableau
    return (tableau,)


@app.cell
def _(mo):
    # Lancer le code avec les paramètres et afficher les résultats
    bouton = mo.ui.run_button(label="Lancer la simulation")
    bouton
    return (bouton,)


@app.cell
def _(bouton, tableau):
    if bouton.value:
        cell_cell, cell_mat, D = tableau.value[:]
        print("Simulation lancée avec les paramètres:")
        print(f"Coefficient cell_cell: {cell_cell}")
        print(f"Coefficient cell_mat: {cell_mat}")
        print(f"Coefficient diffusion D: {D}")
        from eon import main_function
        main_function(cell_cell, cell_mat, D)
    return


if __name__ == "__main__":
    app.run()
