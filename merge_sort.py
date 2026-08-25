"""
Lab 2 - Q2: Merge Sort Analysis (Menu-Driven Program)
CSF303 - Algorithm Design and Analysis
"""

import csv
import random
import time
import matplotlib.pyplot as plt

array = []


def generate_array():
    global array
    n = int(input("Enter n: "))
    array = [random.randint(1, 10000) for _ in range(n)]
    print(f"Generated array of {n} random numbers.")


def display_array():
    if not array:
        print("Array is empty. Generate one first (option 1).")
        return
    print(array)


def merge_sort(arr):
    """Standard merge sort, ascending. Returns (sorted_arr, steps)."""
    steps = 0
    if len(arr) <= 1:
        return arr, steps
    mid = len(arr) // 2
    left, left_steps = merge_sort(arr[:mid])
    right, right_steps = merge_sort(arr[mid:])
    steps += left_steps + right_steps

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        steps += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    steps += (len(left) - i) + (len(right) - j)
    return merged, steps


def quicksort_desc(arr):
    """Quicksort producing descending order (any algorithm is allowed for
    descending per the spec)."""
    steps = 0
    if len(arr) <= 1:
        return arr, steps
    pivot = arr[len(arr) // 2]
    left, mid, right = [], [], []
    for x in arr:
        steps += 1
        if x > pivot:
            left.append(x)
        elif x < pivot:
            right.append(x)
        else:
            mid.append(x)
    left_sorted, ls = quicksort_desc(left)
    right_sorted, rs = quicksort_desc(right)
    steps += ls + rs
    return left_sorted + mid + right_sorted, steps


def sort_ascending():
    global array
    if not array:
        print("Array is empty. Generate one first (option 1).")
        return
    sorted_arr, steps = merge_sort(array)
    array = sorted_arr
    print(f"Sorted ascending: {array}")
    print(f"Step count: {steps}")


def sort_descending():
    global array
    if not array:
        print("Array is empty. Generate one first (option 1).")
        return
    sorted_arr, steps = quicksort_desc(array)
    array = sorted_arr
    print(f"Sorted descending: {array}")
    print(f"Step count: {steps}")


def time_complexity(kind):
    """kind: 'random', 'sorted', 'reverse' - times merge sort across sizes
    and plots time vs n."""
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    times = []
    steps_list = []

    for n in sizes:
        if kind == "random":
            arr = [random.randint(1, 100000) for _ in range(n)]
        elif kind == "sorted":
            arr = list(range(n))
        else:  # reverse-sorted
            arr = list(range(n, 0, -1))

        start = time.perf_counter()
        _, steps = merge_sort(arr)
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        steps_list.append(steps)
        print(f"n={n:>6}  time={elapsed:.6f}s  steps={steps}")

    csv_name = f"merge_sort_{kind}.csv"
    with open(csv_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "time_seconds", "steps"])
        writer.writerows(zip(sizes, times, steps_list))
    print(f"Saved step/time table to {csv_name}")

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times, marker="o")
    plt.xlabel("n")
    plt.ylabel("Time (s)")
    plt.title(f"Merge Sort Time Complexity - {kind} data")
    plt.grid(True)
    plt.tight_layout()
    fname = f"merge_sort_{kind}.png"
    plt.savefig(fname)
    print(f"Saved graph to {fname}")


def menu():
    while True:
        print("\n--- Merge Sort Menu ---")
        print("1. Generate n random numbers -> Array")
        print("2. Display Array")
        print("3. Sort Ascending (Merge Sort)")
        print("4. Sort Descending (any algorithm)")
        print("5. Time Complexity - ascending random data")
        print("6. Time Complexity - ascending already-sorted data")
        print("7. Time Complexity - ascending descending-sorted data")
        print("0. Exit")
        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, OSError):
            print("[No interactive input detected - exiting]")
            break

        if choice == "1":
            generate_array()
        elif choice == "2":
            display_array()
        elif choice == "3":
            sort_ascending()
        elif choice == "4":
            sort_descending()
        elif choice == "5":
            time_complexity("random")
        elif choice == "6":
            time_complexity("sorted")
        elif choice == "7":
            time_complexity("reverse")
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid option.")


# --- Analysis / Conclusion ---
# Merge sort is O(n log n) in the best, average, AND worst case, because it
# always splits the array exactly in half and always does a full O(n) merge
# pass at each of the log n recursion levels - it can't "skip work" on
# already-sorted input the way insertion sort can. So the random, sorted,
# and reverse-sorted timing curves should look similar and all follow n log n
# growth. Quicksort (used above for descending order) is usually faster than
# merge sort in practice on random data, but its naive middle-pivot choice
# can degrade toward O(n^2) on already-sorted or reverse-sorted input.

if __name__ == "__main__":
    menu()
