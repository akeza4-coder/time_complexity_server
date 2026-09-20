# Time Complexity Visualizer (Flask)

A Flask endpoint that times an algorithm for growing input sizes, plots the running time, saves a PNG snapshot locally, and returns the image as a base64 string in the JSON response.

---

## Sample Visualization

![Time Complexity linear_search](snapshots/linear_search_n10000_step1000_20260919_125314_477332.png)

---

## Features

- **Empirical Timing**: Measures algorithm execution speed across varying input sizes (N).
- **Matplotlib Visualization**: Plots input sizes (N) against execution time in seconds.
- **Snapshot Storage**: Automatically saves the generated PNG plot inside the snapshots/ directory.
- **Base64 JSON Response**: Returns the encoded graph directly in the JSON response payload.

---

## Setup & Execution

### 1. Install Requirements
``bash
pip install -r requirements.txt
``n
### 2. Run the Server
``bash
python app.py
``
