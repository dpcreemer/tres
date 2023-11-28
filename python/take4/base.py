#!/usr/bin/python3
import sys, nxos 

if len(sys.argv) > 1: 
  cfg_file = sys.argv[1]
else:
  cfg_file = input("config file name:")

nxos.process_file(cfg_file)

