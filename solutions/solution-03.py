#!/usr/bin/env python3
def dfs(graph, x):
    used[x] = 1
    for v in graph[x]:
        if not used[v]: dfs(graph, v)
    b.append(chr(x+97))

n, m = map(int, input().split())
a = input().split()
b = []
used = [0]*26
r = [[] for i in range(26)]
for i in range(m):
    x, y = input().split()
    r[ord(x)-97].append(ord(y)-97)
for i in range(n):
    if not used[ord(a[i])-97]:
        dfs(r, ord(a[i])-97)
b.reverse()
for i in range(n):
    print(b[i], i+1)