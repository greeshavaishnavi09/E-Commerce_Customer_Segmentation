from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_data_file: Path
    local_data_file: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_file: Path
    status_file: Path    


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_file: Path
    transformed_data_file: Path   


@dataclass(frozen=True)
class ModelTrainerConfig:

    root_dir: Path

    # Transformed customer RFM data
    transformed_data_file: Path

    # Path to save final trained model
    trained_model_path: Path

    # Path to save scaler
    scaler_path: Path

    # Path to save model comparison report
    model_report_path: Path 