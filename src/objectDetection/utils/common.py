import os
from box.exceptions import BoxValueError
import yaml
from objectDetection import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yamal(path_to_yaml: Path) -> ConfigBox:

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f'yaml_file:{path_to_yaml} loaded successfully')
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories:list, verbose=True):
    """create list of Directories

    Arg:
      path_to_directories (list): list of path of directories
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f'create directory at:{path}')


def get_size(path: Path) -> str:

    size_in_kb = round(os.path.getsize(path)/1024)
    return f"{size_in_kb}KB"
