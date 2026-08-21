from E_Commerce_Customer_Segmentation.pipeline.stage_01_dataingestion import DataIngestionTrainingPipeline
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