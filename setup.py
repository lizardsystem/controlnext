from setuptools import setup

version = '0.12'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
])

install_requires = [
    'Django',
    'django-extensions',
    'django-nose',
    'python-dateutil == 1.5',
    'lizard-ui >= 4.0, < 5.0',
    'lizard-map >= 4.0, < 5.0',
    'lizard-fewsjdbc >= 2.7',
    'pytz',
    'djangorestframework',
    'pandas >= 0.9.0',
    'numpy >= 1.6',
    'factory_boy',
    'suds',
    'requests',
    'translations',
],

tests_require = []

setup(name='controlnext',
      version=version,
      description="Delfland watersturing van glastuinbouw basins.",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Sander Smits',
      author_email='sander.smits@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['controlnext', 'controlnext_demo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [],
          'lizard_map.adapter_class': [
              'adapter_basin_fill = controlnext.layers:BasinsAdapter',
          ]
      })
