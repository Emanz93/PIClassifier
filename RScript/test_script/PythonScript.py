#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

# deve essere Rscript.
command = 'Rscript'
path2script = '/home/emanuele/Desktop/RScript.R'
args = ['11', '3', '9', '42']

cmd = [command, path2script] + args

x = subprocess.check_output(cmd, universal_newlines=True)

print('The max is {}'.format(x))
