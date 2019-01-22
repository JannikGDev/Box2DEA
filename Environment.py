import pygame
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

from pypybox2d.common import *
from pypybox2d.world import World
from pypybox2d.shapes import Polygon
import math

# --- constants ---
# Box2D deals with meters, but we want to display pixels,
# so define a conversion factor:
PPM = 5.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

WORLD_HEIGHT = SCREEN_HEIGHT/PPM
WORLD_WIDTH = SCREEN_WIDTH/PPM

White = (255, 255, 255, 255)
Grey = (127, 127, 127, 255)

class Environment:

    def __init__(self, solution, render=False):

        self.time = 0
        self.render = render

        # --- pygame setup ---
        if self.render:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
            pygame.display.set_caption('Simple pygame example')
            self.clock = pygame.time.Clock()

        self.world = World(gravity=(0, -10), do_sleep=True)
        self.running = True


        ground_body_a = self.world.create_static_body(
            position=(0, 0),
            shapes=Polygon(box=(30, 20)),
        )

        ground_body_c = self.world.create_static_body(
            position=(0, 0),
            shapes=Polygon(box=(5, 100)),
        )

        ground_body_d = self.world.create_static_body(
            position=(128, 0),
            shapes=Polygon(box=(5, 100)),
        )

        ground_body_b = self.world.create_static_body(
            position=(120, 0),
            shapes=Polygon(box=(30, 20)),
        )

        self.walker = self.world.create_dynamic_body(position=(10, 23), angle=15)

        boxA = self.walker.create_polygon_fixture(box=(2, 1), density=1, friction=0.3)

        boxB = self.walker.create_polygon_fixture(box=(1, 2), density=1, friction=0.3)

        for i in range(len(solution)//4):

            posX = WORLD_WIDTH*(solution[i+0] + solution[i+2])*0.5
            posY = WORLD_HEIGHT*(solution[i + 1] + solution[i + 3]) * 0.5

            dX = WORLD_WIDTH*(solution[i+0] - solution[i+2])
            dY = WORLD_WIDTH*(solution[i + 1] - solution[i + 3])

            length = math.sqrt(dX*dX+dY*dY)
            if length <= 0:
                length = 1


            if length > 0:
                degree = math.atan(dY/length)
            else:
                degree = 0

            plank = self.world.create_static_body(
                position=(posX, posY),
                shapes=Polygon(box=(length, 1)),
                angle=degree
            )


    def step(self):

        # Make Box2D simulate the physics of our world for one step.
        # Instruct the world to perform a single step of simulation. It is
        # generally best to keep the time step and iterations fixed.
        # See the manual (Section "Simulating the World") for further discussion
        # on these parameters and their implications.
        self.world.step(TIME_STEP, 10, 10)
        self.time += TIME_STEP

        if abs(self.walker.angular_velocity) < 3:
            self.walker.apply_angular_impulse(-5)

        if self.walker.position.y < 0:
            self.running = False

        if self.walker.position.x > WORLD_WIDTH*0.7:
            self.running = False

        if self.time > 40:
            self.running = False

        if self.render:
            self.screen.fill((0, 0, 0, 0))

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    # The user closed the window or pressed escape
                    self.running = False

            for body in self.world.bodies:
                for fixture in body.fixtures:
                    # The fixture holds information like density and friction,
                    # and also the shape.
                    shape = fixture.shape

                    # Naively assume that this is a polygon shape. (not good normally!)
                    # We take the body's transform and multiply it with each
                    # vertex, and then convert from meters to pixels with the scale
                    # factor.
                    vertices = [(body.transform * v) * PPM for v in shape.vertices]

                    # But wait! It's upside-down! Pygame and Box2D orient their
                    # axes in different ways. Box2D is just like how you learned
                    # in high school, with positive x and y directions going
                    # right and up. Pygame, on the other hand, increases in the
                    # right and downward directions. This means we must flip
                    # the y components.
                    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]

                    pygame.draw.polygon(self.screen, White, vertices)

            # Flip the screen and try to keep at the target FPS
            pygame.display.flip()

    def exit(self):

        if self.render:
            pygame.quit()

        print("Took Time:" + str(self.time))

        return self.walker.position.x #- abs(23 - self.walker.position.y)

