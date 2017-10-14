import logging
import argparse

__version__ = '0.0.1-git'
__description__ = 'Simple script to build and deploy git repos'

def main():
    # Configure Argparse
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('config file', type=str)
    parser.add_argument('-v, --version', action='version', version=__version__)
    # Set up logger
    logger = logging.getLogger('pico-ci')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    args = parser.parse_args().__dict__