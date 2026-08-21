from E_Commerce_Customer_Segmentation.constant import *
from E_Commerce_Customer_Segmentation.logging import logger
from pathlib import Path
from E_Commerce_Customer_Segmentation.utils.common import read_yaml,create_directories
from E_Commerce_Customer_Segmentation.entity.config_entity import DataIngestionConfig

class ConfigurationManager:

    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH
    ):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:

        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_data_file=config.source_data_file,
            local_data_file=config.local_data_file
        )

        return data_ingestion_config