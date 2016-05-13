#!/usr/bin/env python3
# Склеивание трех файлов с одинаковым количеством строк
# с поиском по аргументу по строкам.
import sys
#
l1 = []
l2 = []
l3 = []

glue = []

def readfunc(f,l):
    for i in open(f).readlines():
        op = i.rstrip()
        l.append(op)
        
def gluefunc():
    for i in range(len(l1)):
        row = [l1[i],l2[i],l3[i]]
        glue.append(row)

if __name__ == '__main__':
    try:
        file1 = sys.argv[1] # файл №1
        file2 = sys.argv[2] # файл №2
        file3 = sys.argv[3] # файл №3
        search = str(sys.argv[4]) # 4 аргумент - запрос
        
        readfunc(file1,l1)
        readfunc(file2,l2)
        readfunc(file3,l3)
    
        gluefunc()

    
        for i in glue:
            if search in str(i):
                print(i)
                
    except IndexError:
            print("""
                 +------------------------------------+
                 |Необходимо 4 аргумента:             |
                 |./glue.py файл1 файл2 файл3 "запрос"|
                 +------------------------------------+
                  """)
