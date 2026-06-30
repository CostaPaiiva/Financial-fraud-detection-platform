import os

import pandas as pd


# Define the path to the raw transactions dataset.
RAW_DATA_PATH = "data/raw/transactions_raw.csv"


def test_raw_dataset_exists():
    """
    Test to ensure that the raw dataset file exists at the specified path.
    This is a basic check to confirm the data extraction step has produced a file.
    """
    assert os.path.exists(RAW_DATA_PATH)


def test_raw_dataset_has_required_columns():
    """
    Test to verify that the raw dataset contains all expected columns.
    It reads the CSV and checks if a predefined set of critical columns are present.
    """
    df = pd.read_csv(RAW_DATA_PATH)

    required_columns = {
        "transaction_id",
        "customer_id",
        "transaction_date",
        "transaction_hour",
        "amount",
        "transaction_type",
        "merchant_category",
        "channel",
        "device_type",
        "city",
        "country",
        "previous_transactions_count",
        "average_customer_amount",
        "is_foreign_transaction",
        "is_high_risk_country",
        "is_fraud",
    }

    # Assert that all required columns are a subset of the DataFrame's columns.
    assert required_columns.issubset(df.columns)


def test_raw_dataset_has_records():
    """
    Test to ensure that the raw dataset is not empty.
    It checks if the DataFrame loaded from the CSV contains at least one record.
    """
    df = pd.read_csv(RAW_DATA_PATH)

    # Assert that the DataFrame has more than zero rows.
    assert len(df) > 0


def test_fraud_column_is_binary():
    """
    Test to confirm that the 'is_fraud' column contains only binary values (0 or 1).
    It extracts unique values from the 'is_fraud' column, ignoring NaN, and
    asserts that these values are either 0 or 1.
    """
    df = pd.read_csv(RAW_DATA_PATH)

    # Get unique values from 'is_fraud' column, dropping any NaN values.
    unique_values = set(df["is_fraud"].dropna().unique())

    # Assert that all unique values are either 0 or 1.
    assert unique_values.issubset({0, 1})