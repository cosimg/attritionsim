#!/usr/bin/env python3
'''
Version: 0.1
Authors: Steffen Pielström
Dependencies: AttritionSim.py v0.3, config.py v0.2, argparse

This is the code base for turning AttritionSim into a CLI application 
based on pyinstaller.
'''

# Imports
# --------------------------------------------------------------------

import argparse

from config import max_steps

from config import Name
from config import Strength
from config import Range
from config import Speed
from config import Accuracy
from config import Formation

import AttritionSim as sim


# Parse arguments
# --------------------------------------------------------------------

description = ' '


parser = argparse.ArgumentParser(description=description)

parser.add_argument('--max_steps', default=max_steps, 
    help='Maximum number of simulation steps. Default: 100')
parser.add_argument('--output', default='result', 
    help='Output format, either \'result\' or \'full\'')
parser.add_argument('--name_blue', default=Name[0], 
    help='Displayed name og the first force.')
parser.add_argument('--name_red', default=Name[1], 
    help='Displayed name of the second foce.')
parser.add_argument('--strength_blue', default=Strength[0], 
    help='Numerical strength of the first force. Default: 10')
parser.add_argument('--strength_red', default=Strength[1],
     help='Numerical strength of the second force. Default: 10')
parser.add_argument('--range_blue', default=Range[0], 
    help='Firing range of the first force. Default: 50')
parser.add_argument('--range_red', default=Range[1], 
    help='Firing range of the second force. Default: 50')
parser.add_argument('--speed_blue', default=Speed[0], 
    help='Speed of the first force in distance units per simulation step. Default: 1')
parser.add_argument('--speed_red', default=Speed[1],
    help='Speed of the second force in distance units per simulation step. Default: 1')
parser.add_argument('--accuracy_blue', default=Accuracy[0],
    help='Blue unit\'s probability to kill an enemy unit per simulation step, number between 0 and 1. Default: 0.05')
parser.add_argument('--accuracy_red', default=Accuracy[1],
    help='Red unit\'s probability to kill an enemy unit per simulation step, number between 0 and 1. Default: 0.05')
parser.add_argument('--formation_blue', default=Formation[0],
    help='Formation of the first force, currently only \'one line\' is implemented.')
parser.add_argument('--formation_red', default=Formation[1],
    help='Formation of the second force, currently only \'one line\' is implemented.')

args = parser.parse_args()

# Main
# --------------------------------------------------------------------

sim.run_simulation(
    max_steps=int(args.max_steps),
    output=args.output, 
    name=[args.name_blue, args.name_red],
    strength=[int(args.strength_blue), int(args.strength_red)], 
    range=[float(args.range_blue), float(args.range_red)],
    speed=[float(args.speed_blue), float(args.speed_red)], 
    accuracy=[float(args.accuracy_blue), float(args.accuracy_red)],
    formation=[args.formation_blue, args.formation_red]
    )
