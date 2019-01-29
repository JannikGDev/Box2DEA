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
TARGET_FPS = 10
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 240

WORLD_HEIGHT = SCREEN_HEIGHT/PPM
WORLD_WIDTH = SCREEN_WIDTH/PPM

CHECK_DELAY = 3
MIN_DISTANCE = 2

White = (255, 255, 255, 255)
Grey = (127, 127, 127, 255)
Red = (255, 127, 127, 255)
Orange = (255, 180, 180, 255)
Green = (127, 255, 127, 255)

TARGET = (128, 23)
ANCHOR = (18, 8)


class Environment:

    def __init__(self, solution, render=False):

        self.time = 0
        self.last_check = 0
        self.render = render
        self.bridge_anchor = ANCHOR
        self.next_anchor = self.bridge_anchor



        # --- pygame setup ---
        if self.render:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
            pygame.display.set_caption('Simple pygame example')
            self.clock = pygame.time.Clock()

        self.world = World(gravity=(0, -10), do_sleep=True)
        self.running = True

        self.world.create_static_body(
            position=(0, 0),
            shapes=Polygon(box=(20, 10)),
        )

        self.world.create_static_body(
            position=(128, 0),
            shapes=Polygon(box=(20, 20)),
        )

        self.walker = self.world.create_dynamic_body(position=(10, 23), angle=15)
        self.walker.create_polygon_fixture(box=(2, 1), density=1, friction=0.3)
        self.walker.create_polygon_fixture(box=(1, 2), density=1, friction=0.3)

        self.last_walker_pos = self.walker.position

        dx = TARGET[0] - self.walker.position.x
        dy = TARGET[1] - self.walker.position.y

        self.targetDis = dx*dx+dy*dy

        for i in range(len(solution)//2):

            degree = solution[i*2+0] * (2*math.pi)
            length = solution[i*2+1] * 10 + 2

            pos_x = self.next_anchor[0] + length*math.cos(degree)
            pos_y = self.next_anchor[1] + length*math.sin(degree)

            # Calculate next Bridge Joint Position
            self.next_anchor = (self.next_anchor[0] + length*math.cos(degree)*2,
                                self.next_anchor[1] + length*math.sin(degree)*2)

            plank = self.world.create_static_body(
                position=(pos_x, pos_y),
                shapes=Polygon(box=(length, 1)),
                angle=degree
            )

            if self.render:
                plank.user_data = True

    def step(self):

        # Make Box2D simulate the physics of our world for one step.
        # Instruct the world to perform a single step of simulation. It is
        # generally best to keep the time step and iterations fixed.
        # See the manual (Section "Simulating the World") for further discussion
        # on these parameters and their implications.
        self.world.step(TIME_STEP, 10, 10)
        self.time += TIME_STEP

        dx = TARGET[0] - self.walker.position.x
        dy = TARGET[1] - self.walker.position.y
        dis = dx * dx + dy * dy

        if dis < self.targetDis:
            self.targetDis = dis


        if self.time - self.last_check > CHECK_DELAY:
            dx = self.walker.position.x - self.last_walker_pos.x
            dy = self.walker.position.y - self.last_walker_pos.y

            self.last_check = self.time
            self.last_walker_pos = self.walker.position

            # print("Distance: " + str(math.sqrt(dx*dx + dy*dy)))

            minDis = MIN_DISTANCE*MIN_DISTANCE

            if dx*dx + dy*dy < minDis:
                self.running = False

        if abs(self.walker.angular_velocity) < 3:
            self.walker.apply_angular_impulse(-100*TIME_STEP)

        if self.walker.position.y < 0:
            self.running = False

        if self.walker.position.x > WORLD_WIDTH*0.9:
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

                    if body.dynamic:
                        pygame.draw.polygon(self.screen, Green, vertices)
                    elif body.user_data:
                        pygame.draw.polygon(self.screen, Red, vertices)
                    else:
                        pygame.draw.polygon(self.screen, White, vertices)

            # Flip the screen and try to keep at the target FPS
            pygame.display.flip()


    def save_image(self, filename):

        return pygame.image.save(self.screen, filename)

    def exit(self):

        if self.render:
            pygame.quit()

        fitness = self.targetDis

        print("Took Time:" + str(self.time))
        print("Fitness: " + str(fitness))

        return fitness

