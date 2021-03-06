# -*- coding: utf-8 -*-
import re
import os
import sys

MOCK_MODULES = ['numpy', 'Polygon', 'Polygon.Utils']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'numpydoc',
    'sphinx.ext.intersphinx',
]


class Mock(object):

    __all__ = []

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()


for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()

import pyglet2d

if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    html_theme = 'sphinx_rtd_theme'
    import sphinx_rtd_theme
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
html_static_path = ['_static']
templates_path = ['_templates']

project = 'pyglet2d'
copyright = '2014, Henry S. Harrison'

release = pyglet2d.__version__
split_version = release.split('.')
split_version[-1] = re.match('[0-9]*', split_version[-1]).group(0)
version = '.'.join(split_version)

add_function_parentheses = False
pygments_style = 'sphinx'

numpydoc_show_class_members = False

intersphinx_mapping = {
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'pyglet': ('http://www.pyglet.org/doc-current/', None),
}

rst_epilog = """
.. _pyglet: http://www.pyglet.org/index.html

.. |Polygon| replace:: :class:`Polygon3.Polygon`
.. |array| replace:: :class:`array <numpy.ndarray>`

.. |Shape| replace:: :class:`~pyglet2d.Shape`
.. |Shape.circle| replace:: :meth:`~pyglet2d.Shape.circle`
.. |Shape.rectangle| replace:: :meth:`~pyglet2d.Shape.rectangle`
.. |Shape.regular_polygon| replace:: :meth:`~pyglet2d.Shape.regular_polygon`
.. |Shape.from_dict| replace:: :meth:`~pyglet2d.Shape.from_dict`
.. |Shape.scale| replace:: :meth:`~pyglet2d.Shape.scale`
.. |Shape.translate| replace:: :meth:`~pyglet2d.Shape.translate`

"""
