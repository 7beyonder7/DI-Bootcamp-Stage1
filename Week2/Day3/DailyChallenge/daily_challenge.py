import math
import turtle
import time


class Circle:
    def __init__(self, radius=None, diameter=None):
        if radius is not None:
            self._radius = radius
        elif diameter is not None:
            self._radius = diameter / 2
        else:
            raise ValueError("You must provide either a radius or a diameter.")

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive.")
        self._radius = value

    @property
    def diameter(self):
        return self._radius * 2

    @diameter.setter
    def diameter(self, value):
        if value <= 0:
            raise ValueError("Diameter must be positive.")
        self._radius = value / 2

    @property
    def area(self):
        return math.pi * (self._radius ** 2)

    def __repr__(self):
        return f"Circle(radius={self.radius:.2f}, diameter={self.diameter:.2f}, area={self.area:.2f})"

    def __gt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.radius > other.radius

    def __eq__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return math.isclose(self.radius, other.radius)

    def __lt__(self, other):
        return self.radius < other.radius


c1 = Circle(radius=50)
print(c1)

c2 = Circle(diameter=200)
print(c2.radius)

c2.diameter = 50
print(c2.area)

c1.radius = 7
print(c1)

print(c1 > c2)   # True
print(c2 > c1)   # False

c3 = Circle(radius=100)
c4 = Circle(radius=100)
print(c3 == c4)  # True

circles = [c1, c2, c3, c4]
sorted_circles = sorted(circles)
print(sorted_circles)


def draw_circles(circles):
    turtle.speed(1)
    turtle.hideturtle()
    turtle.bgcolor("white")

    sorted_circles = sorted(circles)
    colors = ["red", "green", "blue"]

    for i, c in enumerate(sorted_circles):
        turtle.penup()
        turtle.goto(0, -c.radius)
        turtle.pendown()
        turtle.color(colors[i % len(colors)])
        turtle.circle(c.radius)

    time.sleep(3)
    turtle.bye()


draw_circles([c1, c2, c3])
