from main import *


def circle(debug: bool = False):
    root = RootWheel(Direction.CLOCKWISE, speed=1)
    pen_point = Point(root, radius=200)
    pen = Pen(pen_point, 1, pygame.Color(0, 0, 0))
    spiro = Spirograph([pen])

    spiro.draw()


def ellipse(debug: bool = False):
    root = RootWheel(Direction.CLOCKWISE, speed=1)
    inner_wheel_anchor = Point(root, radius=200)
    inner_wheel = Wheel(inner_wheel_anchor, Direction.COUNTERCLOCKWISE, speed=1)
    pen_point = Point(inner_wheel, radius=50)
    pen = Pen(pen_point, 1, pygame.Color(0, 0, 0))
    spiro = Spirograph([pen])

    spiro.draw()


def four_pointed_rounded_star(debug: bool = False):
    root = RootWheel(Direction.CLOCKWISE, speed=1)
    inner_wheel_anchor = Point(root, radius=200)
    inner_wheel = Wheel(inner_wheel_anchor, Direction.COUNTERCLOCKWISE, speed=3)
    pen_point = Point(inner_wheel, radius=50)
    pen = Pen(pen_point, 1, pygame.Color(0, 0, 0))
    spiro = Spirograph([pen])

    spiro.draw()


def triple_fprs(debug: bool = False):
    root = RootWheel(Direction.CLOCKWISE, speed=1)
    inner_wheel_anchor = Point(root, radius=200)
    inner_wheel = Wheel(inner_wheel_anchor, Direction.COUNTERCLOCKWISE, speed=3)
    pens = []
    for colour, offset in zip(
            [pygame.Color(255, 0, 0), pygame.Color(0, 255, 0), pygame.Color(0, 0, 255)],
            [0,                       1/Decimal(3),            2/Decimal(3)]
    ):
        pen_point = Point(inner_wheel, radius=50, offset=offset)
        pen = Pen(pen_point, 3, colour)
        pens.append(pen)

    Spirograph(pens).draw()


def spirograph(debug: bool = False):
    root = RootWheel(Direction.CLOCKWISE, speed=1)
    inner_wheel_anchor = Point(root, radius=200)
    inner_wheel = Wheel(inner_wheel_anchor, Direction.COUNTERCLOCKWISE, speed=200)
    pen_point = Point(inner_wheel, radius=50)
    pens = [Pen(pen_point, 1, pygame.Color(0, 0, 0, 127))]

    Spirograph(pens).draw(temporal_resolution=10000)


def five_circles(debug: bool = False):
    wheel = root = RootWheel(Direction.CLOCKWISE, speed=1)
    pens = []
    for speed in range(2, 5 + 1):
        anchor = Point(wheel, radius=50)
        pens.append(Pen(anchor, 1, pygame.Color(speed * 50, 0, 0)))
        wheel = Wheel(anchor, Direction.CLOCKWISE if speed % 2 == 1 else Direction.COUNTERCLOCKWISE, speed=speed)
    pen_point = Point(wheel, radius=50)
    pens.append(Pen(pen_point, 5, pygame.Color(0, 0, 0)))

    Spirograph(pens).draw()


if __name__ == "__main__":
    circle()
    # ellipse()
    # triple_fprs()
    # spirograph()
    five_circles()
