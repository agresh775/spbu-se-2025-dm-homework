#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from typing import Dict, List, Set, Tuple

def main() -> None:
    """Основная функция программы."""
    # Чтение входных данных
    n, m = map(int, input().split())
    X: List[str] = input().split() if n > 0 else []
    R: Dict[str, List[str]] = {x: [] for x in X}
    for _ in range(m):
        x, y = input().split()
        R[y].append(x)
    
    # Символ разделитель
    skip = input()
    skip = input()

    # Чтение ответа
    sorting = {x : None for x in X}
    for i in range(n):
        element, num = input().split()
        if int(num) != (i + 1):
            sys.exit(1)
        sorting[element] = int(num)
    
    for x in X:
        for y in R[x]:
            if sorting[y] > sorting[x]:
                print("Incorrect pair:", x, y, file=sys.stderr)
                sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()


