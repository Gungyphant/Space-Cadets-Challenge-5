import math
from abc import ABC
from enum import Enum

class Direction(Enum):  # The position algorithms use increasing t -> clockwise movement, so this allows the value to be useful
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


class Object(ABC):
    """Abstract base class for any object which has a position"""
    def get_pos(self, time: float) -> tuple[float, float]:
        """Get the position of the Object at a time

        :param time: The time since the spirograph began
        """


class BaseWheel(Object, ABC):
    """The abstract base class for wheels"""
    center: tuple[int, int] | Point
    direction: Direction
    speed: float


class RootWheel(BaseWheel):
    """The wheel which is centered on the origin"""
    center: tuple[int, int]
    def __init__(self, direction: Direction, speed: float):
        """:param direction: The direction the wheel rotates
        :param speed: The speed with which the wheel rotates, in arbitrary units
        """
        self.center = (0, 0)
        self.direction = direction
        self.speed = speed

    def get_pos(self, time: float) -> tuple[float, float]:
        # RootWheels cannot move
        return self.center


class Wheel(BaseWheel):
    """A wheel which is centered on a Point on another wheel"""
    center: Point
    def __init__(self, center: Point, direction: Direction, speed: float):
        """:param center: The Point which acts as the center of this wheel
        :param direction: The direction the wheel rotates
        :param speed: The speed with which the wheel rotates, in arbitrary units
        """
        self.center = center
        self.direction = direction
        self.speed = speed

    def get_pos(self, time: float) -> tuple[float, float]:
        # Wheels are always on their point
        return self.center.get_pos(time)


class Point(Object):
    """A point on a Wheek"""
    wheel: Wheel
    radius: float
    offset: float
    def __init__(self, wheel: Wheel, radius: float, offset: float):
        """:param wheel: The Wheel which the point is anchored to
        :param radius: The distance between the center of the Wheel and the Point
        :param offset: The Point's starting offset from directly up, in radians
        """
        self.wheel = wheel
        self.radius = radius
        self.offset = offset

    def get_pos(self, time: float) -> tuple[float, float]:
        # Points rotate around the center of their wheel
        angle = self.wheel.speed * self.wheel.direction.value * time + self.offset
        wheel_x, wheel_y = self.wheel.get_pos(time)
        x, y = wheel_x + self.radius * math.sin(angle), wheel_y + self.radius * math.cos(angle)
        return x, y


class Pen(Object):
    """A pen which draws as it moves"""
    point: Point
    radius: float
    colour: str  # hex code
    def __init__(self, point: Point, radius: float, colour: str):
        """:param point: The Point which the Pen is anchored to
        :param radius: The radius of the pen
        :param colour: The colour the pen draws, as a hex code
        """
        self.point = point
        self.radius = radius
        self.colour = colour

    def get_pos(self, time: float) -> tuple[float, float]:
        # Pens are locked on their point
        return self.point.get_pos(time)
