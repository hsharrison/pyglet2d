__version__ = '0.1.0'

from itertools import chain

import numpy as np
import pyglet
from Polygon import Polygon
from Polygon.Utils import pointList as point_list


class Shape:
    def __init__(self, vertices, color=(255, 255, 255), velocity=(0, 0), colors=None):
        """Graphical polygon primitive for use with `pyglet`_.

        Alternative constructor methods:

        - |Shape.circle|
        - |Shape.rectangle|
        - |Shape.regular_polygon|
        - |Shape.from_dict|

        Parameters
        ----------
        vertices : array-like or |Polygon|.
            If a |Polygon| is passed, its points will be used.
            Otherwise, `vertices` should be a sequence of `[x, y]` locations or an array with x and y columns.
        color : str or 3-tuple of int, optional
            Color, in R, G, B format.
            Alternatively, a key that refers to an element of `colors`.
        velocity : array-like
            Speed and direction of motion, in [dx_dt, dy_dt] format.
        colors : dict of tuple, optional
            Named colors, defined as R, G, B tuples.
            Useful for easily switching between a set of colors.

        Attributes
        ----------
        poly : |Polygon|
            Associated |Polygon| object.
        vertices : |array|
            An array of points, with x and y columns. Read-only.
        center : |array|
            The centroid of the shape.
            Setting center calls |Shape.translate|.
        position : |array|
            Alias for `center`.
        radius : |array|
            Mean distance from each point to the center.
            Setting radius calls |Shape.scale|.
        color : str or tuple of int
            The current color, in R, G, B format if `colors` was not passed.
            Otherwise, the current color is represented as a key in `colors`.
        colors : dict of tuple
            Named colors.
        velocity : |array|
            Speed and direction of motion.
        enabled : bool
            If False, the shape will not be drawn.


        """
        if isinstance(vertices, Polygon):
            self.poly = vertices
        else:
            self.poly = Polygon(vertices)

        self.colors = colors
        self._color = 'primary'
        if colors:
            self.color = color

        else:
            self.colors = {'primary': color}

        self.velocity = np.asarray(velocity)

        # Construct vertex_list.
        self._vertex_list = self._get_vertex_list()
        self.enabled = True

    @classmethod
    def regular_polygon(cls, center, radius, n_vertices, start_angle=0, **kwargs):
        """Construct a regular polygon.

        Parameters
        ----------
        center : array-like
        radius : float
        n_vertices : int
        start_angle : float, optional
            Where to put the first point, relative to `center`,
            in degrees counter-clockwise starting from the horizontal axis.
        **kwargs
            Other keyword arguments are passed to the |Shape| constructor.

        """
        angles = (np.arange(n_vertices) * 2 * np.pi / n_vertices) + (np.pi * start_angle / 180)
        return cls(center + radius * np.array([np.cos(angles), np.sin(angles)]).T, **kwargs)

    @classmethod
    def circle(cls, center, radius, n_vertices=50, **kwargs):
        """Construct a circle.

        Parameters
        ----------
        center : array-like
        radius : float
        n_vertices : int, optional
            Number of points to draw.
            Decrease for performance, increase for appearance.
        **kwargs
            Other keyword arguments are passed to the |Shape| constructor.

        """
        return cls.regular_polygon(center, radius, n_vertices, **kwargs)

    @classmethod
    def rectangle(cls, vertices, **kwargs):
        """Shortcut for creating a rectangle aligned with the screen axes from only two corners.

        Parameters
        ----------
        vertices : array-like
            An array containing the ``[x, y]`` positions of two corners.
        **kwargs
            Other keyword arguments are passed to the |Shape| constructor.

        """
        bottom_left, top_right = vertices
        top_left = [bottom_left[0], top_right[1]]
        bottom_right = [top_right[0], bottom_left[1]]
        return cls([bottom_left, bottom_right, top_right, top_left], **kwargs)

    @classmethod
    def from_dict(cls, spec):
        """Create a |Shape| from a dictionary specification.

        Parameters
        ----------
        spec : dict
            A dictionary with either the fields ``'center'`` and ``'radius'`` (for a circle),
            ``'center'``, ``'radius'``, and ``'n_vertices'`` (for a regular polygon),
            or ``'vertices'`.
            If only two vertices are given, they are assumed to be lower left and top right corners of a rectangle.
            Other fields are interpreted as keyword arguments.

        """
        spec = spec.copy()
        center = spec.pop('center', None)
        radius = spec.pop('radius', None)
        if center and radius:
            return cls.circle(center, radius, **spec)

        vertices = spec.pop('vertices')
        if len(vertices) == 2:
            return cls.rectangle(vertices, **spec)

        return cls(vertices, **spec)

    @property
    def vertices(self):
        return np.asarray(point_list(self.poly))

    @property
    def color(self):
        if len(self.colors) == 1:
            return self.colors[self._color]
        else:
            return self._color

    @color.setter
    def color(self, value):
        if value in self.colors:
            self._color = value
        else:
            self.colors[self._color] = value

    @property
    def _kwargs(self):
        """Keyword arguments for recreating the Shape from the vertices.

        """
        return dict(color=self.color, velocity=self.velocity, colors=self.colors)

    @property
    def center(self):
        return np.asarray(self.poly.center())

    @center.setter
    def center(self, value):
        self.translate(np.asarray(value) - self.center)

    @property
    def radius(self):
        return np.linalg.norm(self.vertices - self.center, axis=1).mean()

    @radius.setter
    def radius(self, value):
        self.scale(value / self.radius)

    @property
    def _gl_vertices(self):
        return list(chain(self.center, *point_list(self.poly)))

    @property
    def _gl_colors(self):
        return (len(self) + 1) * self.colors[self._color]

    def distance_to(self, point):
        """Distance from center to arbitrary point.

        Parameters`
        ----------
        point : array-like

        Returns
        -------
        float

        """
        return np.linalg.norm(self.center - point)

    def scale(self, factor):
        """Resize the shape by a proportion (e.g., 1 is unchanged), in-place.

        Parameters
        ----------
        factor : float

        """
        if factor:
            self.poly.scale(factor, factor)

    def translate(self, vector):
        """Translate the shape along a vector, in-place.

        Parameters
        ----------
        vector : array-like

        """
        self.poly.shift(*vector)

    def _get_vertex_list(self):
        indices = []
        for i in range(1, len(self) + 1):
            indices.extend([0, i, i + 1])
        indices[-1] = 1
        return pyglet.graphics.vertex_list_indexed(
            len(self) + 1, indices, ('v2f', self._gl_vertices), ('c3B', self._gl_colors))

    def draw(self):
        """Draw the shape in the current OpenGL context.

        """
        if self.enabled:
            self._vertex_list.colors = self._gl_colors
            self._vertex_list.vertices = self._gl_vertices
            self._vertex_list.draw(pyglet.gl.GL_TRIANGLES)

    def update(self, dt):
        """Update the shape's position by moving it forward according to its velocity.

        Parameters
        ----------
        dt : float

        """
        shift = dt * self.velocity
        self.poly.shift(*shift)

    def enable(self, enabled):
        """Set whether the shape should be drawn.

        """
        self.enabled = enabled

    def overlaps(self, other):
        """Check if two shapes overlap.

        Parameters
        ----------
        other : |Shape|

        Returns
        -------
        bool

        """
        return bool(self.poly.overlaps(other.poly))

    def covers(self, other):
        """Check if the shape completely covers another shape.

        Parameters
        ----------
        other : |Shape|

        Returns
        -------
        bool

        """
        return bool(self.poly.covers(other.poly))

    def __repr__(self):
        if self._kwargs:
            kwarg_strs = []
            for arg, value in self._kwargs.items():
                if isinstance(value, str):
                    value_str = "'{}'".format(value)
                elif isinstance(value, np.ndarray):
                    value_str = '[{}, {}]'.format(*value)
                else:
                    value_str = str(value)
                kwarg_strs.append(arg + '=' + value_str)
            kwargs = ',\n' + ', '.join(kwarg_strs)
        else:
            kwargs = ''

        return '{cls}({points}{kwargs})'.format(
            cls=type(self).__name__,
            points='[{}]'.format(',\n'.join('[{}, {}]'.format(x, y) for x, y in self.vertices)),
            kwargs=kwargs,
        )

    def __eq__(self, other):
        if isinstance(other, Shape):
            return (np.all(np.isclose(np.sort(self.vertices, axis=0), np.sort(other.vertices, axis=0))) and
                    self.colors == other.colors and
                    self.color == other.color and
                    np.all(np.isclose(self.velocity, other.velocity)))
        else:
            return False

    def __bool__(self):
        return True

    def __getitem__(self, item):
        return self.vertices[item]

    def __len__(self):
        return self.poly.nPoints()

    def __add__(self, other):
        return type(self)(self.vertices + other, **self._kwargs)

    __radd__ = __add__

    def __sub__(self, other):
        return type(self)(self.vertices - other, **self._kwargs)

    def __mul__(self, other):
        return type(self)(self.vertices * other, **self._kwargs)

    def __rmul__(self, other):
        return type(self)(other * self.vertices, **self._kwargs)

    def __truediv__(self, other):
        return type(self)(self.vertices / other, **self._kwargs)

    __div__ = __truediv__

    def __xor__(self, other):
        return type(self)(self.poly ^ other.poly, **self._kwargs)

    def __and__(self, other):
        return type(self)(self.poly & other.poly, **self._kwargs)

    def __or__(self, other):
        return type(self)(self.poly | other.poly, **self._kwargs)

    def __iadd__(self, other):
        self.translate(other)
        return self

    def __isub__(self, other):
        self.translate(-np.asarray(other))
        return self

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.poly.scale(other, other)
        elif len(other) == 2:
            self.poly.scale(*other)
        return self

    def __itruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.poly.scale(1/other, 1/other)
        elif len(other) == 2:
            self.poly.scale(1/other[0], 1/other[1])
        return self

    __idiv__ = __itruediv__

    position = center
