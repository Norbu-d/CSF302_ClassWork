"""
Lab 2 - Q3: Square Matrix Multiplication
CSF303 - Algorithm Design and Analysis

n must be a power of 2 (2, 4, 8, 16, ...).
Standard O(n^3) multiplication with a basic-operation counter.
See strassen.py for the divide-and-conquer alternative.
"""

import random


def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


def get_matrix(n, name):
    choice = input(f"Enter matrix {name} manually (m) or randomly (r)? ").strip().lower()
    if choice == "m":
        print(f"Enter {n} rows of {n} space-separated numbers for matrix {name}:")
        matrix = []
        for i in range(n):
            row = list(map(int, input(f"Row {i + 1}: ").split()))
            if len(row) != n:
                raise ValueError(f"Row must have exactly {n} numbers.")
            matrix.append(row)
        return matrix
    matrix = [[random.randint(1, 20) for _ in range(n)] for _ in range(n)]
    print(f"Matrix {name} (randomly generated):")
    print_matrix(matrix)
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print(row)


def multiply(a, b, n):
    """Standard triple-loop multiplication. Returns (result, basic_op_count)."""
    ops = 0
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += a[i][k] * b[k][j]
                ops += 2  # 1 multiply + 1 add per inner-loop step
            result[i][j] = total
    return result, ops


def main():
    while True:
        n = int(input("Enter matrix size n (must be a power of 2, e.g. 2, 4, 8, 16): "))
        if is_power_of_two(n):
            break
        print("n must be a power of 2. Try again.")

    a = get_matrix(n, "A")
    b = get_matrix(n, "B")

    result, ops = multiply(a, b, n)

    print("\nResultant Matrix (A x B):")
    print_matrix(result)
    print(f"\nBasic operation count (multiplications + additions): {ops}")

    # --- Analysis / Conclusion ---
    # Standard matrix multiplication is O(n^3): three nested loops each of
    # size n. The operation counter above scales as roughly 2*n^3 (one
    # multiply + one add per inner-loop iteration), confirming the cubic
    # growth. Strassen's algorithm (strassen.py) cuts this to about
    # O(n^2.807) by trading one of the eight sub-multiplications for extra
    # additions/subtractions - this only pays off for larger n, since the
    # overhead of splitting and recombining submatrices dominates at
    # small sizes.


if __name__ == "__main__":
    main()
