# Geant4 exercises

Simulation exercises with Geant4, driven from ROOT through the Virtual Monte Carlo
(`TutorialApplication`). Get them into your fork with *Sync fork*.

## Option 1: GitHub Codespace (recommended)

The Geant4 exercises need their own Codespace with ROOT and Geant4:
on the GitHub page of your fork click *Code*, *Codespaces*, then *…* →
*New with options*, choose the dev container configuration **Geant4** and
click *Create codespace*. It is ready after a few minutes. Later you find it
again under *Code*, *Codespaces*.

Open `geant4/tutorial.ipynb` and choose the kernel
*Python Environments* → `/opt/venv/bin/python`. The notebook shows the
event display. The analysis macros run in `geant4/macros.ipynb`, which shows the
events and histograms while the macro runs and its canvases below the cell
(one macro per kernel session; the output goes to e.g. `dEdx.log`):

```python
run_macro('dEdx.C')
```

In the terminal (no graphics in a Codespace) macros run in batch mode:

```
cd geant4
root -l -b -q run_g4.C dEdx.C
```

## Option 2: VS Code with a local dev container (Linux, Windows, macOS)

The same container as in the Codespace runs on your own computer. You need
about 6 GB of free disk space and at least 8 GB of RAM.

Once:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   (Linux: Docker Engine is enough) and start it.
   * **Windows:** Docker Desktop uses WSL2; install it with `wsl --install` in
     PowerShell if Docker Desktop asks for it.
   * **macOS with Apple Silicon (M1–M4):** the image exists only for Intel/AMD
     processors. In Docker Desktop, *Settings* → *General*, tick
     *Use Rosetta for x86_64/amd64 emulation on Apple Silicon*.
   * Give Docker at least 4 GB of memory (*Settings* → *Resources*).
2. Install [VS Code](https://code.visualstudio.com/) and its extension
   **Dev Containers** (`ms-vscode-remote.remote-containers`).
3. Clone your fork, e.g. in a terminal:
   ```
   git clone https://github.com/<your user name>/IAM26.git
   ```

Every time:

1. Open the folder `IAM26` in VS Code (*File* → *Open Folder…*).
2. Command palette (Ctrl+Shift+P, macOS: Cmd+Shift+P) →
   *Dev Containers: Reopen in Container* → choose **Geant4**.
   The first time this downloads the image (about 1 GB) and takes a few minutes.
3. Work as in the Codespace: open `geant4/tutorial.ipynb` and choose the kernel
   *Python Environments* → `/opt/venv/bin/python`.

Your files stay in the `IAM26` folder on your computer; commit and push as usual.
*Dev Containers: Reopen Folder Locally* leaves the container.
To get updates of the tutorial: *Sync fork* on GitHub, then `git pull`.

## Option 3: local installation with conda (Linux, Windows/WSL, macOS)

Install [Miniforge](https://github.com/conda-forge/miniforge), then once:

```
cd geant4
conda env create -f environment.yml
```

* **Windows:** use WSL2 (`wsl --install` in PowerShell) and install Miniforge for
  Linux inside Ubuntu. Windows 11 shows the ROOT windows directly.
* **macOS with Apple Silicon (M1–M4):** some packages exist only for Intel Macs, so
  create the environment with
  `CONDA_SUBDIR=osx-64 conda env create -f environment.yml` (runs via Rosetta).

Every time you open a new terminal:

```
conda activate g4tut
cd geant4
root -l run_g4.C
```

This opens the GUI; load a geometry at the ROOT prompt, e.g.

```
app->InitMC("geometry/pbbox")
```

and generate events with *Next Event*. Without a display (e.g. via ssh) use
`root -l --web run_g4.C` or the notebook `tutorial.ipynb` (`jupyter notebook`).

## Notes

* Geant4 can be initialised only once: restart ROOT (or the notebook kernel)
  before loading another geometry.
* The tutorial code in `src/` is compiled automatically by `run_g4.C`;
  later analysis macros are compiled with a trailing `+`, e.g. `run_macro('tracking2.C+')`.
* The physics list is set in `g4Config.C`.
* If VS Code shows `Cannot read properties of undefined (reading 'ipywidgetsKernel')`
  instead of the buttons, or the notebook hangs on a kernel restart: run the cell
  again; if that does not help, use *Developer: Reload Window* from the command
  palette, or stop and restart the Codespace / dev container. This is a bug in
  VS Code's Jupyter extension, not in your code.
