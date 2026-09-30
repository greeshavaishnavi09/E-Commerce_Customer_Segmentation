# Import libraries

import os
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)

from E_Commerce_Customer_Segmentation.logging import logger
from E_Commerce_Customer_Segmentation.entity.config_entity import ModelEvaluationConfig


class ModelEvaluation:

    def __init__(self, config):

        self.config = config

    # Load transformed RFM data

    def load_data(self):

        rfm = pd.read_csv(
            self.config.transformed_data_file
        )

        logger.info(
            f"RFM data loaded successfully with shape: {rfm.shape}"
        )

        return rfm

    # Load trained model

    def load_model(self):

        model = joblib.load(
            self.config.trained_model_path
        )

        logger.info(
            "Trained model loaded successfully"
        )

        return model

    # Load fitted scaler

    def load_scaler(self):

        scaler = joblib.load(
            self.config.scaler_path
        )

        logger.info(
            "Scaler loaded successfully"
        )

        return scaler

    # Prepare RFM features

    def prepare_data(self, rfm, scaler):

        X = rfm[
            [
                "Recency",
                "Frequency",
                "Monetary"
            ]
        ]

        # Apply same log transformation used during training

        X_log = np.log1p(X)

        # Use saved scaler

        X_scaled = scaler.transform(
            X_log
        )

        X_scaled = pd.DataFrame(
            X_scaled,
            columns=X_log.columns,
            index=X_log.index
        )

        return X_scaled

    # Evaluate final model

    def evaluate_model(self):

        logger.info(
            "Starting Model Evaluation"
        )

        # Load data, model and scaler

        rfm = self.load_data()

        model = self.load_model()

        scaler = self.load_scaler()

        # Prepare data

        X_scaled = self.prepare_data(
            rfm,
            scaler
        )

        # Generate cluster predictions

        labels = model.predict(
            X_scaled
        )

        # Number of clusters

        unique_clusters = np.unique(
            labels
        )

        number_of_clusters = len(
            unique_clusters
        )

        # Calculate clustering metrics

        silhouette = silhouette_score(
            X_scaled,
            labels
        )

        davies_bouldin = davies_bouldin_score(
            X_scaled,
            labels
        )

        calinski_harabasz = calinski_harabasz_score(
            X_scaled,
            labels
        )

        # GMM-specific metrics

        if hasattr(model, "aic"):

            aic = model.aic(
                X_scaled
            )

        else:

            aic = np.nan

        if hasattr(model, "bic"):

            bic = model.bic(
                X_scaled
            )

        else:

            bic = np.nan

        # Create evaluation report

        evaluation_report = pd.DataFrame(
            {
                "Metric": [
                    "Silhouette Score",
                    "Davies-Bouldin Index",
                    "Calinski-Harabasz Score",
                    "AIC",
                    "BIC",
                    "Number of Clusters"
                ],

                "Value": [
                    silhouette,
                    davies_bouldin,
                    calinski_harabasz,
                    aic,
                    bic,
                    number_of_clusters
                ]
            }
        )

        # Display evaluation

        print(
            "\nFinal Model Evaluation:"
        )

        print(
            evaluation_report.round(4)
        )

        # Cluster distribution

        cluster_distribution = (
            pd.Series(labels)
            .value_counts()
            .sort_index()
        )

        # Calculate cluster percentage

        cluster_percentage = (
            cluster_distribution
            / len(labels)
            * 100
        )

        # Create cluster distribution DataFrame

        cluster_distribution_df = pd.DataFrame(
            {
                "CustomerCount": cluster_distribution,
                "Percentage": cluster_percentage
            }
        )

        print(
            "\nCluster Distribution:"
        )

        print(
            cluster_distribution_df.round(2)
        )

        # Create customer cluster profile

        rfm["GMM_Cluster"] = labels

        cluster_profile = (
            rfm
            .groupby("GMM_Cluster")
            .agg(
                Recency=("Recency", "mean"),
                Frequency=("Frequency", "mean"),
                Monetary=("Monetary", "mean"),
                CustomerCount=("CustomerID", "count")
            )
            .reset_index()
        )

        # Calculate cluster percentage

        cluster_profile["Percentage"] = (
            cluster_profile["CustomerCount"]
            / len(rfm)
            * 100
        )

        print(
            "\nCustomer Cluster Profile:"
        )

        print(
            cluster_profile.round(2)
        )

        # Save evaluation report

        evaluation_report.to_csv(
            self.config.report_path,
            index=False
        )

        logger.info(
            f"Evaluation report saved to: {self.config.report_path}"
        )

        # Save cluster profile

        cluster_profile_path = os.path.join(
            self.config.root_dir,
            "cluster_profile.csv"
        )

        cluster_profile.to_csv(
            cluster_profile_path,
            index=False
        )

        logger.info(
            f"Cluster profile saved to: {cluster_profile_path}"
        )

        logger.info(
            "Model Evaluation Completed Successfully"
        )

        return evaluation_report