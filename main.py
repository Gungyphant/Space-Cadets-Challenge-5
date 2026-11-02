import os
from functools import cache
from time import time as current_time
from abc import ABC
from enum import Enum
from decimal import Decimal

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # Stop pygame printing to console on startup
import pygame

from utils import frange, lcm, PreciseNumber, Number, sin, cos, pi


PygameColour = pygame.Color | int | tuple[int, int, int] | tuple[int, int, int, int]

class Direction(Enum):  # The position algorithms use increasing t -> clockwise movement, so this allows the value to be useful
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


RESOLUTION = (500, 500)
FPS = 60


class Object(ABC):
    """Abstract base class for any object which has a position"""
    periodicity: int  # How often the object's state resets

    @cache
    def get_pos(self, time: PreciseNumber) -> tuple[PreciseNumber, PreciseNumber]:
        """Get the position of the Object at a time

        :param time: The time since the spirograph began
        """

    # # The following functions allow for a nicer way of connecting things; Wheel().point(a, b, c) is equivalent to Point(Wheel(), a, b, c)
    # def wheel(self, *args) -> Wheel:
    #     return Wheel(self, *args)
    #
    # def point(self, *args) -> Point:
    #     return Point(self, *args)
    #
    # def pen(self, *args) -> Pen:
    #     return Pen(self, *args)


class BaseWheel(Object, ABC):
    """The abstract base class for wheels"""
    center: tuple[int, int] | Point
    direction: Direction
    speed: int


class RootWheel(BaseWheel):
    """The wheel which is centered on the origin"""
    center: tuple[int, int]
    def __init__(self, direction: Direction, speed: int):
        """:param direction: The direction the wheel rotates
        :param speed: The speed with which the wheel rotates, in rps
        """
        self.center = (0, 0)
        self.direction = direction
        self.speed = speed
        self.periodicity = 0  # RootWheels cannot move (their rotation is not part of them)

    def get_pos(self, time: PreciseNumber) -> tuple[PreciseNumber, PreciseNumber]:
        # RootWheels cannot move
        return self.center


class Wheel(BaseWheel):
    """A wheel which is centered on a Point on another wheel"""
    center: Point
    def __init__(self, center: Point, direction: Direction, speed: int):
        """:param center: The Point which acts as the center of this wheel
        :param direction: The direction the wheel rotates
        :param speed: The speed with which the wheel rotates, in arbitrary units
        """
        self.center = center
        self.direction = direction
        self.speed = speed
        self.periodicity = center.periodicity  # Wheels are always on their point and don't change in any other way

    def get_pos(self, time: PreciseNumber) -> tuple[PreciseNumber, PreciseNumber]:
        # Wheels are always on their point
        return self.center.get_pos(time)


class Point(Object):
    """A point on a Wheek"""
    wheel: BaseWheel
    radius: PreciseNumber
    offset: PreciseNumber
    def __init__(self, wheel: BaseWheel, radius: PreciseNumber, offset: PreciseNumber = 0):
        """:param wheel: The Wheel which the point is anchored to
        :param radius: The distance between the center of the Wheel and the Point
        :param offset: The Point's starting offset from directly up, as a proportion of the Wheel
        """
        self.wheel = wheel
        self.radius = radius
        self.offset = offset
        self.periodicity = lcm(wheel.periodicity, wheel.speed)  # If it takes 3 'seconds' for the center to return to its base position, and the wheel's period of rotation is 2s, it'll take lcm(3, 2) = 6s to reset

    def get_pos(self, time: PreciseNumber) -> tuple[PreciseNumber, PreciseNumber]:
        # Points rotate around the center of their wheel
        angle = (self.wheel.speed * self.wheel.direction.value * time + self.offset) * 2 * pi  # *2pi converts rps to rad/s
        wheel_x, wheel_y = self.wheel.get_pos(time)
        x, y = wheel_x + self.radius * sin(angle), wheel_y + self.radius * cos(angle)
        return x, y


class Pen(Object):
    """A pen which draws as it moves"""
    point: Point
    width: int
    colour: PygameColour
    def __init__(self, point: Point, width: int, colour: PygameColour):
        """:param point: The Point which the Pen is anchored to
        :param width: The radius of the pen
        :param colour: The colour the pen draws, as a hex code
        """
        self.point = point
        self.width = width
        self.colour = colour
        self.periodicity = point.periodicity

    def get_pos(self, time: PreciseNumber) -> tuple[PreciseNumber, PreciseNumber]:
        # Pens are locked on their point
        return self.point.get_pos(time)


def convert_coordinates(coordinate: tuple[Number, Number]) -> tuple[float, float]:
    """Convert a coordinate from Spirograph coordinates to pygame coordinates

    :param coordinate: The Spirograph coordinate
    :returns: The equivalent pygame coordinate
    """
    # (0, 0) is the center in spiro coordinates; (0, 0) is the top left in pygame
    # Also, pygame requires floats
    x, y = coordinate
    width, height = map(Decimal, RESOLUTION)
    new_x, new_y = float(x + width/2), float(y + height/2)
    return new_x, new_y


def convert_coordinate_list(coordinate_list: list[tuple[Number, Number]]) -> list[tuple[float, float]]:
    """Convert a list of Spirograph coordinates to a list of pygame coordinates

    :param coordinate_list: The list of Spirograph coordinates
    :returns: The list of equivalent pygame coordinates
    """
    return list(map(convert_coordinates, coordinate_list))


class Spirograph:
    """A collection of Pens"""
    pens: list[Pen]
    def __init__(self, pens: list[Pen]):
        self.pens = pens

    def display(self, temporal_resolution: Number = 1000, debug: bool = False) -> None:
        """Create a window to show the Spirograph

        :param temporal_resolution: The frequency (in 'Hz') to calculate the position of the pens. Defaults to 1000Hz
        :param debug: If True, debug messages will be printed
        """
        pygame.init()
        screen = pygame.display.set_mode(RESOLUTION)
        clock = pygame.time.Clock()
        running = True

        screen.fill("white")

        # Render the spirograph:
        render_start_time = current_time()

        for pen in self.pens:
            time_range = frange(0, pen.periodicity, 1/Decimal(temporal_resolution))
            positions = [pen.get_pos(Decimal(t)) for t in time_range]
            # print(positions)
            pygame.draw.lines(screen, pen.colour, True, convert_coordinate_list(positions), width=pen.width)

        if debug:
            render_stop_time = current_time()
            print(f"Render took {(render_stop_time - render_start_time) * FPS:.1f} frames")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Window closed
                    running = False

            pygame.display.flip()

            clock.tick(FPS)

        pygame.quit()

    def draw(self, temporal_resolution: Number = 1000) -> None:
        """Create a window to draw the Spirograph in real time

        :param temporal_resolution: The frequency (in 'Hz') to calculate the position of the pens. Defaults to 1000Hz
        """
        pygame.init()
        screen = pygame.display.set_mode(RESOLUTION)
        clock = pygame.time.Clock()
        running = True

        screen.fill("white")

        time = 0
        delta_time = 1/Decimal(temporal_resolution)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Window closed
                    running = False

            # Render the spiro
            for pen in self.pens:
                # print(pen.colour, convert_coordinates(pen.get_pos(time)))
                pygame.draw.line(screen, pen.colour, convert_coordinates(pen.get_pos(time)), convert_coordinates(pen.get_pos(time + delta_time)), width=pen.width)
            time += delta_time

            pygame.display.flip()

            dt = clock.tick(FPS)

        pygame.quit()
