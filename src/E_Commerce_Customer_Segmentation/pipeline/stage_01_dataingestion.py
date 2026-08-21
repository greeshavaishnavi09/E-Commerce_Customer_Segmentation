from E_Commerce_Customer_Segmentation.config.configuration import ConfigurationManager
from E_Commerce_Customer_Segmentation.components.data_ingestion import DataIngestion
from E_Commerce_Customer_Segmentation.logging import logger

# pipeline
class DataIngestionTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        try:

            print("--- STARTING DATA INGESTION PIPELINE ---")

            config = ConfigurationManager()

            data_ingestion_config = config.get_data_ingestion_config()

            data_ingestion = DataIngestion(config=data_ingestion_config)

            data_ingestion.copy_data_file()

            print("--- DATA INGESTION COMPLETED SUCCESSFULLY ---")

        except Exception as e:
            raise e