# Attrition Simulator

- **Version:** 0.4
- **Date:** 2022-06-05
- **Contributors:** Steffen Pielström

*Attrition Simulator* is a programme for agent-based simulations of attrition warfare. It is inspired by the classical Lanchester Laws of attrition, but follows an alternative, individual-based, stochastic modeling approach based on modeling individual units and their probability to eliminate an enemy unit.


## Technical overview

The Attrition Simulator is based on a **Python module** (`AttritionSim.py`) that can be used directly to script experiments. The module provides a basic 'unit' class to model units with particular attributes and a 'force' class to model a fighting force of multiple unit class objects. Furthermore, there are functions that create two opposing forces, have them fight each other and print the results. **Simulation parameters** can be set either as arguments to the functions and methods, or by manipulating the configuration file `config.py`.

The file `AttritionSimCLI.py` provides a **command line interface** that can pass simulation parameters as arguments.

For playing and exploration, there is a **graphical user interface** based on the [*PySimpleGui*](https://pysimplegui.readthedocs.io/) package. We provide a version packaged with *pyinstaller* for *Linux* and *Windows* in a *zip* file for download.

## How to use it: the easy way

(Currently only for *Linux*, a *Windows* version is in the making) **Download** the latest release of the standalone GUI version from [release section](https://github.com/cosimg/attritionsim/releases/tag/v0.3) and execute the file ***AttritionSimGui***. Depending on your operating system, it might be necessary to mark the file as executable first.

![](GUI03Screenshot01.jpg)


## How to use it: the nerd way

### as a python module in a script or on the interactive console

Download the module [https://github.com/cosimg/attritionsim](https://github.com/cosimg/attritionsim). Import it with
```
import AttritionSim as sim
```
The simplest way to use the module is to rely on the wrapper function `run_simulation()` that will run an entire simulation for you.
```
>>> sim.run_simulation()
<AttritionSim.output object at 0x7fc47658d5b0>
```

Simulation parameters can be specified as arguments that are typically organized in pairs specifying values for both of the opposing forces. You can specify:

- `max_steps`: The maximum number of steps the simulation will run.
- `strength`: The initial numerical strengths of both forces.
- `range`: The firing ranges of both forces.
- `accuracy`: The probabilities to hit the current target in a given time step.
- `formation`: The opposing forces' initial spatial layout. Currently, 'one line' is the only option implemented.

For instance, you can run a simulation with one force haveing twice the numbers, the other force twice the accuracy, like this:
```
>>> sim.run_simulation(strength=[10, 5], accuracy=[0.05, 0.1])
<AttritionSim.output object at 0x7fc4766814c0>
```

Alternatively, there is the option to control paramters by changing the **configuration file** `config.py`.

No matter where the parameters come from, the function **returns an object** containing simulation paramters and results. The most important attributes are:

- `steps`: The number of steps the simulation has run.
- `blue`: A list containg the numerical strength of the first force at each step of the simulation.
- `red`: The same for the other force.

As an example, you can access the strength values for the blue force at each step like this:
```
>>> my_result = sim.run_simulation(Strength=[10, 5], Range=[200, 200])
>>> my_result.blue
[10, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7]
```

And, correspondingly, for the opposing red force:
```
>>> my_result.red
[5, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 0]
```

#### Deeper in the rabbit hole...
The module is based on a `unit` class that allows to define unit objects that have certain attributes and try to kill each other in each step of the simulation. Additionally, there is a `force` class, that is, basically, a list of units and some attributes shared by all of them.

so, if you do not want the global function `run_sumulation()` to handle everything for you, you can create a blue force on your own; here with 10 units and 5% chance to hit the enemy, and initialize its units.
```
>>> blue_force = sim.force(0, 'blue', strength=10, accuracy=0.05)
>>> blue_force.initialize_units()
>>> blue_force
<AttritionSim.force object at 0x7f4913fbbee0>
```
Create a red force with less men that shoot better.
```
>>> red_force = sim.force(1, 'red', strength=5, accuracy=0.1)
>>> red_force.initialize_units()
```
**Or** rely on the `initialize()` function to do all that at once.
```
>>> sim.initialize(strength=[10, 5], accuracy=[0.05, 0.1])
```
Now, you can use the function `update_forces()` to run single iterations.
```
>>> sim.update_forces(blue_force, red_force)
```

### with the Command Line Interface

The file `AttritionSimCLI.py` can be called from the command line. It will directly execute `run_simulation()` with arguments passed *via* *argparse* or the defaults defined in the configuration file (`config.py`), and return the result.
```
$ python AttritionSimCLI.py --strength_blue 10 --strength_red 5 --accuracy_blue 0.05 --accuracy_red 0.1
steps: 29
result: Blue victory
Blue force strength: 8
Red force strength: 0
```

If you want to get the full data, i.e. the strengths of both forces in each step of the simulation, you can specify that with the `--output` argument, and write it into a file:
```
python AttritionSimCLI.py --output full > simulation001.csv
```

### with the Graphical User Interface started from the Python console

If you have *Python* installed on your computer, you can easily run the GUI version with your *Python* installation. Dependencies are mostly part of the standard library, the only exception being `PySimpleGUI`. To install that you run
```
$ pip install PySimpleGUI
```
Then, you download the module from [https://github.com/cosimg/attritionsim](https://github.com/cosimg/attritionsim), go into the folder and run
```
$ python AttritionSimGUI.py
```

### How to deploy a new version

I am more than happy to accept pull requests with bug fixed, typo corrections, code (and aesthetic) improvements and added features. I only kindly request you to adehere at least to the bare minimum of good conduct regarding modularity, comments, documentation, doctests, cetera that I have been able to instill so far. The standalone GUI version is made with *pyinstaller*:
```
$ pip install pyinstaller
$ pyinstaller -F AttritionSimGUI.py
```
Note that *pyinstaller* can create a standalone program only for the operating system it is running on.

## TODOs and known issues

- GUI Timing: show each simulation step live in the GUI application and synchronize with system time, so that a step in the simulation lasts the nth fraction of a second.
- Battle field size: add the possibility to alter the size of the battle field as a simulation paramter. Currently, the simulation is always running on a 100 x 100 length units grid. 
- Formations: implement more formations than 'one line'
- Hinderance: add an option that units can not shoot 'through each other'
- Range and speed bar: add bars to the GUI that indicate the current range and speed per simulation step for both forces
- GUI Strength curve: add a graph to GUI that shows the strength curves for both forces
- Data output: add an export function to the GUI
- Unit density: find a way to return unit density (number of units per space, maybe in relation to range) to allow for better comparition of results with other Lanchester-type models.
- Implement static typing in AttritionSimGUI.py


## Literature

Lanchester, Frederick W. (1916). *Aircraft in Warfare*. Constable and Company Limited, London.

