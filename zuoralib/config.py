import os
import logging
import logging.config
import yaml

def load_config():
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'etc')

    config = yaml.load(file(path + '/config.yaml'))
    config['config_root'] = path
    return config

config = load_config()

def get_logger(name='zuoralib'):
    logger = logging.getLogger(name)
    logging.config.dictConfig(config['logging'])
    return logger

logger = get_logger
