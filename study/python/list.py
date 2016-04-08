#!/usr/bin/env python3
for line in open('soc1.csv').readlines():
    spline = line.rstrip().split(', ')
    if (spline[0]) == '':
        spline[0] = 'None'
    print (spline)
