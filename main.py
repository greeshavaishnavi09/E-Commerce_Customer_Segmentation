from E_Commerce_Customer_Segmentation.pipeline.stage_01_dataingestion import DataIngestionTrainingPipeline
from E_Commerce_Customer_Segmentation.pipeline.stage_02_datavalidation import DataValidationTrainingPipeline
from E_Commerce_Customer_Segmentation.pipeline.stage_03_datatransformation import DataTransformationTrainingPipeline
from E_Commerce_Customer_Segmentation.logging import logger


STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} Started <<<<<<")

    obj = DataIngestionTrainingPipeline()
    obj.main()

    logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<")

except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Validation Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} Started <<<<<<")

    obj = DataValidationTrainingPipeline()
    obj.main()

    logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<")

except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME = "Data Transformation Stage"

try:
    logger.info(f">>>>>> Stage {STAGE_NAME} Started <<<<<<")

    obj = DataTransformationTrainingPipeline()
    obj.main()

    logger.info(f">>>>>> Stage {STAGE_NAME} Completed <<<<<<")

except Exception as e:
    logger.exception(e)
    raise e