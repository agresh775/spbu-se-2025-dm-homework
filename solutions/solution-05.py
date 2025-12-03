#!/usr/bin/env python3
def combination(a, b, x, n, k):
    if x == n:
        if len(b) == k: print(*b)
        return
    b.append(a[x])
    combination(a, b, x + 1, n, k)
    b.pop()
    combination(a, b, x + 1, n, k)

n, k = map(int, input().split())
a = input().split()
b = []
combination(a, b, 0, n, k)