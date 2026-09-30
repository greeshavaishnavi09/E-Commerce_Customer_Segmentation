from E_Commerce_Customer_Segmentation.config.configuration import ConfigurationManager
from E_Commerce_Customer_Segmentation.components.model_evaluation import ModelEvaluation
from E_Commerce_Customer_Segmentation.logging import logger

class ModelEvaluationTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        try:

            logger.info(">>>>>> Model Evaluation Stage Started <<<<<<")

            config = ConfigurationManager()

            model_evaluation_config = (config.get_model_evaluation_config())

            model_evaluation = ModelEvaluation(config=model_evaluation_config)

            model_evaluation.evaluate_model()

            logger.info(">>>>>> Model Evaluation Stage Completed Successfully <<<<<<")

        except Exception as e:

            logger.exception(e)

            raise e