import random
from vectors2d import Vector
from obstacles import Circle, Wall
import math

avoidance_strength = 100.0
separation_strength = 4.0
separation_radius = 20.0
sep_rad_sq = separation_radius ** 2
alignment_strength = 1.0
cohesion_strength = 1.0
evasion_strength = 100.0
pursuit_strength = evasion_strength


class Actor:
    """The base class for all actors. Actors can move and be seen by other actors."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color):
        self.sim = simulation

        self.pos = Vector(position[0], position[1])  # position
        self.direction = Vector(velocity[0], velocity[1]).normalize()
        self.dir_history = [self.direction] * 10
        self.v = self.direction * max_speed  # velocity
        self.speed = max_speed
        self.forces = Vector(0, 0)  # sum of all forces on the actor this frame
        self.max_speed = float(max_speed)  # the maximum speed the actor can travel at

        self.view_dist = float(view_distance)  # how far the actor can see
        self.view_dist_sq = self.view_dist ** 2
        self.view_angle = float(view_angle)  # in radians
        self.ahead = self.v  # look ahead vector to avoid collision

        self.mass = mass  # influences
        self.color = color  # color for display

    def update(self, dt):
        """Updates all the actor attributes. Call this every frame after calculating all the forces."""

        self.forces += self.calc_avoidance()
        acceleration = self.forces / self.mass

        self.v += acceleration * dt  # update the velocity

        self.speed = self.v.length()

        # Clamp the velocity at maximum speed
        if self.speed > self.max_speed:
            self.v = self.v.normalize() * self.max_speed
            self.speed = self.max_speed

        self.direction = self.v.normalize()

        del self.dir_history[0]
        self.dir_history.append(self.direction)

        self.forces = Vector(0, 0)  # reset all the forces after applying them

        if not 0 <= self.pos.x <= self.sim.window_size.x or not 0 <= self.pos.y <= self.sim.window_size.y:
            self.v = (self.sim.center - self.pos).normalize() * self.max_speed

        self.pos += self.v * dt  # update the position
        self.ahead = 50 * self.v * dt  # update the ahead vector

    def calc_avoidance(self):
        small_ahead = self.ahead / 2
        threat = None
        threat_dist_sq = None

        for obstacle in self.sim.obstacles:
            if type(obstacle) is Wall:
                dist_sq = max(0.0000001, obstacle.distance_sq_to(self.pos))
                if threat_dist_sq is None or dist_sq < threat_dist_sq:
                    if obstacle.intersects(self.pos, self.ahead):
                        threat = obstacle
                        threat_dist_sq = dist_sq
            elif type(obstacle) is Circle:
                dist_sq = max(0.0000001, self.pos.distance_sq_to(obstacle.pos) - obstacle.rad_sq)
                if threat_dist_sq is None or dist_sq < threat_dist_sq:
                    close_dist_sq = (self.pos + small_ahead).distance_sq_to(obstacle.pos)
                    far_dist_sq = (self.pos + self.ahead).distance_sq_to(obstacle.pos)
                    if close_dist_sq <= obstacle.rad_sq or far_dist_sq <= obstacle.rad_sq or dist_sq <= obstacle.rad_sq:
                        threat = obstacle
                        threat_dist_sq = dist_sq

        if type(threat) is Wall:
            threat_dist = math.sqrt(threat_dist_sq)
            avoidance = (threat.orthonormal_vector_to(self.pos)) * avoidance_strength / threat_dist
            return avoidance
        elif type(threat) is Circle:
            threat_dist = math.sqrt(threat_dist_sq)
            avoidance = (self.pos - threat.pos).normalize() * avoidance_strength / threat_dist
            return avoidance
        else:
            return Vector(0, 0)

    def in_fov(self, point):
        """Checks if a given point is in the field of view"""
        facing_direction = self.v.normalize()
        to_point = self.pos.direction_to(point)
        return to_point.angle_to(facing_direction) <= self.view_angle / 2


class Boid(Actor):
    """Boid class."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color):
        Actor.__init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color)
        self.neighbors = []  # all boids that are close
        self.flocking = Vector(0, 0)
        self.update_this_frame = bool(random.getrandbits(1))

    def update(self, dt):
        # only update neighbors and flocking force every second frame
        if self.update_this_frame:
            self.get_neighbors()
            self.calc_flocking()

        self.forces += self.flocking
        self.forces += self.calc_evasion()
        Actor.update(self, dt)
        self.change_color()

        self.update_this_frame = not self.update_this_frame

    def change_color(self):
        red_val = (1 - self.speed / self.max_speed) * 255
        self.color = (red_val, 255, 0)

    def get_neighbors(self):
        """Gets all the neighbors that are visible to the boid."""
        self.neighbors = []
        for member in self.sim.flock:
            if member is self:
                continue
            elif self.pos.distance_sq_to(member.pos) <= self.view_dist_sq and self.in_fov(member.pos):
                self.neighbors.append(member)

    def get_threat(self):
        closest_threat = None
        closest_dist_sq = None

        for threat in self.sim.predators:
            dist_sq = self.pos.distance_sq_to(threat.pos)
            if dist_sq <= self.view_dist_sq and self.in_fov(threat.pos):
                if closest_threat is None or dist_sq < closest_dist_sq:
                    closest_threat = threat
                    closest_dist_sq = dist_sq

        return closest_threat, closest_dist_sq

    def calc_flocking(self):
        """Calculates all the flocking forces."""
        separation = self.calc_separation()
        alignment = self.calc_alignment()
        cohesion = self.calc_cohesion()

        self.flocking = separation + alignment + cohesion

    def calc_separation(self):
        """Calculate the separation force of the boids which makes them keep a minimum distance from each other."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_evasion = Vector(0, 0)
        close_neighbors = 0  # the number of neighbors that are within a given separation radius

        for neighbor in self.neighbors:
            dist_sq = self.pos.distance_sq_to(neighbor.pos)  # distance to the neighbor
            if dist_sq <= sep_rad_sq:
                close_neighbors += 1
                # divide by distance such that the separation force is stronger for closer neighbors.
                avg_evasion += (self.pos - neighbor.pos) / math.sqrt(dist_sq)  # vector pointing away from the neighbor

        if close_neighbors == 0:
            return Vector(0, 0)
        else:
            avg_evasion /= close_neighbors

        separation = avg_evasion.normalize() * separation_strength
        return separation

    def calc_alignment(self):
        """Calculate the alignment force of the boids which makes them align their velocity vectors."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_direction = self.v.normalize()

        for neighbor in self.neighbors:
            avg_direction += neighbor.v.normalize()

        avg_direction /= len(self.neighbors) + 1  # the average direction every neighbor is facing (including self)

        alignment = avg_direction.normalize() * alignment_strength
        return alignment

    def calc_cohesion(self):
        """Calculate the cohesion force of the boids which makes them stay together."""
        if not self.neighbors:
            return Vector(0, 0)

        avg_position = self.pos

        for neighbor in self.neighbors:
            avg_position += neighbor.pos

        avg_position /= len(self.neighbors) + 1  # the average position every neighbor has (including self)

        cohesion = (avg_position - self.pos).normalize() * cohesion_strength
        return cohesion

    def calc_evasion(self):
        """Calculate the evasion force which makes them evade any predators"""
        threat, dist_sq = self.get_threat()

        if threat is None:
            return Vector(0, 0)

        distance = math.sqrt(dist_sq)

        # if distance <= 5.0:
        #     self.sim.actors.remove(self)
        #     self.sim.flock.remove(self)

        direction = threat.v.side(threat.pos, self.pos) * threat.v.orthonormal()
        evasion = direction * evasion_strength / distance

        return evasion


class Predator(Actor):
    """Basic predator class."""

    def __init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color):
        Actor.__init__(self, simulation, position, velocity, max_speed, view_distance, view_angle, mass, color)

        self.update_this_frame = bool(random.getrandbits(1))

    def update(self, dt):
        if self.update_this_frame:
            self.forces += self.calc_pursuit(dt)
        Actor.update(self, dt)
        self.update_this_frame = not self.update_this_frame

    def calc_pursuit(self, dt):
        """Calculate the pursuit force which makes them pursuit the closest boid"""
        target, dist_sq = self.find_target()
        if target is None:
            pursuit = Vector(0, 0)
        else:
            dist = math.sqrt(dist_sq)
            direction = self.pos.direction_to(target.pos + target.v * 50 * dt)
            pursuit = pursuit_strength * direction / dist

        return pursuit

    def find_target(self):
        closest_target = None
        closest_dist_sq = None

        for target in self.sim.flock:
            dist_sq = self.pos.distance_sq_to(target.pos)
            if dist_sq <= self.view_dist_sq and self.in_fov(target.pos):
                if closest_target is None or dist_sq < closest_dist_sq:
                    closest_target = target
                    closest_dist_sq = dist_sq

        return closest_target, closest_dist_sq
