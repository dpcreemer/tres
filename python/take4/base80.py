#!/usr/bin/python3
import sys, nxos80 
from nxos80 import process_file

if len(sys.argv) > 1: 
  cfg_file = sys.argv[1]
else:
  cfg_file = input("config file name:")

process_file(cfg_file)

