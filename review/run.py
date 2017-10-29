#!/bin/python
import os
n = raw_input("Enter the number of Processes:")
os.system('mpicc test.c')
os.system('mpirun -np '+str(n)+' ./a.out')
