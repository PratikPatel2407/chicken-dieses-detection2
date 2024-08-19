from dataclasses import dataclass
from pathlib import Path
from objectDetection.utils.common import read_yamal, create_directories, get_size
from objectDetection.constants import *




class configurationManager:
    def __init__(self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yamal(config_filepath)
        self.params = read_yamal(params_filepath)

        create_directories([self.config.artifacts_root])





""""pipeline"""

