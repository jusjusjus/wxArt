#!/usr/bin/python

import argparse
import subprocess
import time

workers = ['algol01']
program = 'sleep' # dummy name

command = [program, '1']


try:
    time.sleep(10)
except:
    print('dummy')

