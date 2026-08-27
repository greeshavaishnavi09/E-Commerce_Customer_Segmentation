from E_Commerce_Customer_Segmentation.config.configuration import ConfigurationManager
from E_Commerce_Customer_Segmentation.components.data_validation import DataValidation
from E_Commerce_Customer_Segmentation.logging import logger


# pipeline

class DataValidationTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        try:

            logger.info(">>>>>> Data Validation Stage Started <<<<<<")

            config = ConfigurationManager()

            data_validation_config = (config.get_data_validation_config())

            data_validation = DataValidation(config=data_validation_config)

            validation_status = (data_validation.validate_dataset())

            if validation_status:

                logger.info(">>>>>> Data Validation Stage Completed Successfully <<<<<<")

            else:

                logger.info(">>>>>> Data Validation Stage Failed <<<<<<")

            return validation_status

        except Exception as e:

            logger.exception(e)

            raise e
