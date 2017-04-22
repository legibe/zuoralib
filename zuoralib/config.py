import os
import logging
import logging.config
import yaml

tenant = 'dev'

def load_config():
    root = os.path.join(os.path.expanduser('~'), '.creds')
    path = os.path.join(root, 'zuora.yaml')
    with open(path) as f:
        config = yaml.load(f)
        config = config[tenant]['soap']
        config['wsdl'] = os.path.join(root, config['wsdl'])
    return config

config = load_config()

def get_logger(name='zuoralib'):
    logger = logging.getLogger(name)
    return logger

logger = get_logger()
