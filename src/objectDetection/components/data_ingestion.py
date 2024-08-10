from objectDetection import *
from objectDetection.constants import *

import os
import urllib.request as request
from objectDetection import logger
from objectDetection.utils.common import get_size
import zipfile
from objectDetection.entity.config_entity import DataIngestionConfig
from objectDetection.config.configuration import configurationManager
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url =self.config.source_url,
                filename= self.config.local_data_file
            )
            logger.info(f'{filename} downloaded! with following info: \n{headers}')
        else:
            logger.info(f'file already exists of size:{get_size(Path(self.config.local_data_file))}')


    def extract_zip_file(self):

        unzip_path = self.config.unzip_dir

        p=os.makedirs(unzip_path, exist_ok=True)
        print(p)
        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_ref:
            zip_ref.extractall(unzip_path)


