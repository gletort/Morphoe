# Morphoe

Morphogenesis of olfactory epithelium.

Python code to simulate migration of early olfactory neurons along the telencephalon.
The matrix (telencephalon) is represented as an immobile and uncrossable horseshoe-like barrier (paraboloid).
Cells are distributed along the telencephalon and follow a chemotaxis gradient (mimicking Cxcl12a signalling) to converge in two clusters.

![Example of a simulation](https://github.com/gletort/Morphoe/raw/main/imgs/simu.png)

# Installation/Usage

There is no dependencies to install, you can use it directly on python (tested on python 3.8).

To use it, call the `eon.py` main file in the simulation directory containing your parameter file `params.py`. Templates of parameter files are given in the folder [`simulation_template`](https://github.com/gletort/Morphoe/simulation_template) and in [our github repository associated to our publication](https://github.com/JulieBatut/Zilliox-Letort_2024/tree/main).

To run it, you can go inside the simulation directory and type in a Terminal:
```
python path_to_Morphoe_src_folder/eon.py 
```

# References

Refer to our publication Zilliox, Letort et al. for more details about the model.
If you use this code or part of this code, please cite our publication or/and this repository.

## License
Distributed under the terms of the GPL-3 license, "Morphoe" is free and open source software
