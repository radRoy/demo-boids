import sys
import numpy as np
import pygame as pg
from pygame_widgets import update as update_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import actors
from simulation import Simulation
from actors import Actor, Boid, Predator
from obstacles import Obstacle, Circle, Wall
from vectors2d import Vector

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND = (42, 57, 144)


def setup_sliders(display):
    fontsize = 28

    # Slider settings
    s_left = 15  # distance to left window border (x-dir.) in px
    s_top = 15  # distance to top window border (x-dir.) in px
    s_width = 150  # width (x-dir.) in px
    s_height = 10  # height (y-dir.) in px
    s_dist = 50  # distance between sliders (y-dir.) in px

    # TextBox settings
    t_dist = 20  # dist. to corr. slider (above in animation)
    t_left = s_left + s_width + 5  # dist. to left border
    t_top = s_top + t_dist
    t_width, t_height = 30, 20

    # Sliders and TextBoxes by Simulation parameter
    sep_slider = Slider(display, s_left, s_top, s_width, s_height, min=0.0, max=10.0, step=.1)
    sep_slider.setValue(4.0)
    sep_out = TextBox(display, t_left, t_top, 0, t_height, fontSize=fontsize, borderThickness=1)
    sep_label = TextBox(display, s_left, s_top + t_dist, 0, t_height, fontSize=fontsize, borderThickness=1)\
        .setText("Separation")

    align_slider = Slider(display, s_left, s_top + s_dist, s_width, s_height, min=0.0, max=10.0, step=.1)
    align_slider.setValue(1.0)
    align_out = TextBox(display, t_left, t_top + s_dist, 0, t_height, fontSize=fontsize, borderThickness=1)
    align_label = TextBox(display, s_left, s_top + s_dist + t_dist, 0, t_height, fontSize=fontsize, borderThickness=1)\
        .setText("Alignment")

    coh_slider = Slider(display, s_left, s_top + s_dist * 2, s_width, s_height, min=0.0, max=10.0, step=.1)
    coh_slider.setValue(1.0)
    coh_out = TextBox(display, t_left, t_top + s_dist * 2, 0, t_height, fontSize=fontsize, borderThickness=1)
    coh_label = TextBox(display, s_left, t_top + s_dist * 2, 0, t_height, fontSize=fontsize, borderThickness=1)\
        .setText("Cohesion")

    "spare sliders, pre-arranged to appear below existing ones"
    # sep_rad_slider = Slider(display, s_left, s_top + s_dist * 4, s_width, s_height, min=0.0, max=80.0, step=.1)
    # sep_rad_slider.setValue(20.0)
    # sep_rad_out = TextBox(display, t_left, t_top + s_dist * 4, 0, t_height, fontSize=fontsize, borderThickness=1)
    # sep_rad_label = TextBox(display, s_left, t_top + s_dist * 4, 0, t_height, fontSize=fontsize, borderThickness=1).setText("Separation rad")
    # avoid_slider = Slider(display, s_left, s_top + s_dist * 5, s_width, s_height, min=0.0, max=400.0, step=1)
    # avoid_slider.setValue(100.0)
    # avoid_out = TextBox(display, t_left, t_top + s_dist * 5, 0, t_height, fontSize=fontsize, borderThickness=1)
    # avoid_label = TextBox(display, s_left, t_top + s_dist * 5, 0, t_height, fontSize=fontsize, borderThickness=1).setText("Avoidance")

    # slider_6 = Slider(display, s_left, s_top + s_dist * 6, s_width, s_height, min=0.0, max=10.0, step=.1)
    # slider_6_out = TextBox(display, t_left, t_top + s_dist * 6, 0, t_height, fontSize=fontsize, borderThickness=1)
    # slider_6_label = TextBox(display, s_left, t_top + s_dist * 6, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 6")
    # slider_7 = Slider(display, s_left, s_top + s_dist * 7, s_width, s_height, min=0.0, max=10.0, step=.1)
    # slider_7_out = TextBox(display, t_left, t_top + s_dist * 7, 0, t_height, fontSize=fontsize, borderThickness=1)
    # slider_7_label = TextBox(display, s_left, t_top + s_dist * 7, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 7")
    # slider_8 = Slider(display, s_left, s_top + s_dist * 8, s_width, s_height, min=0.0, max=10.0, step=.1)
    # slider_8_out = TextBox(display, t_left, t_top + s_dist * 8, 0, t_height, fontSize=fontsize, borderThickness=1)
    # slider_8_label = TextBox(display, s_left, t_top + s_dist * 8, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 8")
    # slider_9 = Slider(display, s_left, s_top + s_dist * 9, s_width, s_height, min=0.0, max=10.0, step=.1)
    # slider_9_out = TextBox(display, t_left, t_top + s_dist * 9, 0, t_height, fontSize=fontsize, borderThickness=1)
    # slider_9_label = TextBox(display, s_left, t_top + s_dist * 9, 0, t_height, fontSize=fontsize, borderThickness=1).setText("slider 9")

    return {"sep_slider": sep_slider, "coh_slider": coh_slider, "align_slider": align_slider,
            "sep_out": sep_out, "coh_out": coh_out, "align_out": align_out}  # slider_settings created/updated


def slider_update(slider_settings):
    """reads slider values, updates sim. parameters (actors) and number displayed in next frame"""

    # feeding slider values into simulation parameters
    actors.separation_strength = slider_settings["sep_slider"].getValue()
    actors.cohesion_strength = slider_settings["coh_slider"].getValue()
    actors.alignment_strength = slider_settings["align_slider"].getValue()
    # actors.separation_radius = slider_settings["sep_rad_slider"].getValue()
    # actors.avoidance_strength = slider_settings["avoid_slider"].getValue()

    # each following drawing command draws on top of previous ones
    slider_settings["sep_out"].setText(np.round(actors.separation_strength, 3))
    slider_settings["coh_out"].setText(np.round(actors.cohesion_strength, 3))
    slider_settings["align_out"].setText(np.round(actors.alignment_strength, 3))
    # slider_settings["sep_rad_out"].setText(actors.separation_radius)
    # slider_settings["avoid_out"].setText(actors.avoidance_strength)


def setup_buttons(sim):
    font = pg.font.Font("freesansbold.ttf", 24)
    reset_text = font.render("reset", True, (0, 0, 0), (200, 200, 200))
    reset_rect = reset_text.get_rect()
    reset_rect.center = (sim.window_size.x - 96, 24)
    clear_text = font.render("clear", True, (0, 0, 0), (200, 200, 200))
    clear_rect = clear_text.get_rect()
    clear_rect.center = (sim.window_size.x - 96, 52)
    predator_text = font.render("predator", True, (0, 0, 0), (200, 200, 200))
    predator_rect = clear_text.get_rect()
    predator_rect.center = (sim.window_size.x - 96, 80)

    return {"clear_text": clear_text, "clear_rect": clear_rect, "reset_text": reset_text, "reset_rect": reset_rect,
            "predator_text": predator_text, "predator_rect": predator_rect}  # buttons created/updated


def draw_buttons(display, buttons):
    """draws (blits) the buttons to the display"""
    display.blit(buttons["clear_text"], buttons["clear_rect"])
    display.blit(buttons["reset_text"], buttons["reset_rect"])
    display.blit(buttons["predator_text"], buttons["predator_rect"])


def draw_actors(sim, display):
    """Iterates over all the actors in the simulation and draws them on screen."""
    for actor in sim.actors:
        # get the average direction of the last few frames of the actor
        direction = Vector(0, 0)
        for d in actor.dir_history:
            direction += d
        direction /= len(actor.dir_history)

        if type(actor) is Predator:
            left = actor.pos - direction * 15 + direction.orthonormal() * 5
            right = actor.pos - direction * 15 - direction.orthonormal() * 5
        else:
            left = actor.pos - direction * 10 + direction.orthonormal() * 2
            right = actor.pos - direction * 10 - direction.orthonormal() * 2

        pg.draw.polygon(display, actor.color, points=[actor.pos, left, right])


def draw_obstacles(sim, display):
    """Iterates over all the obstacles in the simulation and draws them on screen."""
    for obstacle in sim.obstacles:
        if type(obstacle) is Wall:
            pg.draw.line(display, BLUE, obstacle.start, obstacle.stop, 10)
        elif type(obstacle) is Circle:
            pg.draw.circle(display, (0, 0, 255), obstacle.pos, obstacle.rad)


def main(sim, fps, window_size):
    """Main function"""
    pg.init()
    display = pg.display.set_mode(window_size)
    clock = pg.time.Clock()
    slider_settings = setup_sliders(display)
    buttons = setup_buttons(sim)

    wall_start = None

    # Main game loop
    while True:

        # Get all events
        events = pg.event.get()
        for event in events:
            # exit the (py) interpreter (end program) if the pygame windows is closed
            if event.type == pg.QUIT:
                sys.exit()  # prints 1 in case of error(s)

            # react to the pushing of the left mouse button
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if buttons["reset_rect"].collidepoint(mouse_pos):
                    sim.reset()
                elif buttons["clear_rect"].collidepoint(mouse_pos):
                    sim.clear_obstacles()
                elif buttons["predator_rect"].collidepoint(mouse_pos):
                    v = np.random.uniform(-1, 1, 2)
                    velocity = Vector(v[0], v[1]).normalize()
                    sim.add_predator(sim.center, velocity=velocity, view_angle=np.pi/2)

            # react to the releasing of the right mouse button
            elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                mouse_pos = pg.mouse.get_pos()
                sim.add_obstacles(Circle(mouse_pos, 20))

            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                mouse_pos = Vector(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                if wall_start is None:
                    wall_start = mouse_pos
                elif abs(wall_start - mouse_pos) >= 0.00001:
                    wall_stop = mouse_pos
                    wall = Wall(wall_start, wall_stop)
                    sim.add_obstacles(wall)
                    wall_start = None

        # preaparing the next empty frame
        display.fill(WHITE)
        dt = clock.tick(fps)
        slider_update(slider_settings)  # fetching parameters (live!)
        sim.step(dt)  # applying parameters instantly (live!) simulating movements in the next frame

        # drawing what is to be drawn
        draw_actors(sim, display)
        draw_obstacles(sim, display)  # TBD: FIX BOTTOM BOUNDARY (incl. weird avoidance behaviour)
            # boids react to the bottom display wall as if it was invisible, sort of like a window. poor fellows...
        draw_buttons(display, buttons)
        update_widgets(events)
        pg.display.update()
    # end of the Main game loop


if __name__ == "__main__":
    res = (1080, 720)
    Sim = Simulation(res, 200)
    Sim.setup()

    main(sim=Sim, fps=30, window_size=res)
