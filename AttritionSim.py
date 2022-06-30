'''
Version: 0.3
Date: 2022-06-03
Authors: Steffen Pielström
Dependencies: config.py v0.2, random, math

AttritionSim is a module for agent-based simulations of attrition warfare. 
It is inspired by the classical Lanchester Laws of attrition, but follows
an alternative, individual-based, stochastic modeling approach based on 
modeling individual units and their probability to eliminate an enemy unit.

The module provides a basic 'unit' class to model units with particular
attributes and a 'force' class to model a fighting force of multiple unit
class objects. Furthermore there are functions that to create two opposing 
forces, have them fight each other and print the results.

The module requires a configuration file config.py that contains default
values.
'''

# Imports
# --------------------------------------------------------------------

from random import random
from math import atan
from math import sin
from math import cos


# Variables
# --------------------------------------------------------------------


from config import max_steps
from config import dist_border_init
from config import firing_distance

from config import Faction
from config import Name
from config import Color
from config import Strength
from config import Range
from config import Speed
from config import Accuracy
from config import Formation


# Classes and methods
# --------------------------------------------------------------------

class unit:
    '''
    Version: 0.1
    Authors: Steffen Pielström

    The fundamental object in the simulation. An individual unit with a set of 
    properties that define its capabilities.
    - faction: either 0 or 1
    - pos: list of floats, indicating unit's x and y position on the grid
    - range: float, unit's maximum firing range
    - speed: float, moving distance per time step
    - accuracy: float between 0 and 1; probability to hit target per time step
    - target_pos: list of two floats; x and y position of the current target
    - target_index: int, the index of the target in the opposing force's units list
    - target_dist: distance to target
    - is_hit: boolean, indicates if the unit has been hit in the current time step
    - has_hit: boolean, indicates if the unit has hit its target in the current time step
    '''
    
    def __init__(self, faction, pos=None, range=Range[0], speed=Speed[0], accuracy=Accuracy[0], 
        target_pos=None, target_index=None, target_dist=None, is_hit=False, 
        has_hit=False):
        '''
        Test:
        >>> test_unit = unit(0, speed=5)
        >>> test_unit.speed
        5
        '''
        self.faction = faction
        self.pos = pos
        self.range = range
        self.speed = speed
        self.accuracy = accuracy
        self.target_pos = target_pos
        self.target_index = target_index
        self.target_dist = target_dist 
        self.is_hit = is_hit
        self.has_hit = has_hit


    def move(self):
        '''
        Version: 0.1
        Authors: Steffen Pielström

        Method to move a unit each time step. Updates the global pos attributes
        for the unit in question.
        Dependencies: math

        Test:
        >>> test_unit = unit(0, pos=[0, 0], speed=10, range=1, target_pos=[50, 0], target_dist=50)
        >>> test_unit.move()
        >>> [test_unit.pos[0], test_unit.pos[1]]
        [10.0, 0]
        '''
        
        # Check if target exits
        if self.target_dist == None:
            pass

        # Check if target is out of comfort firing range
        elif self.target_dist <= self.range:
            pass

        elif self.target_dist == 0:
            pass
        
        else: 
            # Adjust speed if too close to target
            if self.target_dist <= self.speed:
                speed = self.target_dist - self.range*firing_distance
            else:
                speed = self.speed


            # Avoid division by zero when claculating target angle
            if self.pos[0] == self.target_pos[0]:
                if self.target_pos[1] < self.pos[1]:
                    self.pos[1] -= speed
                else:
                    self.pos[1] += speed

            elif self.target_dist > speed:
                alpha = atan(abs(self.pos[1] - self.target_pos[1]) / abs(self.pos[0] - self.target_pos[0]))
                if self.target_pos[0] < self.pos[0]:
                    self.pos[0] -= cos(alpha)*speed
                elif self.target_pos[0] > self.pos[0]:
                    self.pos[0] += cos(alpha)*speed
                else:
                    pass
                if self.target_pos[1] < self.pos[1]:
                    self.pos[1] -= sin(alpha)*speed
                elif self.target_pos[1] > self.pos[1]:
                    self.pos[1] += sin(alpha)*speed
                else:
                    pass
            else:
                pass



    def calculate_distance(self, other):
        '''
        Version: 0.1
        Authors: Steffen Pielström

        Arguments: another unit
        Returns: the distance to the other unit

        Test:
        >>> test_unit = unit(0, pos=[0, 0])
        >>> other_unit = unit(1, pos=[10, 10])
        >>> test_unit.calculate_distance(other_unit) == (10**2 + 10**2)**0.5
        True
        '''
        xdist = abs(self.pos[0] - other.pos[0])
        ydist = abs(self.pos[1] - other.pos[1])
        distance = (xdist**2+ydist**2)**0.5
        return distance


    def find_target(self, units):
        '''
        Version: 0.2
        Authors: Steffen Pielström

        Finds the closest enemy unit in a list of units.

        Arguments: a list of units
        Returns: the index of the closest unit in that list
        Uses: calculate_distance()

        Test:
        >>> test_unit = unit(0, pos=[0, 0])
        >>> enemy_units = [unit(1, pos=[10, 10]), unit(1, pos=[10, 20])]
        >>> test_unit.find_target(enemy_units)
        >>> test_unit.target_index
        0
        '''
        distances = []
        for element in units:
            distances.append(self.calculate_distance(element))
        self.target_index = distances.index(min(distances))
        self.target_pos = units[self.target_index].pos
        self.target_dist = min(distances)
 

    def fire(self, enemy_units):
        '''
        Version: 0.1
        Authors: Steffen Pielström

        Applies a random number generator to check if the unit hits its target.
        
        Arguments: a list of units
        Returns: nothing, changes the is_hit attribute of a hit target to True
        Uses: random

        Test:
        >>> test_unit = unit(0, accuracy=1, target_index=1, target_dist=1, range=10)
        >>> enemy_units = [unit(1), unit(1)]
        >>> test_unit.fire(enemy_units)
        >>> enemy_units[1].is_hit
        True
        '''
        # Check if target got hit
        if self.target_dist <= self.range and random() < self.accuracy:
            self.has_hit = True
            enemy_units[self.target_index].is_hit = True


class force():
    '''
    Version: 0.1
    Authors: Steffen Pielström

    A faction is a group of units with certain common attributes.
    - index: an iteger, either 0 or 1
    - name: string, name of the faction, mainly for indicating in outputs
    - color: a color, defaults are 'blue' and 'darkred'
    - strength: integer, no of units in the force
    - range: float, units' maximum firing range
    - speed: float, moving distance per time step
    - accuracy: float between 0 and 1; prob of each unit per time step to hit its target
    - formation: string, either 'one line', 'two lines' or 'scattered'
    - units: a list of objects of class 'unit'
    '''

    def __init__(self, index, name, color=Color[0], strength=Strength[0], range=Range[0], 
        speed=Speed[0], accuracy=Accuracy[0], formation=Formation[0], units=[]):
        '''
        Test:
        >>> blue_force = force(0, 'blue', strength=10)
        >>> blue_force.strength
        10
        '''
        
        self.index = index
        self.name = name
        self.color = color
        self.strength = strength
        self.range = range
        self.speed = speed
        self.accuracy = accuracy
        self.formation = formation
        self.units = units


    def generate_positions(self):
        '''
        Version: 0.1
        Authors: Steffen Pielström

        Generates initial x and y coordinates for all units in a force depending on
        the force's formation parameter. Currently, only a one line formation is
        implemented.

        Returns: a list of two lists of float, [[x1, x2, ...], [y1, y2, ...]]

        Test:
        >>> blue_force = force(0, 'blue', strength=9, formation='one line')
        >>> blue_force.generate_positions()[1][0]
        10.0
        '''

        # Generate list of coordinates
        xpos = []
        ypos = []
        
        # Single line formation 
        if self.formation == 'one line':
            dist = 100/(self.strength+1)
            for i in range(self.strength):
                if self.index == 0:
                    xpos.append(0+dist_border_init)
                elif self.index == 1:
                    xpos.append(100-dist_border_init)   
                else:
                    print('Error in initialize_postions(): faction unknown')   
                ypos.append((1+i)*dist)
        return([xpos, ypos])

        
    def initialize_units(self):
        '''
        Version: 0.1
        Authors: Steffen Pielström

        Method to initialize unit attributes within a force. 
        
        Test:
        >>> blue_force = force(0, 'blue', strength=9)
        >>> blue_force.initialize_units()
        >>> blue_force.units[0].pos[1]
        10.0
        '''

        positions = self.generate_positions()
        self.units = []
        for i in range(self.strength):
            self.units.append(
                unit(self.index, [positions[0][i], positions[1][i]], 
                self.range, self.speed, self.accuracy)
                )

    def kill_hit_units(self):
        '''
        Version: 0.1
        Authors: Steffen Pielström

        Removes all units hit at the end of a time step.

        Test:
        >>> blue_force = force(0, 'blue', strength=9)
        >>> blue_force.initialize_units()
        >>> len(blue_force.units)
        9
        >>> blue_force.units[0].is_hit = True
        >>> blue_force.kill_hit_units()
        >>> len(blue_force.units)
        8
        '''
        for element in self.units:
            if element.is_hit == True:
                self.units.remove(element)


class output():
    '''
    Version: 0.1
    Authors: Steffen Pielström

    The output class object stores all information that may be returned 
    as output after a simulation.
    '''
    def __init__(self, name=Name, strength=Strength, range=Range, 
                speed=Speed, accuracy=Accuracy, formation=Formation):

        self.name = name
        self.strength = strength
        self.range = range
        self.speed = speed
        self.accuracy = accuracy
        self.formation = formation
        self.steps = 0
        self.blue = []
        self.red = []


    def update(self):
        '''
        Track the strength development in each step of the simulation.
        '''
        self.steps += 1
        self.blue.append(len(blue_force.units))
        self.red.append(len(red_force.units))

    def print(self, type='result'):
        '''
        Print formatted output.
        '''

        if type == 'result':
            steps = 'steps: '+str(self.steps)
            if self.blue[-1] == 0 and self.red[-1] > 0:
                result = 'result: '+Name[1]+' victory'
            elif self.blue[-1] > 0 and self.red[-1] == 0:
                result = 'result: '+Name[0]+' victory'
            elif self.blue[-1] == 0 and self.red[-1] == 0:
                result = 'result: both forces down'
            else:
                result = 'result: no winner yet'
            blue = self.name[0]+' force strength: '+str(self.blue[-1])
            red = self.name[1]+' force strength: '+str(self.red[-1])
            print(steps+'\n'+result+'\n'+blue+'\n'+red)

        elif type == 'full':
            values = ''
            for i in range(len(self.blue)):
                values += '\n' + str(self.blue[i]) + ',' + str(self.red[i])
            print(self.name[0]+','+self.name[1]+ values)

        else:
            print('Warning: Output format \''+str(output)+'\' unknown.')
            print('Specify as either \'result\' or \'full\'')



# Functions
# --------------------------------------------------------------------

def initialize(faction=Faction, name=Name, color=Color, strength=Strength, 
    range=Range, speed=Speed, accuracy=Accuracy, formation=Formation):
    '''
    Version: 0.1
    Authors: Steffen Pielström

    Initializes two forces to start a simulation.

    Test:
    ##>>> blue_force = force(0, 'blue')
    ##>>> initialize()
    ##>>> blue_force.units[0].pos
    ##[10, 9.090909090909092]
    '''
    global blue_force
    blue_force = force(faction[0], name[0], color[0], strength[0], range[0], speed[0], 
    accuracy[0], formation[0])
    blue_force.initialize_units()

    global red_force
    red_force = force(faction[1], name[1], color[1], strength[1], range[1], speed[1], 
    accuracy[1], formation[1])
    red_force.initialize_units()

    global results
    results = output()


def update_forces(blue_force, red_force):
    '''
    Version: 0.2
    Authors: Steffen Pielström

    Performs a single complete simulation step for all forces/units
    involved. 
    
    Test:
    To be done...
    '''
    # First set of loops: identify targets
    for element in blue_force.units:
        element.find_target(red_force.units)
    for element in red_force.units:
        element.find_target(blue_force.units)

    # Second set of loops: move and fire
    for element in blue_force.units:
        element.move()
        element.fire(red_force.units)
    for element in red_force.units:
        element.move()
        element.fire(blue_force.units) 
    blue_force.kill_hit_units()
    red_force.kill_hit_units()


def run_simulation(max_steps=max_steps, output='return', faction=Faction, name=Name,
    color=Color, strength=Strength, range=Range, speed=Speed, accuracy=Accuracy,
    formation=Formation):
    '''
    Version: 0.3
    Authors: Steffen Pielström
    
    This is the main function calling all methods and functions in the
    module and runnning an antire simulation from initialization to 
    returning the final result.
    '''
    initialize(faction=faction, name=name, color=color, strength=strength, range=range, 
        speed=speed, accuracy=accuracy,formation=formation)
    
    # Initialize loop conditions
    conditions = True

    # Main loop
    while conditions == True:        
        update_forces(blue_force, red_force)        
        results.update()

        conditions = (
            len(blue_force.units) > 0 
            and len(red_force.units) > 0 
            and results.steps < max_steps
            )

    # Handle results
    if output == 'return':
        return results
    else:
        results.print(output)


# Use doctest to test functions and methods
# --------------------------------------------------------------------
'''
To use doctest, call this file from command line with:

python AttritionSim.py -v
'''

if __name__ == "__main__":#
    import doctest
    doctest.testmod()

run_simulation()