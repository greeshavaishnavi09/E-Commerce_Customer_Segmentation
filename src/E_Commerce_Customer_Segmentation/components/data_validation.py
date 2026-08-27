import os
import pandas as pd

from E_Commerce_Customer_Segmentation.logging import logger
from E_Commerce_Customer_Segmentation.entity.config_entity import DataValidationConfig


# components


class DataValidation:

    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_dataset(self):

        validation_status = True

        # 1. DATASET EXISTENCE CHECK

        if not os.path.exists(self.config.data_file):

            logger.info("Dataset Not Found")

            return False

        logger.info("Dataset Found")

        # Read Dataset

        df = pd.read_excel(self.config.data_file)

        # 2. DATASET SHAPE CHECK

        rows, columns = df.shape

        logger.info(f"Rows : {rows}")
        logger.info(f"Columns : {columns}")

        if rows == 0:

            logger.info("Dataset is Empty")

            validation_status = False

        if columns == 0:

            logger.info("Dataset has No Columns")

            validation_status = False

        # 3. SCHEMA / EXPECTED COLUMN CHECK

        expected_columns = [
            "InvoiceNo",
            "StockCode",
            "Description",
            "Quantity",
            "InvoiceDate",
            "UnitPrice",
            "CustomerID",
            "Country"
        ]

        actual_columns = list(df.columns)

        missing_columns = (
            set(expected_columns) - set(actual_columns)
        )

        extra_columns = (
            set(actual_columns) - set(expected_columns)
        )

        if not missing_columns and not extra_columns:

            logger.info("Schema Validation Passed")

        else:

            logger.info("Schema Validation Failed")

            if missing_columns:

                logger.info(
                    f"Missing Columns : {missing_columns}"
                )

            if extra_columns:

                logger.info(
                    f"Extra Columns : {extra_columns}"
                )

            validation_status = False

        # 4. DATA TYPE VALIDATION

        expected_dtypes = {
            "InvoiceNo": "object",
            "StockCode": "object",
            "Description": "object",
            "Quantity": "int64",
            "InvoiceDate": "datetime64[ns]",
            "UnitPrice": "float64",
            "CustomerID": "float64",
            "Country": "object"
        }

        actual_dtypes = df.dtypes.astype(str).to_dict()

        for column, expected_dtype in expected_dtypes.items():

            if column not in actual_dtypes:

                logger.info(
                    f"{column} is Missing"
                )

                validation_status = False

            elif actual_dtypes[column] != expected_dtype:

                logger.info(
                    f"{column} datatype mismatch | "
                    f"Expected: {expected_dtype} | "
                    f"Actual: {actual_dtypes[column]}"
                )

                validation_status = False

        logger.info("Data Type Validation Completed")

        # 5. MISSING VALUE VALIDATION

        missing_values = df.isnull().sum()

        logger.info("Missing Value Summary:")
        logger.info(missing_values[missing_values > 0])

        # CustomerID is important for customer segmentation.
        # Description can contain missing values.

        if df["InvoiceDate"].isnull().sum() > 0:

            logger.info(
                "Missing InvoiceDate values found"
            )

            validation_status = False

        if df["Country"].isnull().sum() > 0:

            logger.info(
                "Missing Country values found"
            )

            validation_status = False

        logger.info("Missing Value Validation Completed")

        # 6. DUPLICATE ROW CHECK

        duplicates = df.duplicated().sum()

        logger.info(
            f"Duplicate Rows : {duplicates}"
        )

        if duplicates > 0:

            logger.info(
                "Duplicate rows found. "
                "These will be handled during "
                "data transformation."
            )

        else:

            logger.info(
                "No Duplicate Rows Found"
            )

        # 7. CUSTOMER ID VALIDATION

        missing_customer_id = df["CustomerID"].isnull().sum()

        unique_customers = df["CustomerID"].nunique()

        logger.info(
            f"Missing CustomerID : {missing_customer_id}"
        )

        logger.info(
            f"Unique Customers : {unique_customers}"
        )

        if unique_customers == 0:

            logger.info(
                "No valid CustomerID values found"
            )

            validation_status = False

        else:

            logger.info(
                "CustomerID Validation Completed"
            )

        # 8. QUANTITY VALIDATION

        invalid_quantity = (
            df["Quantity"] <= 0
        ).sum()

        logger.info(
            f"Non-positive Quantity Rows : "
            f"{invalid_quantity}"
        )

        if invalid_quantity > 0:

            logger.info(
                "Non-positive Quantity values found. "
                "These will be handled during "
                "data transformation."
            )

        else:

            logger.info(
                "Quantity Validation Passed"
            )

        # 9. UNIT PRICE VALIDATION

        invalid_unit_price = (
            df["UnitPrice"] <= 0
        ).sum()

        logger.info(
            f"Non-positive UnitPrice Rows : "
            f"{invalid_unit_price}"
        )

        if invalid_unit_price > 0:

            logger.info(
                "Non-positive UnitPrice values found. "
                "These will be handled during "
                "data transformation."
            )

        else:

            logger.info(
                "UnitPrice Validation Passed"
            )

        # 10. INVOICE DATE VALIDATION

        missing_invoice_date = (
            df["InvoiceDate"].isnull().sum()
        )

        if missing_invoice_date > 0:

            logger.info(
                "Invalid InvoiceDate values found"
            )

            validation_status = False

        else:

            logger.info(
                "InvoiceDate Validation Passed"
            )

        # 11. COUNTRY VALIDATION

        missing_country = (
            df["Country"].isnull().sum()
        )

        if missing_country > 0:

            logger.info(
                "Missing Country values found"
            )

            validation_status = False

        else:

            logger.info(
                "Country Validation Passed"
            )

        # 12. WRITE VALIDATION STATUS

        os.makedirs(
            os.path.dirname(
                self.config.status_file
            ),
            exist_ok=True
        )

        with open(
            self.config.status_file,
            "w"
        ) as file:

            file.write(
                f"Validation Status : "
                f"{validation_status}"
            )

        logger.info(
            f"Validation Status : "
            f"{validation_status}"
        )

        return validation_status