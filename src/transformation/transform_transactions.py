import os
import sys

import numpy as np
import pandas as pd


# This line is crucial for enabling the script to import modules from the 'src' directory
# when it's executed directly. It adds the project's root directory to the Python path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import the custom logger from the utils module. 'noqa: E402' silences a linter
# warning about imports not being at the top of the file, which is necessary here
# due to the sys.path modification.
from src.utils.logger import get_logger  # noqa: E402


# Initialize the logger for this module.
logger = get_logger(__name__)


# Define constants for the paths where raw and processed data are stored.
RAW_DATA_PATH = "data/raw/transactions_raw.csv"
PROCESSED_DATA_PATH = "data/processed/transactions_processed.csv"


def load_raw_data(file_path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Loads raw data from the raw data layer.

    Args:
        file_path (str): The path to the raw data CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the raw transaction data.

    Raises:
        FileNotFoundError: If the specified raw data file does not exist.
    """

    logger.info("Loading raw data from: %s", file_path)

    # Check if the file exists before attempting to load it.
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw file not found: {file_path}")

    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(file_path)

    logger.info("Raw data loaded successfully.")
    logger.info("Total records loaded: %s", len(df))

    return df


def standardize_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes textual columns:
    - Removes extra spaces
    - Converts to lowercase
    - Replaces spaces with underscores in categorical fields
    """

    logger.info("Standardizing textual columns.")

    # Columns that might contain leading/trailing spaces.
    text_columns = [
        "transaction_id",
        "customer_id",
        "transaction_type",
        "merchant_category",
        "channel",
        "device_type",
        "city",
        "country",
    ]

    # Apply strip for all potential text columns.
    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    # Categorical columns that should be standardized to lowercase and use underscores.
    categorical_columns = [
        "transaction_type",
        "merchant_category",
        "channel",
        "device_type",
        "city",
        "country",
    ]

    # Apply lowercase and replace spaces/hyphens with underscores.
    for column in categorical_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .str.lower()
                .str.replace(" ", "_", regex=False)
                .str.replace("-", "_", regex=False)
            )

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing values in a simple and controlled manner.
    Categorical columns are filled with 'unknown'.
    Numeric columns are filled with their median.
    Binary columns are filled with 0.
    """

    logger.info("Handling missing values.")

    # Log the count of missing values before treatment.
    missing_before = df.isna().sum()
    logger.info("Missing values before treatment:\n%s", missing_before[missing_before > 0])

    # Dictionary defining fill values for specific categorical columns.
    fill_values = {
        "merchant_category": "unknown",
        "channel": "unknown",
        "device_type": "unknown",
        "city": "unknown",
        "country": "unknown",
        "transaction_type": "unknown",
    }

    # Apply fillna for specified categorical columns.
    for column, value in fill_values.items():
        if column in df.columns:
            df[column] = df[column].fillna(value)

    # Columns identified as numeric.
    numeric_columns = [
        "amount",
        "previous_transactions_count",
        "average_customer_amount",
        "transaction_hour",
    ]

    # Fill missing numeric values with the column's median.
    for column in numeric_columns:
        if column in df.columns:
            df[column] = df[column].fillna(df[column].median())

    # Columns identified as binary flags.
    binary_columns = [
        "is_foreign_transaction",
        "is_high_risk_country",
        "is_fraud",
    ]

    # Fill missing binary values with 0.
    for column in binary_columns:
        if column in df.columns:
            df[column] = df[column].fillna(0)

    # Log the count of missing values after treatment to verify.
    missing_after = df.isna().sum()
    logger.info("Missing values after treatment:\n%s", missing_after[missing_after > 0])

    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts column data types to appropriate formats.
    """

    logger.info("Converting data types.")

    # Convert 'transaction_date' to datetime objects, coercing errors to NaT (Not a Time).
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    # Columns expected to be integers.
    integer_columns = [
        "transaction_hour",
        "previous_transactions_count",
        "is_foreign_transaction",
        "is_high_risk_country",
        "is_fraud",
    ]

    # Convert to numeric, fill NaNs with 0, then convert to integer.
    for column in integer_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(int)

    # Columns expected to be floats.
    float_columns = [
        "amount",
        "average_customer_amount",
    ]

    # Convert to numeric, fill NaNs with 0, then convert to float.
    for column in float_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(float)

    return df


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates analytical features and features useful for Machine Learning.
    """

    logger.info("Creating features.")

    # Extract date components from 'transaction_date'.
    df["transaction_date_only"] = df["transaction_date"].dt.date # Date only (YYYY-MM-DD)
    df["transaction_year"] = df["transaction_date"].dt.year
    df["transaction_month"] = df["transaction_date"].dt.month
    df["transaction_day"] = df["transaction_date"].dt.day
    df["transaction_day_of_week"] = df["transaction_date"].dt.dayofweek # Monday=0, Sunday=6
    df["transaction_day_name"] = df["transaction_date"].dt.day_name() # e.g., 'Monday'
    # Create a binary flag for weekend transactions.
    df["is_weekend"] = df["transaction_day_of_week"].isin([5, 6]).astype(int)

    # Create binary flags for night transactions (00:00-05:00) and business hours (09:00-18:00).
    df["is_night_transaction"] = df["transaction_hour"].between(0, 5).astype(int)
    df["is_business_hours"] = df["transaction_hour"].between(9, 18).astype(int)

    # Calculate the ratio of transaction amount to the customer's average amount.
    # Handle division by zero by replacing 0 with NaN to avoid errors, then fill NaNs.
    df["amount_above_customer_avg"] = (
        df["amount"] / df["average_customer_amount"].replace(0, np.nan)
    )

    # Replace infinite values resulting from division by zero (or near zero) with NaN, then fill NaNs with 0.
    df["amount_above_customer_avg"] = (
        df["amount_above_customer_avg"]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
        .round(2)
    )

    # Calculate the difference between transaction amount and customer's average amount.
    df["amount_difference_from_avg"] = (
        df["amount"] - df["average_customer_amount"]
    ).round(2)

    # Categorize 'amount_above_customer_avg' into risk levels using bins.
    df["amount_risk_level"] = pd.cut(
        df["amount_above_customer_avg"],
        bins=[-np.inf, 1, 2, 4, np.inf],
        labels=["normal", "attention", "high", "critical"],
    ).astype(str)

    # Categorize 'amount' into transaction amount categories.
    df["transaction_amount_category"] = pd.cut(
        df["amount"],
        bins=[-np.inf, 50, 200, 1000, 5000, np.inf],
        labels=["very_low", "low", "medium", "high", "very_high"],
    ).astype(str)

    # Categorize customer activity level based on previous transaction count.
    df["customer_activity_level"] = pd.cut(
        df["previous_transactions_count"],
        bins=[-np.inf, 5, 20, 50, 100, np.inf],
        labels=["new_customer", "low_activity", "medium_activity", "high_activity", "very_high_activity"],
    ).astype(str)

    # Initialize a rule-based risk score.
    df["rule_based_risk_score"] = 0

    # Increase risk score based on various criteria, simulating business rules for fraud detection.
    df["rule_based_risk_score"] += np.where(df["amount_above_customer_avg"] > 2, 15, 0) # High amount relative to average
    df["rule_based_risk_score"] += np.where(df["amount_above_customer_avg"] > 4, 20, 0)
    df["rule_based_risk_score"] += np.where(df["amount_above_customer_avg"] > 6, 25, 0)
    df["rule_based_risk_score"] += np.where(df["is_foreign_transaction"] == 1, 15, 0) # Foreign transaction
    df["rule_based_risk_score"] += np.where(df["is_high_risk_country"] == 1, 25, 0)    # High-risk country
    df["rule_based_risk_score"] += np.where(df["is_night_transaction"] == 1, 10, 0)    # Night transaction
    df["rule_based_risk_score"] += np.where(df["channel"] == "api", 10, 0)             # API channel
    df["rule_based_risk_score"] += np.where(df["device_type"] == "unknown", 15, 0)     # Unknown device type
    df["rule_based_risk_score"] += np.where(df["merchant_category"] == "crypto", 15, 0) # Crypto merchant
    df["rule_based_risk_score"] += np.where(df["transaction_type"] == "chargeback", 15, 0) # Chargeback transaction

    # Clip the risk score to a maximum of 100.
    df["rule_based_risk_score"] = df["rule_based_risk_score"].clip(0, 100)

    # Categorize the rule-based risk score into descriptive risk levels.
    df["risk_level"] = pd.cut(
        df["rule_based_risk_score"],
        bins=[-1, 25, 50, 75, 100], # Bins for categorization. -1 includes 0 score.
        labels=["low", "medium", "high", "critical"], # Labels for each bin.
    ).astype(str)

    return df


def validate_processed_data(df: pd.DataFrame) -> None:
    """
    Validates minimum data quality rules for the processed data.

    Args:
        df (pd.DataFrame): The DataFrame with processed transaction data.

    Raises:
        ValueError: If any validation rule fails.
    """

    logger.info("Validating processed data.")

    # List of expected columns after transformation.
    required_columns = [
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
        "amount_above_customer_avg",
        "is_night_transaction",
        "is_weekend",
        "rule_based_risk_score",
        "risk_level",
    ]

    # Check for missing required columns.
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Required columns are missing: {missing_columns}")

    # Check for duplicate transaction IDs.
    if df["transaction_id"].duplicated().any():
        raise ValueError("Duplicate transaction_id found.")

    # Check for negative transaction amounts.
    if df["amount"].lt(0).any():
        raise ValueError("Transactions with negative amount found.")

    # Check if 'is_fraud' column contains only binary values (0 or 1).
    if not set(df["is_fraud"].unique()).issubset({0, 1}):
        raise ValueError("The 'is_fraud' column must contain only 0 or 1.")

    # Check for invalid dates in 'transaction_date'.
    if df["transaction_date"].isna().any():
        raise ValueError("Invalid dates found in 'transaction_date'.")

    logger.info("Validation completed successfully.")


def save_processed_data(df: pd.DataFrame, file_path: str = PROCESSED_DATA_PATH) -> None:
    """
    Saves the processed data to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame with processed transaction data.
        file_path (str): The path where the processed CSV file will be saved.
    """

    logger.info("Saving processed data to: %s", file_path)

    # Ensure the 'data/processed' directory exists.
    os.makedirs("data/processed", exist_ok=True)

    # Save the DataFrame to CSV.
    df.to_csv(file_path, index=False, encoding="utf-8")

    logger.info("Processed data saved successfully.")
    logger.info("Total processed records: %s", len(df))
    logger.info("Total processed columns: %s", len(df.columns))


def transform_transactions() -> pd.DataFrame:
    """
    Executes the complete transformation pipeline.
    This function orchestrates the loading, cleaning, feature engineering, validation, and saving of data.
    """

    logger.info("Starting transformation pipeline.")

    # Step 1: Load raw data.
    df = load_raw_data()
    # Step 2: Standardize text columns.
    df = standardize_text_columns(df)
    # Step 3: Handle missing values.
    df = handle_missing_values(df)
    # Step 4: Convert data types.
    df = convert_data_types(df)
    # Step 5: Create new features.
    df = create_features(df)

    # Step 6: Validate the transformed data.
    validate_processed_data(df)
    # Step 7: Save the processed data.
    save_processed_data(df)

    logger.info("Transformation pipeline finished successfully.")

    return df


def main() -> None:
    """
    Main function to run the transformation pipeline when the script is executed.
    """
    transform_transactions()


if __name__ == "__main__":
    # This block ensures that 'main()' is called only when the script is executed directly,
    # not when it's imported as a module.
    main()