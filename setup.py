from setuptools import setup, find_packages

from picoci import __version__, __description__

setup(
    name='pico-ci',
    version=__version__,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points = {
        'console_scripts': ['pysketch=pico-ci:main'],
    },
    install_requires=[
        "flask",
    ],
    url='https://github.com/IGBC/Pico-CI',
    # license='GPL V3.0',
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Environment :: Console',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Natural Language :: English',],
    author='IGBC',
    author_email='segfault@c-base.org',
    description=__description__,
    long_description='Simple script to build and deploy git repos, that I built to publish my blog\nSee: https://github.com/IGBC/Pico-CI',
)
