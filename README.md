# EIT Reconstruction Benchmark Dashboard

[![CI](https://github.com/Tannaz2001/ktc-eit-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/Tannaz2001/ktc-eit-framework/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

**A benchmarking platform for Electrical Impedance Tomography (EIT) image-reconstruction algorithms.**

---

## What is this?

This project runs multiple algorithms that try to "see inside" an object using only
electrical measurements taken at its surface — a technique called **EIT**. Think of it like
an X-ray, but using electricity instead of radiation.

The algorithms are scored on how accurately they reconstruct an image of what's inside
a water tank (the test object). This dashboard lets you:

- **Run** multiple reconstruction algorithms at once
- **Compare** their scores side by side on a leaderboard
- **Add your own algorithm** in three different ways (see [Adding Your Own Method](#7-adding-your-own-method))
- **Export** a report explaining the results in plain language

> **You do not need to understand EIT to use this dashboard.** You only need to follow the
> setup steps below.

---

## Table of Contents

1. [Before You Start — Install the Prerequisites](#1-before-you-start--install-the-prerequisites)
2. [Get the Code](#2-get-the-code)
3. [Set Up the Python Environment](#3-set-up-the-python-environment)
4. [Run the Dashboard](#4-run-the-dashboard)
5. [What You Will See](#5-what-you-will-see)
6. [Run the Benchmark](#6-run-the-benchmark)
7. [Adding Your Own Method](#7-adding-your-own-method)
   - [Path A — Upload a Bundle (.zip)](#path-a--upload-a-bundle-zip)
   - [Path B — Link an Existing Docker Image](#path-b--link-an-existing-docker-image)
   - [Path C — Drop in a Python Script](#path-c--drop-in-a-python-script)
8. [How Scoring Works](#8-how-scoring-works)
9. [Project Structure](#9-project-structure)
10. [Troubleshooting](#10-troubleshooting)
11. [Team](#11-team)

---

## 1. Before You Start — Install the Prerequisites

You need two things installed on your computer before anything else will work.

### Python 3.10 or newer

1. Go to <https://www.python.org/downloads/>
2. Download the latest **Python 3.x** release for your operating system
3. **Windows users:** during installation, tick the checkbox that says **"Add Python to PATH"**
   before clicking Install — if you miss this, commands like `python` will not work in
   your terminal
4. Open a terminal (PowerShell on Windows, Terminal on Mac/Linux) and confirm it worked:
   ```
   python --version
   ```
   You should see something like `Python 3.11.4`. If you see an error, Python is not on
   your PATH — reinstall and tick that checkbox.

### Git

1. Go to <https://git-scm.com/downloads>
2. Download and install Git (all default options are fine)
3. Confirm it worked:
   ```
   git --version
   ```

### Docker Desktop *(only needed if you want to add new methods via ZIP upload or image link)*

If you only want to **run** the existing built-in algorithms you can skip Docker for now.
If you want to **add a new method** using Path A or Path B below, you will need it.

1. Go to <https://www.docker.com/products/docker-desktop>
2. Download and install **Docker Desktop** (free)
3. After installation, open Docker Desktop from your Start menu / Applications and wait
   until the status in the app reads **"Docker Desktop is running"**
4. Confirm in a terminal:
   ```
   docker --version
   ```

---

## 2. Get the Code

Open a terminal, navigate to the folder where you want to put the project, then run:

```powershell
git clone https://github.com/Tannaz2001/ktc-eit-framework.git
cd ktc-eit-framework
```

This downloads the entire project including the evaluation dataset — no separate download
is needed.

---

## 3. Set Up the Python Environment

A **virtual environment** keeps this project's packages separate from everything else on
your computer. Think of it as a private sandbox just for this project.

**Run these commands in order, from inside the project folder:**

```powershell
# Step 1 — Create the sandbox (run this once, ever)
python -m venv venv

# Step 2 — Activate the sandbox
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Mac / Linux:
source venv/bin/activate
```

After Step 2 your terminal prompt will gain a `(venv)` prefix like this:

```
(venv) C:\ktc-eit-framework>
```

That prefix means the sandbox is active. If you ever open a new terminal window you
must run Step 2 again — the sandbox does not stay active across terminal sessions.

```powershell
# Step 3 — Install all required packages into the sandbox
pip install -r requirements.txt

# Step 4 — Install the framework itself (REQUIRED — do not skip)
pip install -e .
```

> **Why is Step 4 required?**
> Without it, the app crashes with `ModuleNotFoundError: No module named 'ktc_framework'`.
> `pip install -e .` tells Python where to find the framework code that lives in `src/`.

---

## 4. Run the Dashboard

With your virtual environment active (you see `(venv)` in the prompt), run:

```powershell
streamlit run app.py
```

After a few seconds your terminal will print something like:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

Open that URL in your browser. The **EIT Bench** dashboard will load.

> **"streamlit: command not found"?**
> Your virtual environment is not active. Run `.\venv\Scripts\Activate.ps1` (Windows) or
> `source venv/bin/activate` (Mac/Linux) and try again.

> 📸 **Screenshot:** Paste a screenshot of the dashboard home page here so new users know
> what to expect on first load (before any benchmark has been run).

---

## 5. What You Will See

The dashboard has a **sidebar on the left** and **chart panels on the right**.

### Sidebar

| Section | What it does |
|---|---|
| **Dataset Settings** | Points the app at your data files. Defaults work out of the box. Click "Validate paths" to confirm everything is found. |
| **Run Benchmark** | Runs the selected algorithms and generates scores. |
| **Methods** | Tick-boxes to choose which algorithms to compare in the charts. |
| **Metrics** | Tick-boxes to choose which scores to display. |

### Main panel (tabs across the top)

| Tab | What it shows |
|---|---|
| **Leaderboard** | Ranked list of algorithms by score |
| **Degradation** | How each algorithm's score changes as the problem gets harder (levels 1 → 7) |
| **Metrics** | Breakdown of individual metrics (Dice, IoU, etc.) per method |
| **Radar** | Spider-chart comparing all methods across all metrics at once |
| **Geometry** | Did the algorithm find each inclusion in the right place? |
| **Images** | Side-by-side: algorithm output vs. ground truth |

> 📸 **Screenshot:** Paste a screenshot here showing a populated leaderboard after a
> benchmark run, so new users know what the end result looks like.

---

## 6. Run the Benchmark

### Via the dashboard (easiest)

In the sidebar, click **"Run all methods"**.

The terminal prints a **METHOD DISCOVERY REPORT** immediately — before any reconstruction
starts — that lists every scheduled method and whether it was found:

```
── Method Discovery ──────────────────────────────────
  Registered in registry : 6 methods
  Scheduled for execution: 6 methods
    ✓ KTC2023_CUQI4              (KTC2023_CUQI4.py)
    ✓ BackProjection             (builtin)
    ✓ CompetitionCNN             (builtin)
    ✓ LinearDifferenceReconstruction  (builtin)
    ✓ KTC2023_CUQI2_main         (KTC2023-CUQI2-main)
    ✓ KTC2023_CUQI1              (KTC2023_CUQI1.py)
─────────────────────────────────────────────────────
```

A `✓` next to every method means everything is ready. A `✗` means a file is missing —
see [Troubleshooting](#10-troubleshooting).

A full run (6 methods × 7 levels × 3 samples = 126 reconstructions) takes roughly
**20–40 minutes** on a typical laptop. The dashboard refreshes automatically when done.

### Via the command line (alternative)

```powershell
python run.py --config configs/ktc_all_methods.yaml
```

---

## 7. Adding Your Own Method

You can plug any reconstruction algorithm into the benchmark in **three ways**. Pick the
one that matches how your code is packaged:

| | Path | Best for |
|---|---|---|
| **A** | [Upload a Bundle (.zip)](#path-a--upload-a-bundle-zip) | New algorithm you wrote — you package it as a zip and the system builds a Docker image automatically |
| **B** | [Link an Existing Docker Image](#path-b--link-an-existing-docker-image) | Algorithm already published to Docker Hub or a container registry |
| **C** | [Drop in a Python Script](#path-c--drop-in-a-python-script) | A plain `.py` script that reads data from a folder and writes `.mat` output files |

All three paths end with your method appearing in the **Methods** sidebar so you can tick
it and run it alongside the built-in baselines.

---

### Path A — Upload a Bundle (.zip)

The dashboard builds a Docker image from your zip in the background. You write your
algorithm in plain Python; the system handles containerisation.

#### Prerequisites

Docker Desktop must be **running** before you upload (the Docker Desktop window must show
"Docker Desktop is running", not a grey/stopped state).

#### Step 1 — Create the zip file

Your zip must contain **exactly** these files. The filenames are fixed — do not rename them:

```
my_method.zip
├── algorithm.py      ← your reconstruction code (required)
├── requirements.txt  ← Python packages your code needs (required, may be empty)
└── ktc_config.yml    ← method name and base Docker image (optional but recommended)
```

---

**`algorithm.py`** — must define a function named `reconstruct(batch)`.

The `batch` object has these fields:

| Field | Type | Description |
|---|---|---|
| `batch.voltages` | numpy array, shape (76,) | Voltage measurements from the 32 electrodes |
| `batch.injection_patterns` | numpy array, shape (32, 76) | Which electrodes are active at each step |
| `batch.level` | int, 1–7 | Difficulty level (higher = fewer electrodes = harder) |
| `batch.ground_truth` | numpy array, shape (256, 256) | Ground-truth mask (labels 0/1/2) |
| `batch.mesh` | object or None | FEM mesh (can be ignored if your method does not need it) |
| `batch.reference_voltages` | numpy array or None | Empty-tank reference voltages |

Your function must return a **numpy array of shape (256, 256)** with integer labels:
- `0` = background (water)
- `1` = resistive inclusion (plastic)
- `2` = conductive inclusion (metal)

Minimal working example:

```python
# algorithm.py

import numpy as np

def reconstruct(batch):
    """
    Reconstruct a 256x256 segmentation map from EIT measurements.

    Parameters
    ----------
    batch : DataBatch
        Contains .voltages, .injection_patterns, .level, .ground_truth, .mesh

    Returns
    -------
    numpy.ndarray, shape (256, 256), dtype uint8
        Segmentation map: 0=background, 1=resistive, 2=conductive
    """
    # Replace the line below with your actual algorithm.
    # Returning all zeros means "predict empty tank everywhere" (baseline = 0 KTC score).
    return np.zeros((256, 256), dtype=np.uint8)
```

---

**`requirements.txt`** — list any pip packages your algorithm needs, one per line.
`numpy` and `scipy` are always available — you only need to list extras.

```
# requirements.txt — leave this file empty if your algorithm only uses numpy/scipy
scikit-learn
matplotlib
```

---

**`ktc_config.yml`** — sets the method name and Docker base image.

```yaml
# ktc_config.yml
name: MyAlgorithm            # name shown in the dashboard (letters/numbers/underscores only)
base_image: python:3.10-slim # base Docker image; use pytorch/pytorch if you need PyTorch
```

If you omit this file the method name defaults to the zip filename with special characters
replaced by underscores.

---

#### Step 2 — Upload via the dashboard sidebar

1. Open the dashboard in your browser
2. Scroll down in the sidebar to **"Add Method"**
3. Click the **"Upload Bundle (.zip)"** tab
4. Click the upload area and select your zip file

A confirmation message appears immediately:
> *"⏳ Building 'MyAlgorithm' in the background — dashboard stays live. Refresh to check status."*

> 📸 **Screenshot:** Show the sidebar "Add Method" section with the "Upload Bundle" tab
> active and a zip file selected, so new users know what to click.

#### Step 3 — Wait for the build

The Docker image builds in the background. You can keep using the dashboard. After
1–5 minutes (depending on your `requirements.txt`), refresh the page.

Your method appears in the **Methods** sidebar with one of these states:

| Badge | Meaning |
|---|---|
| *(no badge)* | Build succeeded — ready to run |
| **⏳ Building…** | Still in progress — wait and refresh again |
| **⚠ Build failed** | Something in your zip was invalid — check package names in `requirements.txt` |

> 📸 **Screenshot:** Show the Methods sidebar with a newly added method appearing
> (no badge = ready), alongside the built-in baselines.

#### Step 4 — Run it

Tick your method in the Methods checklist and click **"Run all methods"** in the sidebar,
or click the **Run** button next to your method name.

---

### Path B — Link an Existing Docker Image

Use this if your algorithm is already packaged and published as a Docker image (e.g., on
Docker Hub, GHCR, or built locally).

#### What your image's entrypoint must do

The benchmark calls your container like this:

```bash
docker run --rm -v /tmp/ktc_run:/data YOUR_IMAGE_TAG /data/input.json /data/output.npy
```

Your entrypoint must:
1. Read the file at the first argument (`/data/input.json`)
2. Write the reconstruction to the file at the second argument (`/data/output.npy`)

**Input format (`input.json`):**

```json
{
  "voltages":            { "data": "<base64-bytes>", "dtype": "float32", "shape": [76] },
  "injection_patterns":  { "data": "<base64-bytes>", "dtype": "float32", "shape": [32, 76] },
  "ground_truth":        { "data": "<base64-bytes>", "dtype": "uint8",   "shape": [256, 256] },
  "level":               3,
  "sample_id":           "data1",
  "mesh":                null,
  "reference_voltages":  null,
  "measurement_patterns": null
}
```

To decode a numpy array from the JSON inside your container:

```python
import json, base64, numpy as np

with open("/data/input.json") as f:
    payload = json.load(f)

def decode(d):
    """Decode a base64-encoded numpy array from the JSON payload."""
    raw = base64.b64decode(d["data"])
    return np.frombuffer(raw, dtype=d["dtype"]).reshape(d["shape"])

voltages = decode(payload["voltages"])
level    = int(payload["level"])
```

**Output format (`output.npy`):**

```python
import numpy as np

reconstruction = np.zeros((256, 256), dtype=np.uint8)  # your result here
np.save("/data/output.npy", reconstruction)
```

#### Steps

1. Make sure the image is available locally:
   ```powershell
   docker pull your-username/your-image:latest
   # or if built locally, verify it shows up:
   docker images
   ```

2. In the dashboard sidebar click **"Add Method"** → **"Link Existing Image"** tab

3. Fill in all three fields:

   | Field | Example | Notes |
   |---|---|---|
   | **Method Name** | `MyDockerMethod` | Letters, numbers, underscores only — no spaces |
   | **Docker Image Tag / URL** | `your-username/my-eit-method:latest` | Exact tag as shown in `docker images` |
   | **Author** | `Your Name` | Optional, shown in the registry |

4. Click **"Link Image"**

Your method is registered immediately (no build wait) and appears in the Methods
checklist.

> 📸 **Screenshot:** Show the "Link Existing Image" tab with all three fields filled in,
> just before clicking the button.

---

### Path C — Drop in a Python Script

Use this if your algorithm is a plain Python script that reads EIT data from a folder and
writes `.mat` result files — the same format used by all KTC 2023 competition submissions.
No Docker is needed.

#### What your script must look like

Your script must follow the **KTC CLI contract**. Three things are non-negotiable:

1. `import argparse` somewhere at the top
2. A `def main():` function that parses exactly three arguments
3. `if __name__ == "__main__": main()` at the very bottom

**The three arguments the framework always passes, in order:**

| Argument | What it contains |
|---|---|
| `inputFolder` | Path to a folder containing `data1.mat`, `data2.mat`, `data3.mat` (voltage measurements) and `ref.mat` (empty-tank reference) |
| `outputFolder` | Path where you must write your output `.mat` files named `1.mat`, `2.mat`, `3.mat` |
| `categoryNbr` | Integer 1–7 representing the difficulty level |

**Template — copy this and replace the reconstruction logic:**

```python
# my_method.py
# Drop this file into external_methods/ and click "Refresh methods" in the dashboard.

import argparse
import glob
import os

import numpy as np
import scipy.io


def main():
    # --- Parse the three positional arguments ---
    # The framework calls: python my_method.py <inputFolder> <outputFolder> <categoryNbr>
    parser = argparse.ArgumentParser(description="KTC EIT reconstruction method")
    parser.add_argument("inputFolder",  help="Folder with data*.mat and ref.mat")
    parser.add_argument("outputFolder", help="Folder to write reconstruction .mat files")
    parser.add_argument("categoryNbr",  help="Difficulty level (1=easiest, 7=hardest)")
    args = parser.parse_args()

    level = int(args.categoryNbr)

    # --- Load the empty-tank reference voltages ---
    ref_path = os.path.join(args.inputFolder, "ref.mat")
    ref_mat  = scipy.io.loadmat(ref_path, squeeze_me=True)
    ref_voltages = ref_mat["Uelref"].flatten()   # shape (76,) — voltages with nothing in the tank

    # --- Find all data files for this level/sample group ---
    data_files = sorted(glob.glob(os.path.join(args.inputFolder, "data*.mat")))

    os.makedirs(args.outputFolder, exist_ok=True)

    for i, data_file in enumerate(data_files):
        mat      = scipy.io.loadmat(data_file, squeeze_me=True)
        voltages = mat["Uel"].flatten()           # shape (76,) — voltages with inclusion in tank
        diff     = voltages - ref_voltages        # difference signal (standard EIT approach)

        # =====================================================================
        # YOUR RECONSTRUCTION ALGORITHM GOES HERE
        # =====================================================================
        # Inputs available:
        #   voltages     — raw voltage measurements, shape (76,)
        #   diff         — difference from empty tank, shape (76,)
        #   ref_voltages — reference voltages, shape (76,)
        #   level        — difficulty 1–7
        #
        # Output required:
        #   reconstruction — numpy array shape (256, 256), dtype uint8
        #   Values: 0=background, 1=resistive (plastic), 2=conductive (metal)
        # =====================================================================
        reconstruction = np.zeros((256, 256), dtype=np.uint8)  # ← replace this line

        # --- Save the output (filename MUST be 1.mat, 2.mat, 3.mat, ...) ---
        out_path = os.path.join(args.outputFolder, f"{i + 1}.mat")
        scipy.io.savemat(out_path, {"reconstruction": reconstruction})
        print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
```

#### Steps

1. Save your completed script with a `.py` extension

2. Copy it into the `external_methods/` folder at the project root:
   ```powershell
   # Windows PowerShell:
   copy C:\path\to\my_method.py .\external_methods\my_method.py

   # Mac / Linux:
   cp /path/to/my_method.py ./external_methods/my_method.py
   ```

3. In the dashboard sidebar, click **"Refresh methods"** — the dashboard scans
   `external_methods/` and your method name appears in the Methods checklist

4. Tick your method and click **"Run all methods"**

> **Important:** Your script runs on your **local Python install**, not inside Docker.
> If your script imports packages that are not in `requirements.txt`, install them first:
> ```powershell
> pip install <package-name>
> ```

> 📸 **Screenshot:** Show the Methods sidebar *before* and *after* clicking
> "Refresh methods" so new users can see their method appear.

---

## 8. How Scoring Works

Each reconstruction is compared to the known ground truth using the official **KTC score**:

| Score | Meaning |
|------:|---------|
| **1.0** | Perfect reconstruction |
| **0.0** | No better than returning an all-zero (empty tank) image |
| **< 0** | Worse than predicting an empty tank |

The KTC score is based on **SSIM** (structural similarity), computed separately for the
resistive (plastic) and conductive (metal) regions, then averaged.

Additional metrics shown in the dashboard:

| Metric | What it measures |
|---|---|
| **Dice** | How much the predicted inclusion area overlaps the true area (0–1) |
| **IoU** | Intersection over Union — stricter version of Dice |
| **Hull IoU** | Whether the inclusion was found in the right geometric position |
| **Runtime (ms)** | How long each reconstruction took |

All methods are also assigned **letter grades (A–D)** for quick at-a-glance comparison.

---

## 9. Project Structure

```
ktc-eit-framework/
│
├── app.py                          # Streamlit dashboard — the main UI entry point
├── run.py                          # Command-line benchmark runner
│
├── configs/
│   ├── ktc_all_methods.yaml        # Benchmark config: which methods/levels/samples to run
│   └── registered_methods.json     # Registry of Docker-based methods (auto-managed, do not edit)
│
├── external_methods/               # Drop-in external algorithm files (Path C scripts go here)
│   ├── KTC2023_CUQI1.py            # Example: legacy KTC competition CLI script
│   ├── KTC2023_CUQI4.py            # Example: legacy KTC competition CLI script
│   └── KTC2023-CUQI2-main/         # Example: bundle-style method with method.yaml manifest
│
├── src/ktc_framework/
│   ├── methods/                    # Built-in algorithms (BackProjection, CompetitionCNN, …)
│   ├── adapters/
│   │   ├── docker_builder.py       # Builds Docker images (Path A) and links images (Path B)
│   │   ├── cli_plugin_wrapper.py   # Wraps Path C scripts so the runner can call them
│   │   └── plugin_detector.py      # Detects which contract a .py file follows
│   ├── runner/
│   │   └── experiment_runner.py    # Loops over methods × levels × samples
│   ├── metrics/                    # KTC score, Dice, IoU, composite score
│   └── reporting/                  # HTML report generator
│
├── EvaluationData/                 # KTC 2023 evaluation dataset (included — no download needed)
│   └── evaluation_datasets/
│       ├── level1/ … level7/       # Voltage .mat files per level
│       └── GroundTruths/           # Ground-truth segmentation masks
│
├── Codes_Matlab/                   # Training data and FEM mesh files
├── outputs/                        # Benchmark results (auto-generated on first run)
└── requirements.txt                # Python dependencies
```

---

## 10. Troubleshooting

### `ModuleNotFoundError: No module named 'ktc_framework'`

You skipped or forgot `pip install -e .`. With your venv active, run:
```powershell
pip install -e .
```

### `streamlit: command not found`

Your virtual environment is not active. Run:
```powershell
# Windows:
.\venv\Scripts\Activate.ps1
# Mac / Linux:
source venv/bin/activate
```
Then try `streamlit run app.py` again.

### `ModuleNotFoundError: No module named 'filelock'`

```powershell
pip install filelock
```

### Dashboard shows "No data" everywhere

No benchmark has been run yet. Click **"Run all methods"** in the sidebar, or run:
```powershell
python run.py --config configs/ktc_all_methods.yaml
```

### Benchmark shows "No data" for some methods but not others

Check the terminal for the METHOD DISCOVERY REPORT printed at the start of the run.
Look for `✗` entries — those methods failed to load.

| What the terminal says | Cause | Fix |
|---|---|---|
| `✗ NOT REGISTERED SomeName` | Method file is missing from `external_methods/` | Copy the file there and click "Refresh methods" |
| `FileNotFoundError: data1.mat` | `EvaluationData/` folder is missing or in the wrong location | Confirm the folder exists at the project root |
| `docker run failed` | Docker image was not built yet, or Docker is not running | Wait for the ⏳ badge to clear; check Docker Desktop is open |

### "Validate paths" shows all ERR

Click **Dataset Settings** in the sidebar and confirm **Dataset root** is set to
`EvaluationData`. Click **"Validate paths"** again.

### My Path C script runs but scores all zeros

Your script is being called correctly but your reconstruction logic is returning zeros.
Check `outputs/failures.json` for detailed error messages after a run. Also verify that
your output `.mat` file uses the key name `reconstruction` (that is the exact name the
scorer looks for).

### Path A build shows "⚠ Build failed"

Common causes:
- A package name in `requirements.txt` is misspelled (e.g., `sklearn` instead of
  `scikit-learn`)
- Your `algorithm.py` has a syntax error
- Docker Desktop is not running

Delete the method from the sidebar (Manage Methods → Delete Method), fix the issue,
re-zip, and upload again.

### `CompetitionCNN` scores 0.000 or does not appear

`CompetitionCNN` requires TensorFlow, which is not in the base `requirements.txt`:
```powershell
pip install tensorflow
```

---

## 11. Team

Developed as a summer research project on EIT reconstruction benchmarking, using the
**Kuopio Tomography Challenge (KTC) 2023** dataset.

- **Dataset & challenge:** <https://www.fips.fi/KTC2023.php>
- **Team:**
  - Tannaz Inamdar
  - Areeba Masood
  - Sahil Khan
  - Syeda Ulya Seerat
