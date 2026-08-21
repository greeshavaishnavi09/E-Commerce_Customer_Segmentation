# import libraries for component

import os
import shutil

from pathlib import Path

from E_Commerce_Customer_Segmentation.logging import logger
from E_Commerce_Customer_Segmentation.utils.common import get_size
from E_Commerce_Customer_Segmentation.entity.config_entity import DataIngestionConfig

# component

class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def copy_data_file(self):

        if not os.path.exists(self.config.local_data_file):

            shutil.copy(
                self.config.source_data_file,
                self.config.local_data_file
            )

            logger.info("Dataset copied successfully")

        else:

            logger.info("Dataset already exists")