#!/usr/bin/env python3
for line in open('/proc/vmstat').readlines():
    if 'pgscan' in line:
    l = line.rstrip().split(" ")
        for (key,value) in l:
            d[key] = value
