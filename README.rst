========
pyglet2d
========

Polygon primitives for `pyglet`_.

+--------------------+-------------------+---------------+
| | |travis-badge|   | | |version-badge| | | |git-badge| |
| | |coverage-badge| | | |license-badge| | | |hg-badge|  |
+--------------------+-------------------+---------------+

.. |travis-badge| image:: http://img.shields.io/travis/hsharrison/pyglet2d.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/hsharrison/pyglet2d

.. |coverage-badge| image:: http://img.shields.io/coveralls/hsharrison/pyglet2d.png?style=flat
    :alt: Coverage Status
    :target: https://coveralls.io/r/hsharrison/pyglet2d

.. |version-badge| image:: http://img.shields.io/pypi/v/pyglet2d.png?style=flat
    :alt: PyPi Package
    :target: https://pypi.python.org/pypi/pyglet2d

.. |license-badge| image:: http://img.shields.io/badge/license-BSD-blue.png?style=flat
    :alt: License
    :target: https://pypi.python.org/pypi/pyglet2d

.. |git-badge| image:: http://img.shields.io/badge/repo-git-lightgrey.png?style=flat
    :alt: Git Repository
    :target: https://github.com/hsharrison/pyglet2d

.. |hg-badge| image:: http://img.shields.io/badge/repo-hg-lightgrey.png?style=flat
    :alt: Mercurial Repository
    :target: https://bitbucket.org/hharrison/pyglet2d


This package provides a ``Shape`` object that can be acts as an interface between the libraries `polygon`_ and `pyglet`_.
The former provides numerical routines for handling shapes, and the latter can process OpenGL bindings.
With pyglet2d, you can incorporate 2D shapes into your applications without having to write your own OpenGL calls.

Features
========

- In addition to the standard constructor (from a list or array of points), four others are provided:
  ``Shape.regular_polygon``, ``Shape.circle``, ``Shape.rectangle``, and ``Shape.from_dict``.
  The latter is a specification-based constructor that is easy to use with JSON or YAML.
- ``Shape`` has two methods that are useful as `pyglet`_ callbacks: ``Shape.draw`` and ``Shape.update``.
  A ``Shape`` can be given a velocity and/or an angular velocity, and it will be updated accordingly when ``Shape.update`` is called.
- A ``Shape`` can be manipulated using the methods ``Shape.scale``, ``Shape.rotate``, ``Shape.flip_x``, ``Shape.flip_y``, ``Shape.flip``, and ``Shape.translate``, or with in-place arithmetic (e.g. ``shape += [5, 0]``).
- Alternatively, setting the properties ``Shape.center`` and ``Shape.radius`` will translate and scale the shape, respectively.
- Clipping operations provided by `polygon`_ are bound to the operators \| (union), & (intersection), - (difference), and ^ (xor).
- Additional `polygon`_ methods can be accessed directly from the ``Shape.poly`` attribute, where the ``Polygon`` object is stored.
- Shortcuts are provided to `polygon`_ functions via the boolean methods ``Shape.overlaps(other)`` and ``Shape.covers(other)``.

Example
=======

See ``tests/graphics_demo.py`` for a usage example.
This script also serves as a test.
Run it to make sure that your graphics pipeline is working correctly::

    python tests/graphics_demo.py

Requirements
============

- Python >= 3.3
- `pyglet`_ >= 1.2alpha1. This must be manually installed as it is not on PyPi.
- `polygon`_ >= 3
- `numpy`_

Installation
============

::

    pip install pyglet2d --upgrade

Documentation
=============

https://pyglet2d.readthedocs.org/

Development
===========

To run the all tests run::

    tox

.. _pyglet: http://www.pyglet.org/index.html
.. _polygon: http://www.j-raedler.de/projects/polygon/
.. _numpy: http://www.numpy.org/
