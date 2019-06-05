#!/usr/bin/env python

import argparse
from Services.MainService import Main

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--processes', help='Number of processes will run. Greater or equal 1', required=False,
                    nargs='?', default=1, const=1)

args = parser.parse_args()

if int(args.processes) < 1:
    print('The number of process have greater or equal than 1.')
else:
    Main().run(int(args.processes))
