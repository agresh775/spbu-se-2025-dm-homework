#!/usr/bin/env python3
def R():
    for i in range(n):
        if [a[i], a[i]] not in r: 
            print('*', end='')
            return
    print('R', end='')
    
def S():
    for i in range(m):
        if r[i][::-1] not in r:
            print('*', end='')
            return
    print('S', end='')
    
def T():
    for i in range(m):
        for j in range(m):
            if r[i][1] == r[j][0]:
                if [r[i][0], r[j][1]] not in r:
                    print('*', end='')
                    return
    print('T', end='')
    
def A():
    for i in range(m):
        if r[i][0] == r[i][1]: continue
        if r[i][::-1] in r:
            print('*', end='')
            return
    print('A', end='')

n, m = map(int, input().split())
a = input().split()
r = []
for i in range(m):
    r.append(input().split())
R()
S()
T()
A()
    
