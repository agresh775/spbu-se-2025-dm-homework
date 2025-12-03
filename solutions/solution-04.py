#!/usr/bin/env python3
def permutation(a, b, used, n):
    flag = 0
    for i in range(n):
        if not used[i]:
            used[i] = 1
            b.append(a[i])
            permutation(a, b, used, n)
            b.pop()
            used[i] = 0
            flag = 1
    if not flag: print(*b)

n = int(input())
a = input().split()
b = []
used = [0]*n
permutation(a, b, used, n)