import logging
import argparse
import shutil
from flask import Flask, request
from tempfile import makedtemp


__version__ = '0.0.1-git'
__description__ = 'Simple script to build and deploy git repos'

app = Flask(__name__)

@app.route("/", methods=['POST'])
def remote_update():
    logger.getLogger('picoci.update')
    logger.info('Recieved Request with data: %s' % request.form)
    return 'OK'

def local_update():
    build_and_deploy()

def build_and_deploy():
    #create a tempory dir to use as scratch disk
    path = makedtemp()
    if app.config['REPO_URL']:
        
    shutil.rmtree(path)



def main():
    # Configure Argparse
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('config file', type=str)
    parser.add_argument('-v, --version', action='version', version=__version__)
    # Set up logger
    logger = logging.getLogger('picoci')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s]: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    args = parser.parse_args().__dict__
    logger.info('Started with arguments: %s' % args)

    # Load default config and override config from an environment variable
    app.config.update(dict(
        REPO_URL='',
        DEPLOY_KEY='',
        BUILD_SCRIPT='',
        DEPLOY_SCRIPT='',
    ))
    app.config.from_pyfile(args['config file'])