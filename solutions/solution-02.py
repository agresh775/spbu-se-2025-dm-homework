#!/usr/bin/env python3
n, m = map(int, input().split())
a = input().split()
a.sort()
r = [[] for i in range(26)]
inv_r = [[] for i in range(26)]

for i in range(m):
    x, y = input().split()
    r[ord(x)-97].append(ord(y)-97)
    inv_r[ord(y)-97].append(ord(x)-97)

cnt_min = cnt_max = 0
for i in range(n):
    if len(inv_r[ord(a[i])-97]) == 0: 
        cnt_min += 1
        print(a[i], end=' ')
print()
for i in range(n):
    if len(r[ord(a[i])-97]) == 0: 
        cnt_max += 1
        print(a[i], end=' ')
print()
if cnt_min == 1:
    for i in range(n):
        if len(inv_r[ord(a[i])-97]) == 0:
            print(a[i])
            break
else: print('-')
if cnt_max == 1:
    for i in range(n):
        if len(r[ord(a[i])-97]) == 0:
            print(a[i])
            break
else: print('-')
