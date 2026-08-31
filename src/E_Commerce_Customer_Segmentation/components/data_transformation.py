import os
import pandas as pd

from E_Commerce_Customer_Segmentation.logging import logger
from E_Commerce_Customer_Segmentation.entity.config_entity import DataTransformationConfig


# components


class DataTransformation:

    def __init__(self, config: DataTransformationConfig):

        self.config = config

    def transform_data(self):

        logger.info("Starting Data Transformation")

        # Read dataset

        df = pd.read_excel(self.config.data_file)

        logger.info(f"Original dataset shape: {df.shape}")

        # Remove duplicate rows

        df = df.drop_duplicates()

        logger.info(f"Shape after removing duplicates: {df.shape}")

        # Remove transactions without CustomerID

        df = df.dropna(subset=["CustomerID"])

        logger.info(f"Shape after removing missing CustomerID: {df.shape}")

        # Remove cancelled invoices

        df = df[
            ~df["InvoiceNo"]
            .astype(str)
            .str.startswith("C")
        ]

        logger.info(f"Shape after removing cancelled invoices: {df.shape}")

        # Keep positive quantities

        df = df[df["Quantity"] > 0]

        logger.info(f"Shape after removing invalid quantities: {df.shape}")

        # Keep positive unit prices

        df = df[df["UnitPrice"] > 0]

        logger.info(f"Shape after removing invalid prices: {df.shape}")

        # Create Revenue

        df["Revenue"] = (
            df["Quantity"] *
            df["UnitPrice"]
        )

        # Reference date for Recency

        reference_date = (
            df["InvoiceDate"].max()
            + pd.Timedelta(days=1)
        )

        # Create RFM dataset

        rfm = df.groupby("CustomerID").agg(
            Recency=(
                "InvoiceDate",
                lambda x:
                (reference_date - x.max()).days
            ),

            Frequency=(
                "InvoiceNo",
                "nunique"
            ),

            Monetary=(
                "Revenue",
                "sum"
            )
        )

        # Reset index

        rfm = rfm.reset_index()

        logger.info(f"Customer RFM shape: {rfm.shape}")

        # Save transformed data

        os.makedirs(self.config.root_dir,
            exist_ok=True
        )

        rfm.to_csv(
            self.config.transformed_data_file,
            index=False
        )

        logger.info(
            f"Transformed data saved to: "
            f"{self.config.transformed_data_file}"
        )

        return rfm