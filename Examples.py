from main import *


def circle(debug: bool = False):
    root = RootWheel(Direction.CLOCKWISE, speed=1)
    pen_point = Point(root, radius=200)
    pen = Pen(pen_point, 1, pygame.Color(0, 0, 0))
    spiro = Spirograph([pen])

    spiro.display(debug=debug)


def ellipse(debug: bool = False):
    root = RootWheel(Direction.CLOCKWISE, speed=1)
    inner_wheel_anchor = Point(root, radius=200)
    inner_wheel = Wheel(inner_wheel_anchor, Direction.COUNTERCLOCKWISE, speed=1)
    pen_point = Point(inner_wheel, radius=50)
    pen = Pen(pen_point, 1, pygame.Color(0, 0, 0))
    spiro = Spirograph([pen])

    spiro.display(debug=debug)


def four_pointed_rounded_star(debug: bool = False):
    root = RootWheel(Direction.CLOCKWISE, speed=1)
    inner_wheel_anchor = Point(root, radius=200)
    inner_wheel = Wheel(inner_wheel_anchor, Direction.COUNTERCLOCKWISE, speed=3)
    pen_point = Point(inner_wheel, radius=50)
    pen = Pen(pen_point, 1, pygame.Color(0, 0, 0))
    spiro = Spirograph([pen])

    spiro.display(debug=debug)

if __name__ == "__main__":
    circle()
    ellipse()
    four_pointed_rounded_star()
