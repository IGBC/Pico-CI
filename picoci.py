import logging
import argparse
import shutil
from os import chdir, getcwd
from shlex import split
from flask import Flask, request
from tempfile import makedtemp
from subprocess import run, PIPE

__version__ = '0.0.1-git'
__description__ = 'Simple script to build and deploy git repos'

app = Flask(__name__)

@app.route('/', methods=['POST'])
def remote_update():
    ''' Triggers updater from webhook '''
    logger = logging.getLogger('picoci.update')
    logger.debug('Recieved Request with data: %s' % request.form)
    return 'OK'

def local_update():
    ''' Triggers updater from local machine '''
    logger = logging.getLogger('picoci.update')
    logger.info('Update requested from local machine')
    build_and_deploy()

def build_and_deploy():
    ''' clones source repo and runs build and deploy scripts '''
    logger = logging.getLogger('picoci.bad')
    
    # Create a tempory dir to use as scratch disk
    logging.debug('making temp dir')
    path = makedtemp()
    
    # Switch into tempdir
    logger.debug('cd_ing into %s' % path)
    chdir(path)
    
    # If the repo is blank log an error and exit
    if not app.config['REPO_URL']:
        logger.fatal('No repository defined in config file. Cannot update.')
        return 
    
    # Clone Repo
    if not clone(path):
        logger.error('Repository Clone failed.')
        shutil.rmtree(path)
        return
    # Build App
    if not build(path):
        logger.error('Build step failed.')
        shutil.rmtree(path)
        return
    # deploy App
    if not deploy(path):
        logger.error('Deploy step failed.')
        shutil.rmtree(path)
        return
    
    #Remove the temp dir again.
    logger.debug('Removing temp dir' % path)
    shutil.rmtree(path)
  
def clone(path):
    ''' Clones the repo
        Returns success '''
    logger = logging.getLogger('picoci.clone')
    logger.info('Cloning %s' % app.config['REPO_URL'])
    command = 'git clone %s %s' % (app.config['REPO_URL'], path)
    logger.debug('clone command: %s' % command)        
    return run_cmd(command, logger)
        
    
def build(path):
    ''' Runs the build step
        Returns success '''
    logger = logging.getLogger('picoci.build')
    # Skip if no script defined
    if not app.config['BUILD_SCRIPT']:
        logger.debug('No build script listed, skipping.')
        return True
    
    logger.info('Running build script')
    command = './' + app.config['BUILD_SCRIPT']
    logger.debug('build command: %s' % command)
    return run_cmd(command, logger)

def deploy(path):
    ''' Runs the deploy step
        Returns success '''
    logger = logging.getLogger('picoci.deploy')
    # Skip if no script defined
    if not app.config['DEPLOY_SCRIPT']:
        logger.debug('No deploy script listed, skipping.')
        return True
    
    logger.info('Running deploy script')
    command = './' + app.config['DEPLOY_SCRIPT']
    logger.debug('deploy command: %s' % command)
    return run_cmd(command, logger)

def run_cmd(command, logger):
    ''' Run shell command,
    log the shit out of errors.
        Returns success'''
    # Run clone command and dump stdout into output
    output = run(split(command), stdout=PIPE)
    # If return code is not 0 (SUCCESS) log the shit out of what happened
    if output.returncode:
        logger.error('Command returned non 0 code %s. Stopping' % output.returncode)
        logger.error('%s ARGS: "%s"' % (output.returncode, output.args))
        logger.error('WK_DIR: "%s"' % getcwd())
        logger.error('STDOUT: "%s"' % output.stdout)
        return False
    else:
        return True

def main():
    ''' It's the entry point '''
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
