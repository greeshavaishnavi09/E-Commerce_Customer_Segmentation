from E_Commerce_Customer_Segmentation.config.configuration import ConfigurationManager
from E_Commerce_Customer_Segmentation.components.prediction import Prediction
from E_Commerce_Customer_Segmentation.logging import logger


class PredictionPipeline:

    def __init__(self):
        pass

    def main(self, recency, frequency, monetary):

        try:

            logger.info(">>>>>> Prediction Stage Started <<<<<<")

            config = ConfigurationManager()
            prediction_config = config.get_prediction_config()

            prediction = Prediction(config=prediction_config)

            result = prediction.predict_customer(
                recency=recency,
                frequency=frequency,
                monetary=monetary
            )

            logger.info(">>>>>> Prediction Stage Completed Successfully <<<<<<")

            return result

        except Exception as e:

            logger.exception(e)
            raise e