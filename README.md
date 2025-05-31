# demo-boids
Demonstration repository of the boids simulation project of my partner's ([@Jacqueline-Ulken](https://github.com/Jacqueline-Ulken)) and mine (part of the course ESC202 simulations in the natural sciences. Jacqueline is not visible as a contributor to this GitHub repository because it's just a cleaned up copy of the original one but optimised for readability. Jacqueline mainly wrote the class structures while I mainly handled the animation and code collaboration / version control aspects. But we helped each other out and the project was truly a balanced team effort. I wanted to create a simulation of some emergent behaviour and Jacqueline wanted to simulate animal flocking behaviour with an interest in group grazing behaviour. The grazing part was too complex for the scope of this project, unfortunately. However, we managed to combine our interests well and produced a clean end result showing emergent swarm behaviour based on a few simple rules. The emergence was defined as being erreicht if a swarm exhibits behaviour that an individual bird (or "bird-oid object" (boid)) does not, like moving through an obstacle as a swarm instead of avoiding it by going around it like individual boids do. This was achieved. To whitness it yourself, you can clone (download) this repository, set up and run the simulation yourself.

The code was completely self-written by Jacqueline and me in equal parts and the equations taken from the paper contained in this repository. Refer to [the presentation PDF](https://github.com/radRoy/demo-boids/blob/master/Boids.pdf) for a short project presentation from Introduction to Results and Outlook and for more detailed sources.

![Boids swarming about (presentation title slide) 1](https://github.com/radRoy/demo-boids/blob/master/Boids_pdf_title_screen.png)
Boids swarming about.

## Background of this project
Read the presentation PDF [`Boids.pdf`](https://github.com/radRoy/demo-boids/blob/master/Boids.pdf) and refer to the two video files documenting the progress & problems along the way.

## Running the simulation
- Download the code as a .zip file
- Extract to another folder
- Execute `main.py` by typing `python main.py` into your virtual environment (I used `py -m venv <envName>` to create mine).
  - You might need to install some python libraries like pygame and numpy

As of now, there is a `requirements.txt` file available, which I created when trying to run the `main.py` file from the Windows `cmd.exe` console.  
I can confirm that with an [installation of python 3.11.2](https://www.python.org/downloads/release/python-3112/), and by following the python.org guides for [installing packages with pip](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), [handling requirement files](https://pip.pypa.io/en/latest/user_guide/#requirements-files), and using my `requirements.txt` contained in this repo., this boids demo (interactive simulation) program should run.

The precise versions of packages / python itself do not have to be that specific. From memory, I think we developed this thing in python 3.8 & 3.9 and didn't synchronise our environments at all, even.

### Options to explore the boids' behaviours
- Press the right mouse button to place circular obstacles (symbolising trees)
- Press the spacebar twice to draw rectangular obstacles (symbolising walls)
- Play around with the parameter sliders and the buttons provided
