# demo-boids
Demonstration repository of the boids simulation project of my partner's ([@Jacqueline-Ulken](https://github.com/Jacqueline-Ulken))
and mine (part of the course ESC202 simulations in the natural sciences)

The code was completely self-written and the equations taken from the paper contained in this repository. Refer to the presentation PDF for more detailed sources.

Testing image embedding 1 - absolute link:
![Boids swarming about (presentation title slide) 1](https://github.com/radRoy/demo-boids/blob/master/Boids_pdf_title_screen.png)

Testing image embedding 2 - relative link:
![Boids swarming about (presentation title slide) 2](demo-boids/Boids_pdf_title_screen.png)

![Boids swarming about (presentation title slide) 1](https://github.com/radRoy/demo-boids/blob/master/Boids.pdf)

## Background of this project
Read the presentation PDF `Boids.pdf` and refer to the two video files documenting the progress & problems along the way

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
