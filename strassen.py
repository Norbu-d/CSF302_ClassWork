"""
Lab 2 - Q3 (bonus): Strassen's Matrix Multiplication
CSF303 - Algorithm Design and Analysis

O(n^log2(7)) ~= O(n^2.807) via 7 recursive multiplications instead of 8.
n must be a power of 2.
"""

import random

mult_count = 0  # global counter for scalar (1x1) multiplications


def add(a, b):
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]


def sub(a, b):
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]


def split(m):
    n = len(m)
    mid = n // 2
    a11 = [row[:mid] for row in m[:mid]]
    a12 = [row[mid:] for row in m[:mid]]
    a21 = [row[:mid] for row in m[mid:]]
    a22 = [row[mid:] for row in m[mid:]]
    return a11, a12, a21, a22


def combine(c11, c12, c21, c22):
    top = [r1 + r2 for r1, r2 in zip(c11, c12)]
    bottom = [r1 + r2 for r1, r2 in zip(c21, c22)]
    return top + bottom


def strassen(a, b):
    global mult_count
    n = len(a)
    if n == 1:
        mult_count += 1
        return [[a[0][0] * b[0][0]]]

    a11, a12, a21, a22 = split(a)
    b11, b12, b21, b22 = split(b)

    m1 = strassen(add(a11, a22), add(b11, b22))
    m2 = strassen(add(a21, a22), b11)
    m3 = strassen(a11, sub(b12, b22))
    m4 = strassen(a22, sub(b21, b11))
    m5 = strassen(add(a11, a12), b22)
    m6 = strassen(sub(a21, a11), add(b11, b12))
    m7 = strassen(sub(a12, a22), add(b21, b22))

    c11 = add(sub(add(m1, m4), m5), m7)
    c12 = add(m3, m5)
    c21 = add(m2, m4)
    c22 = add(sub(add(m1, m3), m2), m6)

    return combine(c11, c12, c21, c22)


def print_matrix(m):
    for row in m:
        print(row)


def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


def main():
    global mult_count
    while True:
        n = int(input("Enter matrix size n (power of 2): "))
        if is_power_of_two(n):
            break
        print("n must be a power of 2. Try again.")

    a = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]
    b = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]

    print("Matrix A:")
    print_matrix(a)
    print("Matrix B:")
    print_matrix(b)

    mult_count = 0
    result = strassen(a, b)

    print("\nResult (Strassen):")
    print_matrix(result)
    print(f"\nScalar multiplication count: {mult_count}  (7 per split level, vs 8 for standard)")

    # --- Analysis / Conclusion ---
    # Standard multiplication does 8 scalar multiplications per split level;
    # Strassen only does 7, at the cost of extra additions/subtractions to
    # combine results. That single multiplication saved per level compounds
    # recursively, giving O(n^log2(7)) ~= O(n^2.807) instead of O(n^3).
    # In practice the constant factors and extra matrix additions make
    # Strassen slower than the standard method for small n - it only wins
    # once n is large enough that the exponent difference outweighs the
    # overhead.


if __name__ == "__main__":
    main()
