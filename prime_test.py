"""
Lab 2 - Q1: Prime Number Testing
CSF303 - Algorithm Design and Analysis

Compares Naive (O(n)) vs Optimized (O(sqrt n)) primality tests.
Records step counts, saves results to CSV, and plots a comparison graph.
Also includes the optional Sieve of Eratosthenes.
"""

import csv
import math
import random
import matplotlib.pyplot as plt


def is_prime_naive(n):
    """Check divisibility from 2 to n-1. Returns (is_prime, steps)."""
    steps = 0
    if n < 2:
        return False, steps
    for i in range(2, n):
        steps += 1
        if n % i == 0:
            return False, steps
    return True, steps


def is_prime_optimized(n):
    """Check divisibility up to sqrt(n). Returns (is_prime, steps)."""
    steps = 0
    if n < 2:
        return False, steps
    i = 2
    while i * i <= n:
        steps += 1
        if n % i == 0:
            return False, steps
        i += 1
    return True, steps


def sieve_of_eratosthenes(limit):
    """Return (list_of_primes_up_to_limit, step_count). Optional part of Q1."""
    steps = 0
    is_p = [True] * (limit + 1)
    if limit >= 0:
        is_p[0] = False
    if limit >= 1:
        is_p[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        steps += 1
        if is_p[i]:
            for j in range(i * i, limit + 1, i):
                steps += 1
                is_p[j] = False
    primes = [i for i, p in enumerate(is_p) if p]
    return primes, steps


def get_numbers_from_user(min_count=10):
    """Prompt for at least min_count numbers. Falls back to a random demo
    set if stdin is not interactive, so the script never crashes when
    piped or auto-graded without a live terminal."""
    numbers = []
    print(f"Enter at least {min_count} numbers (blank line to finish once you've entered {min_count}):")
    try:
        while True:
            line = input(f"Number {len(numbers) + 1} (Enter to finish): ").strip()
            if line == "":
                if len(numbers) >= min_count:
                    break
                print(f"Need at least {min_count} numbers - you've entered {len(numbers)}.")
                continue
            numbers.append(int(line))
    except (EOFError, OSError):
        print(f"\n[No interactive input detected - using a random demo set of {min_count} numbers]")
        numbers = random.sample(range(1000, 200000), min_count)
    return numbers


def main():
    numbers = get_numbers_from_user(10)

    results = []
    for n in numbers:
        is_p_naive, naive_steps = is_prime_naive(n)
        is_p_opt, opt_steps = is_prime_optimized(n)
        results.append({
            "n": n,
            "is_prime": is_p_naive,
            "naive_steps": naive_steps,
            "optimized_steps": opt_steps,
        })

    print(f"\n{'n':>10} | {'Prime?':>7} | {'Naive Steps':>12} | {'Optimized Steps':>16}")
    print("-" * 55)
    for r in results:
        print(f"{r['n']:>10} | {str(r['is_prime']):>7} | {r['naive_steps']:>12} | {r['optimized_steps']:>16}")

    with open("prime_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "is_prime", "naive_steps", "optimized_steps"])
        writer.writeheader()
        writer.writerows(results)
    print("\nSaved step-count table to prime_results.csv")

    sorted_results = sorted(results, key=lambda r: r["n"])
    ns = [r["n"] for r in sorted_results]
    naive_steps = [r["naive_steps"] for r in sorted_results]
    opt_steps = [r["optimized_steps"] for r in sorted_results]

    plt.figure(figsize=(8, 5))
    plt.plot(ns, naive_steps, marker="o", label="Naive O(n)")
    plt.plot(ns, opt_steps, marker="s", label="Optimized O(sqrt n)")
    plt.xlabel("n")
    plt.ylabel("Step count")
    plt.title("Prime Testing: Naive vs Optimized Step Counts")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("prime_comparison.png")
    print("Saved graph to prime_comparison.png")

    limit = max(ns) if ns else 100
    primes, sieve_steps = sieve_of_eratosthenes(limit)
    print(f"\n[Optional] Sieve of Eratosthenes up to {limit}: found {len(primes)} primes in {sieve_steps} steps")

    # --- Analysis / Conclusion ---
    # The naive method does up to n-2 divisions in the worst case (n prime,
    # or n's smallest factor is close to n), so its step count grows
    # linearly with n: O(n). The optimized method only checks divisors up
    # to sqrt(n), so its step count grows as O(sqrt n) - much slower. The
    # gap between the two curves should widen sharply as n increases, with
    # the naive line pulling far above the optimized line on the graph.
    # The sieve is fastest when you need ALL primes up to a limit at once
    # (O(n log log n) total for that whole range), but it's wasted work if
    # you only need to test one specific large n.


if __name__ == "__main__":
    main()
