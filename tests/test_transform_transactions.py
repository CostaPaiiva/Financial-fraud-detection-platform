import os

import pandas as pd


# Define the path to the processed transactions dataset.
PROCESSED_DATA_PATH = "data/processed/transactions_processed.csv"


def test_processed_dataset_exists():
    """
    Test to ensure that the processed dataset file exists at the specified path.
    This confirms the data transformation step has successfully produced an output file.
    """
    assert os.path.exists(PROCESSED_DATA_PATH)


def test_processed_dataset_has_features():
    """
    Test to verify that the processed dataset contains all expected new features
    generated during the transformation process.
    """
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Define the set of features that are expected to be present after transformation.
    expected_features = {
        "amount_above_customer_avg",
        "amount_difference_from_avg",
        "amount_risk_level",
        "transaction_amount_category",
        "customer_activity_level",
        "is_night_transaction",
        "is_weekend",
        "is_business_hours",
        "rule_based_risk_score",
        "risk_level",
    }

    # Assert that all expected features are a subset of the DataFrame's columns.
    assert expected_features.issubset(df.columns)


def test_processed_dataset_has_no_required_nulls():
    """
    Test to ensure that critical columns, which should have been handled for missing values
    during transformation, do not contain any nulls.
    """
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # List of columns that are expected to be entirely non-null after processing.
    required_columns = [
        "transaction_id",
        "customer_id",
        "transaction_date",
        "amount",
        "transaction_type",
        "merchant_category",
        "channel",
        "device_type",
        "city",
        "country",
        "is_fraud",
    ]

    # Calculate the sum of null values across these required columns. It should be 0.
    assert df[required_columns].isna().sum().sum() == 0


def test_transaction_id_is_unique():
    """
    Test to verify that the 'transaction_id' column contains only unique values.
    Duplicate IDs would indicate a data integrity issue.
    """
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Assert that all values in 'transaction_id' are unique.
    assert df["transaction_id"].is_unique


def test_amount_is_not_negative():
    """
    Test to ensure that all values in the 'amount' column are non-negative.
    Negative transaction amounts are typically invalid.
    """
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Assert that all values in 'amount' are greater than or equal to 0.
    assert (df["amount"] >= 0).all()


def test_rule_based_risk_score_between_0_and_100():
    """
    Test to check if the 'rule_based_risk_score' is within the expected range of 0 to 100.
    This validates the scoring logic applied during feature creation.
    """
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Assert that all values in 'rule_based_risk_score' are between 0 and 100 (inclusive).
    assert df["rule_based_risk_score"].between(0, 100).all()


def test_is_fraud_is_binary():
    """
    Test to confirm that the 'is_fraud' column contains only binary values (0 or 1).
    This is crucial for the target variable in binary classification tasks.
    """
    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Get unique values from 'is_fraud' column.
    unique_values = set(df["is_fraud"].unique())

    # Assert that the unique values are a subset of {0, 1}.
    assert unique_values.issubset({0, 1})