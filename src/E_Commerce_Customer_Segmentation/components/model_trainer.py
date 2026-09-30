# Import all libraries

import os
import joblib
import pandas as pd
import numpy as np

from E_Commerce_Customer_Segmentation.logging import logger
from E_Commerce_Customer_Segmentation.entity.config_entity import ModelTrainerConfig

from sklearn.preprocessing import StandardScaler

from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN

from sklearn.mixture import GaussianMixture

from sklearn.metrics import silhouette_score,davies_bouldin_score,calinski_harabasz_score


# components


class ModelTrainer:

    def __init__(self, config):

        self.config = config

    # LOAD TRANSFORMED DATA

    def load_data(self):

        rfm = pd.read_csv(self.config.transformed_data_file)

        return rfm

    # PREPARE DATA

    def prepare_data(self, rfm):

        # Select RFM features

        X = rfm[
            [
                "Recency",
                "Frequency",
                "Monetary"
            ]
        ]

        # Log transformation

        X_log = np.log1p(X)

        # Standardization

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(
            X_log
        )

        X_scaled = pd.DataFrame(
            X_scaled,
            columns=X_log.columns,
            index=X_log.index
        )

        return X_scaled, scaler

    # CALCULATE CLUSTERING METRICS

    def calculate_metrics(
        self,
        X_scaled,
        labels,
        model_name
    ):

        # DBSCAN noise points

        if model_name == "DBSCAN":

            valid_mask = labels != -1

            X_valid = X_scaled[
                valid_mask
            ]

            valid_labels = labels[
                valid_mask
            ]

            unique_clusters = np.unique(
                valid_labels
            )

            noise_percentage = (
                np.sum(labels == -1)
                / len(labels)
            ) * 100

        else:

            X_valid = X_scaled

            valid_labels = labels

            unique_clusters = np.unique(
                labels
            )

            noise_percentage = 0.0

        # Check whether at least two clusters exist

        if len(unique_clusters) >= 2:

            silhouette = silhouette_score(
                X_valid,
                valid_labels
            )

            davies_bouldin = davies_bouldin_score(
                X_valid,
                valid_labels
            )

            calinski_harabasz = calinski_harabasz_score(
                X_valid,
                valid_labels
            )

        else:

            silhouette = np.nan

            davies_bouldin = np.nan

            calinski_harabasz = np.nan

        return {
            "Model": model_name,
            "Silhouette Score": silhouette,
            "Davies-Bouldin Index": davies_bouldin,
            "Calinski-Harabasz Score": calinski_harabasz,
            "Noise Percentage": noise_percentage,
            "Number of Clusters": len(unique_clusters)
        }

    # TRAIN MODELS

    def train_models(self):

        # Load transformed RFM data

        rfm = self.load_data()

        # Prepare data

        X_scaled, scaler = self.prepare_data(
            rfm
        )

        # FINAL MODEL CONFIGURATIONS

        models = {

            "K-Means": KMeans(
                n_clusters=4,
                random_state=42,
                n_init=10
            ),

            "Hierarchical": AgglomerativeClustering(
                n_clusters=4,
                linkage="ward"
            ),

            "DBSCAN": DBSCAN(
                eps=0.5,
                min_samples=7
            ),

            "GMM": GaussianMixture(
                n_components=2,
                covariance_type="spherical",
                n_init=20,
                reg_covar=1e-6,
                random_state=42
            )
        }

        results = []

        trained_models = {}

        cluster_labels = {}

        # TRAIN EACH MODEL

        for model_name, model in models.items():

            print(
                f"Training {model_name}..."
            )

            # Fit model

            labels = model.fit_predict(X_scaled)

            # Calculate metrics

            metrics = self.calculate_metrics(
                X_scaled,
                labels,
                model_name
            )

            results.append(metrics)

            trained_models[model_name] = model

            cluster_labels[model_name] = labels

        # MODEL COMPARISON

        results_df = pd.DataFrame(
            results
        )

        results_df = results_df[
            [
                "Model",
                "Silhouette Score",
                "Davies-Bouldin Index",
                "Calinski-Harabasz Score",
                "Noise Percentage",
                "Number of Clusters"
            ]
        ]

        print("\nModel Comparison:")

        print(results_df.round(4))

        # SELECT FINAL MODEL

        valid_results = results_df.dropna(
            subset=[
                "Silhouette Score"
            ]
        ).copy()

        # Select model using highest Silhouette Score

        best_model_name = (
            valid_results
            .sort_values(
                by=[
                    "Silhouette Score",
                    "Davies-Bouldin Index"
                ],
                ascending=[
                    False,
                    True
                ]
            )
            .iloc[0]["Model"]
        )

        best_model = trained_models[
            best_model_name
        ]

        best_labels = cluster_labels[
            best_model_name
        ]

        print("\nFinal Selected Model:")

        print(best_model_name)

        # SAVE MODEL REPORT

        results_df.to_csv(
            self.config.model_report_path,
            index=False
        )

        # SAVE FINAL MODEL

        joblib.dump(
            best_model,
            self.config.trained_model_path
        )

        # SAVE SCALER

        joblib.dump(scaler,
            self.config.scaler_path
        )

        # SAVE CUSTOMER CLUSTERS

        customer_clusters = rfm.copy()

        customer_clusters[
            "Cluster"
        ] = best_labels

        cluster_file_path = os.path.join(
            self.config.root_dir,
            "customer_clusters.csv"
        )

        customer_clusters.to_csv(
            cluster_file_path,
            index=False
        )

        # SAVE CLUSTER PROFILE

        cluster_profile = (
            customer_clusters
            .groupby("Cluster")
            .agg(
                Recency=("Recency", "mean"),
                Frequency=("Frequency", "mean"),
                Monetary=("Monetary", "mean"),
                CustomerCount=("Cluster", "count")
            )
            .reset_index()
        )

        cluster_profile["Percentage"] = (cluster_profile["CustomerCount"]/ len(customer_clusters)) * 100

        cluster_profile_path = os.path.join(
            self.config.root_dir,
            "cluster_profile.csv"
        )

        cluster_profile.to_csv(
            cluster_profile_path,
            index=False
        )

        # DISPLAY FINAL INFORMATION

        print("\nModel Trainer Completed")

        print("\nModel Report Saved At:")

        print(self.config.model_report_path)

        print("\nFinal Model Saved At:")

        print(self.config.trained_model_path)

        print("\nScaler Saved At:")

        print(self.config.scaler_path)

        print("\nCustomer Clusters Saved At:")

        print(cluster_file_path)

        print("\nCluster Profile Saved At:")

        print(cluster_profile_path)

        return (results_df,best_model_name)