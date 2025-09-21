import os
import yaml

def load_config():
    '''Load configuration from a YAML file located in the config directory.'''
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_dir, 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config =  yaml.safe_load(f)
    return config

if __name__ == "__main__":
    '''Test the configuration loader.'''
    print(load_config())