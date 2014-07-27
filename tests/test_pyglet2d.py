from unittest.mock import Mock

import numpy as np
import pytest
import pyglet

from pyglet2d import Shape


def vertex_list_side_effect(*args, **kwargs):
    mock_vertex_list_instance = Mock()
    mock_vertex_list_instance.draw = Mock(return_value=None)
    mock_vertex_list_instance.args = args
    mock_vertex_list_instance.kwargs = kwargs
    return mock_vertex_list_instance


@pytest.fixture(autouse=True)
def mock_pyglet_graphics(monkeypatch):
    mock_vertex_list = Mock(side_effect=vertex_list_side_effect)
    mock_graphics = Mock
    mock_graphics.vertex_list_indexed = mock_vertex_list
    monkeypatch.setattr(pyglet, 'graphics', mock_graphics)
    mock_gl = Mock()
    mock_gl.attach_mock(Mock(name='GL_TRIANGLES'), 'GL_TRIANGLES')
    monkeypatch.setattr(pyglet, 'gl', mock_gl)


def test_regular_polygon():
    shape = Shape.regular_polygon([0, 0], 1, 4)
    assert np.all(np.isclose(
        shape.vertices,
        [[1, 0],
         [0, 1],
         [-1, 0],
         [0, -1]]
    ))


def test_circle():
    assert Shape.circle([0, 0], 1, n_vertices=50) == Shape.regular_polygon([0, 0], 1, 50)


def test_rectangle():
    rect = Shape.rectangle([[-1, -1], [1, 1]])
    other_rect = Shape.regular_polygon([0, 0], np.sqrt(2), 4, start_angle=np.pi/4)
    assert rect == other_rect


def test_circle_from_dict():
    spec = {
        'center': [0, 0],
        'radius': 1,
    }
    assert Shape.from_dict(spec) == Shape.circle([0, 0], 1)


def test_regular_polygon_from_dict():
    spec = {
        'center': [0, 0],
        'radius': 1,
        'n_vertices': 10,
    }
    assert Shape.from_dict(spec) == Shape.regular_polygon([0, 0], 1, 10)


def test_rectangle_from_dict():
    spec = {
        'vertices': [[-1, -1],
                     [1, 1]],
    }
    assert Shape.from_dict(spec) == Shape.rectangle(spec['vertices'])


def test_from_dict():
    spec = {
        'vertices': [[1, 0],
                     [0, 1],
                     [-1, 0],
                     [0, -1]],
        'color': (120, 50, 12),
        'velocity': np.random.sample(2),
    }
    assert Shape.from_dict(spec) == Shape(spec['vertices'], color=spec['color'], velocity=spec['velocity'])


def test_colors():
    colors = {
        'primary': (0, 0, 0),
        'secondary': (100, 100, 100),
        'flashing': (20, 10, 89),
    }
    shape = Shape.circle([0, 0], 1, colors=colors)
    assert shape.color == 'primary'
    shape.color = 'secondary'
    assert shape.color == 'secondary'
    shape.color = (72, 71, 8)
    assert shape.color == 'secondary'
    shape.color = 'flashing'
    assert shape.colors['secondary'] == (72, 71, 8)


def test_color():
    shape = Shape.circle([0, 0], 1, color=(1, 2, 3))
    assert shape.color == (1, 2, 3)
    shape.color = (10, 20, 30)
    assert shape.color == (10, 20, 30)


def test_update():
    shape = Shape.circle([0, 0], 1, velocity=[1, 1])
    shape.update(1)
    assert np.all(np.isclose(shape.center, [1, 1]))

    shape = Shape.regular_polygon([0, 0], 1, 6, angular_velocity=1, velocity=[-2, 2])
    shape.update(0.5)
    assert shape == Shape.regular_polygon([-1, 1], 1, 6, angular_velocity=1, velocity=[-2, 2], start_angle=0.5)


def test_repr():
    shape = Shape.circle([0, 0], 1, velocity=[1, 1], color=(1, 2, 3), colors={'a': (20, 6, 169)})
    assert eval(repr(shape)) == shape


def test_translate():
    shape = Shape.circle([0, 0], 1)
    shape.translate([10, 10])
    assert shape == Shape.circle([10, 10], 1)


def test_scale():
    shape = Shape.circle([0, 0], 1)
    shape.scale(10)
    assert shape == Shape.circle([0, 0], 10)

    shape = Shape.rectangle([[-1, -1], [1, 1]])
    shape.scale([2, 5])
    assert shape == Shape.rectangle([[-2, -5], [2, 5]])

    shape = Shape.rectangle([[-1, -1], [1, 1]])
    shape.scale(2, center=[1, 1])
    assert shape == Shape.rectangle([[-3, -3], [1, 1]])


def test_rotate():
    shape = Shape.rectangle([[-1, -1], [1, 1]])
    shape.rotate(np.pi/2)
    assert shape == Shape.rectangle([[-1, -1], [1, 1]])
    shape.rotate(np.pi/4)
    assert shape == Shape.regular_polygon([0, 0], np.sqrt(2), 4)

    shape = Shape.rectangle([[-1, -1], [1, 1]])
    shape.rotate(np.pi/2, [1, 1])
    assert shape == Shape.rectangle([[1, -1], [3, 1]])


def test_flip():
    shape = Shape.rectangle([[-1, -1], [1, 1]])
    shape.flip_x()
    assert shape == Shape.rectangle([[-1, -1], [1, 1]])
    shape.flip_y()
    assert shape == Shape.rectangle([[-1, -1], [1, 1]])

    shape.flip_x([1, 0])
    assert shape == Shape.rectangle([[1, -1], [3, 1]])

    shape.flip_y([0, 1])
    assert shape == Shape.rectangle([[1, 1], [3, 3]])

    shape -= [2, 2]
    shape.flip(np.pi/4)
    assert shape == Shape.rectangle([[-1, -1], [1, 1]])
    shape.flip(np.pi/4, center=[-1, 1])
    assert shape == Shape.rectangle([[-3, 1], [-1, 3]])


def test_from_polygon():
    shape = Shape.circle([0, 0], 1)
    assert shape == Shape(shape.poly)


def test_arithmetic():
    shape = Shape.circle([0, 0], 1, color=(0, 0, 0))
    assert shape + [1, 10] == [1, 10] + shape == Shape.circle([1, 10], 1, color=(0, 0, 0))
    assert shape - [1, 10] == Shape.circle([-1, -10], 1, color=(0, 0, 0))
    assert 10 * shape == shape * 10 == Shape.circle([0, 0], 10, color=(0, 0, 0))
    stretched = shape * np.array([2, 4])
    assert [2, 4] * shape == stretched
    for point in stretched.vertices:
        assert np.isclose(np.linalg.norm(point / [2, 4]), 1)


def test_in_place_arithmetic():
    shape = Shape.rectangle([[-1, -1], [1, 1]])
    shape += [10, 5]
    assert shape != Shape.rectangle([[-1, -1], [1, 1]])
    assert shape == Shape.rectangle([[9, 4], [11, 6]])
    shape -= [10, 5]
    assert shape == Shape.rectangle([[-1, -1], [1, 1]])
    shape *= 10
    assert shape != Shape.rectangle([[-1, -1], [1, 1]])
    assert shape == Shape.rectangle([[-10, -10], [10, 10]])
    shape /= 10
    assert shape == Shape.rectangle([[-1, -1], [1, 1]])
    shape *= [1, 5]
    assert shape != Shape.rectangle([[-1, -1], [1, 1]])
    assert shape == Shape.rectangle([[-1, -5], [1, 5]])
    shape /= [10, 1]
    assert shape == Shape.rectangle([[-0.1, -5], [0.1, 5]])


def test_overlaps():
    a = Shape.circle([-1, 0], 1)
    b = a + [2, 0]
    assert not a.overlaps(b)
    a += [1.01, 0]
    assert a.overlaps(b)


def test_covers():
    a = Shape.circle([-1, 0], 1)
    b = a / 2 + [0.5, 0.5]
    assert not a.covers(b)
    a *= 2
    assert a.covers(b)


def test_union():
    assert Shape.rectangle([[-1, 0], [0, 1]]) | Shape.rectangle([[0, 0], [1, 1]]) == Shape.rectangle([[-1, 0], [1, 1]])


def test_intersection():
    assert Shape.rectangle([[-1, 0], [1, 2]]) & Shape.rectangle([[0, 0], [1, 1]]) == Shape.rectangle([[0, 0], [1, 1]])


def test_difference():
    assert Shape.rectangle([[-1, 0], [1, 3]]) - Shape.rectangle([[0, 0], [2, 3]]) == Shape.rectangle([[-1, 0], [0, 3]])


def test_xor():
    assert Shape.rectangle([[-1, 0], [0, 1]]) ^ Shape.rectangle([[0, 0], [1, 1]]) == Shape.rectangle([[-1, 0], [1, 1]])
    assert ((Shape.rectangle([[-1, 0], [0.5, 1]]) ^ Shape.rectangle([[-0.5, 0], [1, 1]])) ==
            (Shape.rectangle([[-1, 0], [1, 1]])) - Shape.rectangle([[-0.5, 0], [0.5, 1]]))


def test_center():
    shape = Shape.rectangle([[-1, -1], [1, 1]])
    assert np.all(np.isclose(shape.center, [0, 0]))
    shape.center = [1, 1]
    assert shape == Shape.rectangle([[0, 0], [2, 2]])


def test_radius():
    shape = Shape.circle([0, 0], 1)
    assert shape.radius == 1
    shape.radius = 0.1
    assert shape == Shape.circle([0, 0], 0.1)


def test_distance_to():
    shape = Shape.circle([0, 0], 1)
    assert np.isclose(shape.distance_to([1, 1]), np.sqrt(2))


def test_eq():
    assert Shape.regular_polygon([0, 0], 1, 4) != Shape.regular_polygon([0, 0], 1, 5)
    assert Shape.regular_polygon([0, 0], 1, 4) == Shape.regular_polygon([0, 0], 1, 4, start_angle=np.pi)


def test_neq():
    assert Shape.circle([0, 0], 1) != 0


def test_bool():
    assert Shape.circle([0, 0], 1)


def test_getitem():
    assert np.all(Shape.regular_polygon([0, 0], 1, 10)[0] == [1, 0])


def test_vertex_list():
    shape = Shape.rectangle([[-1, -1], [1, 1]], color=(100, 100, 100))
    indices = [0, 1, 2,
               0, 2, 3,
               0, 3, 4,
               0, 4, 1]
    vertices = [0, 0,
                -1, -1,
                1, -1,
                1, 1,
                -1, 1],
    colors = 5 * [100, 100, 100]

    args = shape._vertex_list.args
    assert len(args) == 4
    assert args[0] == 5
    assert args[1] == indices
    assert args[2][0] == 'v2f'
    assert np.all(np.isclose(args[2][1], vertices))
    assert args[3][0] == 'c3B'
    assert np.all(np.isclose(args[3][1], colors))


def test_enable_disable():
    shape = Shape.rectangle([[-1, -1], [1, 1]], color=(100, 100, 100))
    shape.enable(False)
    shape.draw()
    assert not shape._vertex_list.draw.called
    shape.enable(True)
    shape.draw()
    assert shape._vertex_list.draw.call_count == 1
    call_args = shape._vertex_list.draw.call_args
    assert len(call_args[0]) == 1
    gl_triangles = call_args[0][0]
    assert isinstance(gl_triangles, Mock)

