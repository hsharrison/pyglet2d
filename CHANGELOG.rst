
Changelog
=========

0.2.1 (2014-07-27)
------------------

* All in-place operations now return the ``Shape``, allowing operations to be chained.

0.2.0 (2014-07-27)
------------------

* Added optional arguments ``y_factor`` and ``center`` to ``Shape.scale``.
* Implemented ``Shape.rotate``.
* Implemented angular velocity.
* Argument ``start_angle`` in ``Shape.regular_polygon`` is now in radians.
* ``graphics_test.py`` renamed to ``graphics_demo.py``.
* Implement ``Shape.flip_x``, ``Shape.flip_y``, and ``Shape.flip``.
* Explicitly set the ``Polygon3`` data style to ``STYLE_NUMPY``.
* Implement ``Shape`` union and difference with the addition and subtraction operators.
* Don't throw an error when comparing the equality of shapes with different numbers of vertices.

0.1.2 (2014-07-26)
------------------

* Fixed Shape docstring.
* Changed docs from napoleon to numpydoc.

0.1.1 (2014-07-26)
------------------

* Mocking of graphics calls to pyglet, for testing without a display (e.g., on Travis).
* Fixed intersphinx links in docs.
* Fixed coveralls.io integration.

0.1.0 (2014-07-25)
------------------

* First release on PyPI.
