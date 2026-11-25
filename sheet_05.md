# Instrumentation and Analysis Methods – Exercise Sheet 5

**Handout:** 25th Nov 2026 **Due:** 9th Dec 2026

## Geant4 exercises

The Geant4 exercises are in the folder [geant4](geant4/README.md) of your IAM26 fork: update your fork with *Sync fork* on its GitHub page.

**GitHub Codespace (recommended).** The Geant4 exercises need their own Codespace. On the GitHub page of your fork click *Code*, *Codespaces*, then *…* → *New with options*, choose the dev container configuration *Geant4* and click *Create codespace*. This opens VS Code in your browser with ROOT and Geant4 already installed. The first start takes a few minutes; later you find the Codespace again under *Code*, *Codespaces*. You work with two notebooks; for both select the kernel *Python Environments* → `/opt/venv/bin/python`:

- [**geant4/tutorial.ipynb**](geant4/tutorial.ipynb): the event display. Run the cells from the top. The first cell compiles the tutorial application and creates `app`, the second loads a geometry and the cell with `event_gui(app)` shows the controls: choose the particle and the momentum and press *Next event*. Rotate the 3D view with the mouse and hover over a track to see the particle type and its momentum; `print_tracks(pmin=0.01)` lists all tracks of the last event above 10 MeV.
- [**geant4/macros.ipynb**](geant4/macros.ipynb): runs analysis macros like **dEdx.C** with `run_macro('dEdx.C')`. It shows the events and histograms while the macro runs and the canvases of the macro below the cell. The text output of the macro goes to `dEdx.log`.

Geant4 can be initialised only once per session: **restart the kernel** (*Restart* button of the notebook) before you load another geometry, after you changed a geometry file or a macro, and before you run another macro. ROOT commands are written in Python: `app->InitMC("geometry/pbbox")` becomes `app.InitMC('geometry/pbbox')`. To save a plot for your solution use e.g. `c2.SaveAs('energy.png')` for a canvas created in the notebook, or `ROOT.gROOT.FindObject('c1').SaveAs('hloss.png')` for a canvas created by a macro, and download the file with a right click in the file explorer of VS Code.

**VS Code on your own computer.** The same container as in the Codespace runs locally (about 6 GB disk space, at least 8 GB RAM). Install [Docker Desktop](https://www.docker.com/products/docker-desktop/), [VS Code](https://code.visualstudio.com/) and its extension *Dev Containers*. On Macs with Apple Silicon tick *Use Rosetta for x86_64/amd64 emulation on Apple Silicon* in the settings of Docker Desktop. Clone your fork, open the folder **IAM26** in VS Code and run *Dev Containers: Reopen in Container* from the command palette (Ctrl+Shift+P), choose the configuration *Geant4*. The first start downloads the image (about 1 GB). Then work with the notebooks as in the Codespace. Details are in [**geant4/README.md**](geant4/README.md) of your fork.

**Local installation with conda.** Follow the instructions in [**geant4/README.md**](geant4/README.md) of your fork (conda environment for Linux, macOS and Windows/WSL). Then start ROOT with the Geant4 interface and its graphical user interface in a terminal:

``` bash
conda activate g4tut
cd geant4
root -l run_g4.C
```

and use the C++ commands below on the ROOT prompt. Restart ROOT whenever the text says to restart the kernel. You can use the notebooks locally as well (`jupyter notebook` in the folder **geant4**).

## Exercise 1: Interaction of particles and matter (8 points)

Please upload your solutions (text/plots) to Moodle for this exercise. Do not forget to write the names of all team members on the solution.

a) (2 points) Let's start with shooting muons in a block of lead. Load the geometry describing the lead block into Geant4 (this is the second cell of **tutorial.ipynb**):

   ``` python
   app.InitMC('geometry/pbbox')    # notebook
   ```
   ``` cpp
   app->InitMC("geometry/pbbox");  // ROOT prompt
   ```

   This creates a cube of lead with a length of 20 cm. Now use the controls of `event_gui(app)` (locally: the GUI) to generate events with muons (*mu-* or *mu+*). What do you observe for muons with a momentum of

   0.3 GeV, 1 GeV, 10 GeV, 100 GeV and 1000 GeV?

   Which interactions do you see predominantly depending on the energy? Use the track colours (listed in the notebook) and `print_tracks` to identify the secondary particles.

b) (1 point) Now restart the kernel (ROOT) and load a different geometry by changing the second cell to

   ``` python
   app.InitMC('geometry/cubox')    # notebook
   ```
   ``` cpp
   app->InitMC("geometry/cubox");  // ROOT prompt
   ```

   This is a copper box with 0.2 cm length. Generate one event with a muon at $p = 1$ GeV. Then draw the predefined histogram `hPrimaryEnergy` with the last cell of **tutorial.ipynb** or on the ROOT prompt with

   ``` cpp
   new TCanvas();
   hPrimaryEnergy->Draw()
   ```

   The plot shows the energy of the muon along its path through our little experiment. Read off the energy of the muon after it left the copper and compute the energy loss $dE/dx$ in MeV cm²/g. The loss is small compared to the energy: hover over the markers of the histogram to read off the values. The density of copper is 8.96 g/cm³. Compare your result to the plot from the slides "Interaction of particles and matter" (p 10).\
   Change to pions to compare the result to the plot on page 11. Note: the histogram adds up all events, so reset it before you generate the pion event with

   ``` python
   app.FinishRun()    # notebook
   ```
   ``` cpp
   app->FinishRun();  // ROOT prompt
   ```

c) (1 point) Change the material in **geometry/cubox.C** to "Fe" and "Pb" by modifying the `GetMedium` line (open the file in the editor of VS Code and save it). Restart the kernel after each change and again compute the energy loss for muons and compare it to the plot in the lecture (p 13). The densities are 7.87 g/cm³ for iron and 11.35 g/cm³ for lead.

d) (1 point) Generate 1000 events for copper by starting from the macro **dEdx.C**, plot the energy loss for the muons and fit it with the appropriate function. Note: Please do not forget to change the material in **geometry/cubox.C** back to copper. We now use the energy deposited in our copper box instead of the energy loss from the histogram. Why can the deposited energy be smaller than the energy loss of the muon? Give the most probable value from your fit and the mean of the histogram. Run the macro in **macros.ipynb** (restart the kernel and run the setup cell before, and again after every change of **dEdx.C**) with

   ``` python
   run_macro('dEdx.C')
   ```

   or locally in a terminal with

   ``` bash
   root -l run_g4.C dEdx.C
   ```

   In a terminal of the Codespace there is no graphics; there you can run the macro in batch mode with `root -l -b -q run_g4.C dEdx.C` and save the canvases with `SaveAs` in the macro.

e) (3 points) Repeat this for $\beta\gamma$ values of 0.1, 1, 10, 100, 1000 and 10000 by changing the momentum in **dEdx.C**. Estimate the mean and the most probable energy loss for each $\beta\gamma$ value and compare them with the energy loss predictions for thin layers (p 20). Note that the mean depends on the range of the histogram: entries above 10 MeV are not included. What happens at $\beta\gamma = 0.1$, and why?
