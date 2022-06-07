'''
Version: 0.3
Authors: Steffen Pielström
Dependencies: AttritionSim.py v0.3, config.py v0.2, PySimpleGui, time, typing

GUI application based on the AttritionSim module. To be deplyed with pyinstaller.
'''

# Imports
# ------------------------------------------------------------------------------

import PySimpleGUI as sg
from time import sleep

import AttritionSim as sim

from config import Faction
from config import Name
from config import Color
from config import Strength
from config import Range
from config import Speed
from config import Accuracy
from config import Formation

# Variables
# --------------------------------------------------------------------

unit_size: float = 1
frame_size = (600, 500)
input_dimension = (7, 1)

# Second per time step in the gui and fraction of a time step a shooting 
# line remains visible. This is not yet implemented. -> TODO
sec_per_step: float = 0.1 
time_fraction_per_shot: float = 0.5

step_sum: int = 0

initialized: bool = False
max_steps: int = 1


# Layout
# --------------------------------------------------------------------

graph = sg.Graph(frame_size, (0, 0), (100, 100), key='-GRAPH-', background_color='grey')

input_blue = [
    sg.Text('Blue Force:', text_color=Color[0], font='bold'),
    sg.Text('strength', text_color=Color[0]),
    sg.Input(default_text=Strength[0], key='-STRENGTH_B-', size=input_dimension),
    sg.Text('range', text_color=Color[0]),
    sg.Input(default_text=Range[0], key='-RANGE_B-', size=input_dimension),
    sg.Text('speed', text_color = Color[0]),
    sg.Input(default_text=Speed[0], key='-SPEED_B-', size=input_dimension),
    sg.Text('accuracy', text_color=Color[0]),
    sg.Input(default_text=Accuracy[0], key='-ACCURACY_B-', size=input_dimension),
    ]

input_red = [
    sg.Text('Red  Force:', text_color=Color[1], font='bold'),
    sg.Text('strength', text_color=Color[1]),
    sg.Input(default_text=Strength[1], key='-STRENGTH_R-', size=input_dimension),
    sg.Text('range', text_color=Color[1]),
    sg.Input(default_text=Range[1], key='-RANGE_R-', size=input_dimension),
    sg.Text('speed', text_color=Color[1]),
    sg.Input(default_text=Speed[1], key='-SPEED_R-', size=input_dimension),
    sg.Text('accuracy', text_color=Color[1]),
    sg.Input(default_text=Accuracy[1], key='-ACCURACY_R-', size=input_dimension),
    ]
screen_counter = [
    sg.Text('Steps simulated: '),
    sg.Text(step_sum, key='-STEPS_SIMULATED-'),
    sg.Text('Blue force: ', text_color=Color[0]),
    sg.Text(' - ', key='-BLUE_STRENGTH-', text_color=Color[0]),
    sg.Text('Red force: ', text_color=Color[1]),
    sg.Text(' - ', key='-RED_STRENGTH-', text_color=Color[1]),
    ]
buttons = [
    sg.Button('Place new forces', key='-BUTTON1-'),
    sg.Button('Run simulation for', key='-BUTTON2-'), 
    sg.Input(default_text=max_steps, key='-MAX_STEPS-', size=input_dimension),
    sg.Text('steps')
    ]

layout = [
    [graph],
    [sg.Text('Initial configuration', font='bold')],
    input_blue,
    input_red,
    buttons,
    [sg.Text('Current state', font='bold')],
    screen_counter
    ]


# Functions
# --------------------------------------------------------------------

def draw_units(force):
  '''
  Draws units on the graph.
  Arguments: a force object
  '''
  for element in force.units:
    graph.draw_circle(
      (element.pos[0], element.pos[1]), 
      unit_size, fill_color=force.color, line_color=force.color
      )

def draw_attacks():
    '''
    Function for drawing lines between units if killing each other.
    '''   
    for element in blue_force.units:
        if element.has_hit == True:
            graph.draw_line(element.pos, element.target_pos)
        else:
            pass

    for element in red_force.units:
        if element.has_hit == True:
            graph.draw_line(element.pos, element.target_pos)
        else:
            pass

    
def reset_has_hit():
    '''
    This function is necessary to reset the has_hit attribute in all units after drawing
    the shooting lines in each simulation step. It is probably not the most elegant of
    sulutions and you are invited to come up with a better one. 
    '''
    for element in blue_force.units:
        element.has_hit = False
    for element in red_force.units:
        element.has_hit = False

def current_state(blue_force, red_force):
    '''
    Produce some output for debugging.
    '''
    output = 'blue: \n'  
    output += 'target, [x, y] \n'
    for element in blue_force.units:
        output += str(element.target_index)+', '+str(element.pos)+'\n'
    output += 'red: \n'  
    output += 'target, [x, y] \n'
    for element in red_force.units:
        output += str(element.target_index)+', '+str(element.pos)+'\n'
    print(output)


def initialize_gui():
    '''
    
    '''

    graph.erase()

    # Read values from input fields
    Strength[0] = int(values['-STRENGTH_B-'])
    Range[0] = float(values['-RANGE_B-'])
    Speed[0] = float(values['-SPEED_B-'])
    Accuracy[0] = float(values['-ACCURACY_B-'])

    Strength[1] = int(values['-STRENGTH_R-'])
    Range[1] = float(values['-RANGE_R-'])
    Speed[1] = float(values['-SPEED_R-'])
    Accuracy[1] = float(values['-ACCURACY_R-'])

    # Initialize forces
    global blue_force
    blue_force = sim.force(Faction[0], Name[0], Color[0], Strength[0], Range[0], Speed[0], 
    Accuracy[0], Formation[0])
    blue_force.initialize_units()
    draw_units(blue_force)

    global red_force
    red_force = sim.force(Faction[1], Name[1], Color[1], Strength[1], Range[1], Speed[1], 
    Accuracy[1], Formation[1])
    red_force.initialize_units()
    draw_units(red_force)

    # Update screen output
    window['-BLUE_STRENGTH-'].update(len(blue_force.units))
    window['-RED_STRENGTH-'].update(len(red_force.units))
    window['-STEPS_SIMULATED-'].update(step_sum)

    # Variables for output generation
    global blue
    blue = []
    global red
    red = []


def run_simulation_gui(blue_force, red_force, max_steps=max_steps):    
    '''
    '''
    # Initialize loop conditions
    steps = 0
    if len(blue_force.units) > 0 and len(red_force.units) > 0:
        conditions = True
    else:
        conditions = False

    # Initialize lists for output tracking
    blue = []
    red = []

    # Main loop
    while conditions == True:        

        # Simulate step
        sim.update_forces(blue_force, red_force)    

        # Update screen
        global step_sum
        step_sum += 1
        graph.erase()
        draw_attacks()
        draw_units(blue_force)
        draw_units(red_force)
        reset_has_hit()
        window['-STEPS_SIMULATED-'].update(step_sum)
        window['-BLUE_STRENGTH-'].update(len(blue_force.units))
        window['-RED_STRENGTH-'].update(len(red_force.units))

        # Update loop conditions
        steps += 1   
        conditions = (
            len(blue_force.units) > 0 
            and len(red_force.units) > 0 
            and steps < max_steps
            )

        # Update stored outputs
        blue.append(len(blue_force.units)) #<--------------------------------TODO no putput function yet
        red.append(len(red_force.units))     
        #sleep(sec_per_step)   #<----------------------------------------------------------------TODO still freezing the gui


# Main
# --------------------------------------------------------------------

window = sg.Window('Attrition Simulator', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    
    # Update values according to inputs and initialize
    if event == '-BUTTON1-': 
        step_sum = 0
        initialize_gui()
        initialized = True

    # Run simulation
    if event == '-BUTTON2-' and initialized == True:
        max_steps = int(values['-MAX_STEPS-'])
        run_simulation_gui(blue_force, red_force, max_steps)
    

window.close()
