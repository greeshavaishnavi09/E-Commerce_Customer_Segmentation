from E_Commerce_Customer_Segmentation.config.configuration import ConfigurationManager
from E_Commerce_Customer_Segmentation.components.model_trainer import ModelTrainer
from E_Commerce_Customer_Segmentation.logging import logger


# pipeline 


class ModelTrainerTrainingPipeline:

    def __init__(self):
        pass

    def main(self):

        try:

            logger.info(">>>>>> Model Trainer Stage Started <<<<<<")

            config = ConfigurationManager()

            model_trainer_config = (config.get_model_trainer_config())

            model_trainer = ModelTrainer(config=model_trainer_config)

            model_trainer.train_models()

            logger.info(">>>>>> Model Trainer Stage Completed Successfully <<<<<<")

        except Exception as e:

            logger.exception(e)

            raise e