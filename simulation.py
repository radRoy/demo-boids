import numpy as np
from actors import Actor, Boid, Predator
from obstacles import Obstacle, Circle, Wall
from vectors2d import Vector


class Simulation:
    def __init__(self, window_size=(1, 1), nboids=10):
        self.window_size = Vector(window_size[0], window_size[1])
        self.center = Vector(window_size[0]/2, window_size[1]/2)
        self.actors = []
        self.flock = []
        self.predators = []
        self.obstacles = []
        self.nboids = nboids
        self.boid_settings = {"max_speed": 0.1, "view_distance": 50, "view_angle": np.pi*1.5, "mass": 5000,
                              "color": (255, 255, 0)}

    def setup(self):
        # Create four walls around the edges and add them to the obstacles
        top_wall = Wall((0, 0), (self.window_size.x, 0))
        right_wall = Wall((self.window_size.x, 0), (self.window_size.x, self.window_size.y))
        bottom_wall = Wall((self.window_size.x, self.window_size.x), (0, self.window_size.y))
        left_wall = Wall((0, self.window_size.y), (0, 0))
        self.add_obstacles(top_wall, right_wall, bottom_wall, left_wall)

        # Create random positions and velocities
        x_vals = np.random.uniform(0, self.window_size.x, self.nboids)
        y_vals = np.random.uniform(0, self.window_size.y, self.nboids)
        positions = np.column_stack((x_vals, y_vals))
        velocities = np.random.uniform(-1, 1, (self.nboids, 2))

        # Populate the simulation with new boids
        self.add_n_boids(self.nboids, positions, velocities)

    def add_obstacles(self, *args):
        for obstacle in args:
            self.obstacles.append(obstacle)

    def delete_obstacles(self, *args):
        for obstacle in args:
            self.obstacles.remove(obstacle)
            del obstacle

    def clear_obstacles(self):
        del self.obstacles[4:]

    def add_n_boids(self, n, positions, velocities):
        for i in range(n):
            new = Boid(simulation=self,
                       position=positions[i],
                       velocity=velocities[i],
                       max_speed=self.boid_settings["max_speed"],
                       view_distance=self.boid_settings["view_distance"],
                       view_angle=self.boid_settings["view_angle"],
                       mass=self.boid_settings["mass"],
                       color=self.boid_settings["color"])

            self.flock.append(new)
            self.actors.append(new)

    def add_predator(self, position, velocity, max_speed=0.1, view_distance=200, view_angle=np.pi, mass=5000, color=(255, 0, 0)):
        new = Predator(simulation=self,
                       position=position,
                       velocity=velocity,
                       max_speed=max_speed,
                       view_distance=view_distance,
                       view_angle=view_angle,
                       mass=mass,
                       color=color)

        self.actors.append(new)
        self.predators.append(new)

    def step(self, dt):
        for actor in self.actors:
            actor.update(dt)

    def reset(self):
        self.actors = []
        self.flock = []
        self.predators = []
        self.obstacles = []
        self.setup()

