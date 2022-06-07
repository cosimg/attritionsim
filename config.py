'''
Version: 0.2
Authors: Steffen Pielström
Dependencies: typing
'''

# Imports
# ----------------------------------------------------------------------------------

from typing import List


# Simulation variables
# ----------------------------------------------------------------------------------
# The ones you can change for experimenting

# Unit attributes
Strength: List[int] = [10, 10]
Range: List[float] = [50, 50]
Speed: List[float] = [1,1]
Accuracy: List[float] = [0.05, 0.05] # a probabilty between 0 and 1
Formation: List[str] = ['one line', 'one line'] # more options not yet implemented

# Default for the max of simulation steps
max_steps: int = 100

# Size of the battlefield, both x and y are identical
field_size: float = 100

# Initial distance of units to the frame if in line
dist_border_init: float = 10 

# Proportion of range at wich units stop to close in to the enemy
firing_distance: float = 0.5 # a proportion between 0 and 1


# System variables
# ----------------------------------------------------------------------------------
# Change only if you want to mess with the system!

Faction: List[int] = [0, 1]
Name: List[str] = ['Blue', 'Red']
Color: List[str] = ['blue', 'darkred']
