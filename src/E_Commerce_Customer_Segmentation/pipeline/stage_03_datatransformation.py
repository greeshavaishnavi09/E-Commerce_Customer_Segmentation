from E_Commerce_Customer_Segmentation.config.configuration import ConfigurationManager
from E_Commerce_Customer_Segmentation.components.data_transformation import DataTransformation
from E_Commerce_Customer_Segmentation.logging import logger


# pipeline 


class DataTransformationTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        try:

            logger.info(">>>>>> Data Transformation Stage Started <<<<<<")

            config = ConfigurationManager()

            data_transformation_config = (config.get_data_transformation_config())

            data_transformation = DataTransformation(config=data_transformation_config)

            data_transformation.transform_data()

            logger.info(">>>>>> Data Transformation Stage Completed Successfully <<<<<<")

        except Exception as e:

            logger.exception(e)

            raise e