import os
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SNAPSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def linear_search(arr, target):
    for item in arr:
        if item == target:
            return True
    return False

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

algorithms = {
    "binary_search": (binary_search, "O(log n)"),
    "linear_search": (linear_search, "O(n)"),
    "merge_sort": (merge_sort, "O(n log n)")
}

n_max = 10000
step = 1000
n_values = list(range(0, n_max + 1, step))

for name, (func, complexity) in algorithms.items():
    timings = []
    for n in n_values:
        arr = list(range(n, 0, -1)) if "sort" in name else list(range(n))
        start = time.perf_counter()
        if "sort" in name:
            func(arr)
        else:
            func(arr, -1)
        timings.append(time.perf_counter() - start)

    fig, ax = plt.subplots(figsize=(9, 5), dpi=120)
    ax.plot(n_values, timings, marker='o', markersize=4, linestyle='-', color='#1f77b4', label=f'{name} (Measured)')
    ax.set_title(f"Time Complexity: {name} ({complexity})", fontsize=14, pad=12)
    ax.set_xlabel("Input Size (n)", fontsize=11)
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc="upper left")
    plt.tight_layout()

    fig.savefig(os.path.join(SNAPSHOT_DIR, f"{name}_10000.png"), format="png")
    plt.close(fig)

print("Snapshots generated successfully!")