
# import lib

import os
import joblib
import numpy as np
import pandas as pd


class Prediction:

    def __init__(self, config):

        self.config = config

        self.model = joblib.load(self.config.trained_model_path)
        self.scaler = joblib.load(self.config.scaler_path)

    def predict_customer(self, recency, frequency, monetary):

        # Create customer RFM data
        customer = pd.DataFrame({
            "Recency": [recency],
            "Frequency": [frequency],
            "Monetary": [monetary]
        })

        # Apply log transformation
        customer_log = np.log1p(customer)

        # Apply saved scaler
        customer_scaled = self.scaler.transform(customer_log)

        # Predict cluster
        predicted_cluster = self.model.predict(customer_scaled)[0]

        # Get membership probabilities
        probabilities = self.model.predict_proba(customer_scaled)[0]

        # Get probability of predicted cluster
        membership_probability = probabilities[predicted_cluster]

        return {
            "Cluster": int(predicted_cluster),
            "Membership_Probability": float(membership_probability)
        }