from setuptools import setup, find_packages
import sys, os

version = '1.0dev'
shortdesc = "Dicttree qt renderers"
longdesc = ''
#longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
#longdesc += open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()
#longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

setup(name='dicttree.qt',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Operating System :: OS Independent',
            'Programming Language :: Python',
      ], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Florian Friesdorf',
      author_email='flo@chaoflow.net',
      url='https://github.com/chaoflow/dicttree.qt',
      license='',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['dicttree'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'dicttree',
      ],
      extras_require={
          'test': [
              'interlude',
              'plone.testing',
              'unittest2',
              'zope.configuration',
              'zope.testing',
          ]
      },
      entry_points="""
      """,
      )
