import os
import time
import io
import base64
import urllib.parse
from datetime import datetime
from collections import deque
from flask import Flask, request, jsonify
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "snapshots")
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# --- Data Structures ---

class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        return self._items.popleft()

    def is_empty(self):
        return len(self._items) == 0


# --- Algorithm Implementations ---

def linear_search(arr, target):
    for item in arr:
        if item == target:
            return True
    return False

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

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a

def nested_loops(n):
    total = 0
    for _ in range(n):
        for _ in range(n):
            total += 1
    return total

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

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def stack_reverse_array(n):
    s = Stack()
    for x in range(n):
        s.push(x)
    out = []
    while not s.is_empty():
        out.append(s.pop())
    return out

def queue_reverse_with_stack(n):
    q = Queue()
    s = Stack()
    for i in range(n):
        q.enqueue(i)
    while not q.is_empty():
        s.push(q.dequeue())
    while not s.is_empty():
        q.enqueue(s.pop())
    return q


# --- Algorithm Registry ---

ALGORITHM_REGISTRY = {
    "linear_search": "O(n)",
    "binary_search": "O(log n)",
    "bubble_sort": "O(n^2)",
    "nested_loops": "O(n^2)",
    "merge_sort": "O(n log n)",
    "insertion_sort": "O(n^2)",
    "stack_reverse": "O(n)",
    "queue_reverse": "O(n)"
}


# --- Benchmarking ---

def benchmark_algorithm(algo_name, n):
    target = -1
    if algo_name == "linear_search":
        arr = list(range(n))
        start = time.perf_counter()
        linear_search(arr, target)
        return time.perf_counter() - start
    elif algo_name == "binary_search":
        arr = list(range(n))
        start = time.perf_counter()
        binary_search(arr, target)
        return time.perf_counter() - start
    elif algo_name == "bubble_sort":
        arr = list(range(n, 0, -1))
        start = time.perf_counter()
        bubble_sort(arr)
        return time.perf_counter() - start
    elif algo_name == "nested_loops":
        start = time.perf_counter()
        nested_loops(n)
        return time.perf_counter() - start
    elif algo_name == "merge_sort":
        arr = list(range(n, 0, -1))
        start = time.perf_counter()
        merge_sort(arr)
        return time.perf_counter() - start
    elif algo_name == "insertion_sort":
        arr = list(range(n, 0, -1))
        start = time.perf_counter()
        insertion_sort(arr)
        return time.perf_counter() - start
    elif algo_name == "stack_reverse":
        start = time.perf_counter()
        stack_reverse_array(n)
        return time.perf_counter() - start
    elif algo_name == "queue_reverse":
        start = time.perf_counter()
        queue_reverse_with_stack(n)
        return time.perf_counter() - start
    return 0.0


# --- Routes ---

@app.route('/analyze', methods=['GET'])
def analyze():
    raw_algo = request.args.get('algo', '')
    raw_step = request.args.get('step', '')
    raw_n_max = request.args.get('n_max', '')

    if not raw_algo or not raw_step or not raw_n_max:
        return jsonify({
            "error": "Missing parameters: 'algo', 'step', and 'n_max' are required.",
            "supported_algorithms": list(ALGORITHM_REGISTRY.keys())
        }), 400

    algo = urllib.parse.unquote(raw_algo).strip().strip("'").strip('"').lower()
    step_str = raw_step.replace(",", "").strip()
    n_max_str = raw_n_max.replace(",", "").strip()

    if algo not in ALGORITHM_REGISTRY:
        return jsonify({
            "error": f"Algorithm '{algo}' is not supported.",
            "supported_algorithms": list(ALGORITHM_REGISTRY.keys())
        }), 400

    try:
        step = int(step_str)
        n_max = int(n_max_str)
    except ValueError:
        return jsonify({"error": "'step' and 'n_max' must be integers."}), 400

    if step <= 0 or n_max <= 0:
        return jsonify({"error": "'step' and 'n_max' must be positive integers."}), 400

    if step > n_max:
        return jsonify({"error": "'step' cannot exceed 'n_max'."}), 400

    if algo in ["bubble_sort", "insertion_sort", "nested_loops"] and n_max > 8000:
        return jsonify({
            "error": f"n_max={n_max} is too large for {algo} (O(n^2)). Use n_max <= 8000."
        }), 400

    n_values = list(range(0, n_max + 1, step))
    if n_values[-1] != n_max:
        n_values.append(n_max)

    timings = [benchmark_algorithm(algo, n) for n in n_values]

    fig, ax = plt.subplots(figsize=(9, 5), dpi=120)
    ax.plot(n_values, timings, marker='o', markersize=4, linestyle='-', color='#1f77b4', label=f'{algo} (Measured)')
    theoretical = ALGORITHM_REGISTRY[algo]
    ax.set_title(f"Time Complexity: {algo} ({theoretical})", fontsize=14, pad=12)
    ax.set_xlabel("Input Size (n)", fontsize=11)
    ax.set_ylabel("Execution Time (seconds)", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc="upper left")
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{algo}_n{n_max}_step{step}_{timestamp}.png"
    filepath = os.path.join(SNAPSHOT_DIR, filename)
    fig.savefig(filepath, format="png")

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    b64_image = base64.b64encode(buffer.read()).decode('utf-8')

    return jsonify({
        "algorithm": algo,
        "theoretical_complexity": theoretical,
        "n_max": n_max,
        "step": step,
        "local_snapshot_path": filepath,
        "data_points": [{"n": n, "time_seconds": t} for n, t in zip(n_values, timings)],
        "image_base64": b64_image
    }), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)