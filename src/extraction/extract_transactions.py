import os
import sys
from datetime import datetime, timedelta

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


# Define constants for the paths where raw and sample data will be saved.
RAW_DATA_PATH = "data/raw/transactions_raw.csv"
SAMPLE_DATA_PATH = "data/sample/sample_transactions.csv"


def generate_transaction_data(num_transactions: int = 50000, seed: int = 42) -> pd.DataFrame:
    """
    Generates a simulated and realistic dataset of financial transactions.

    The goal is to create patterns that appear plausible in a fraud scenario:
    - Very high transactions relative to the customer's average.
    - International transactions.
    - Transactions in higher-risk countries.
    - Transactions made during early morning hours.
    - Use of digital channels and mobile devices.

    Args:
        num_transactions (int): The number of transactions to generate.
        seed (int): Seed for random number generation to ensure reproducibility.

    Returns:
        pd.DataFrame: A DataFrame containing the simulated transaction data.
    """

    # Set the random seed for NumPy to ensure consistent results across runs.
    np.random.seed(seed)

    logger.info("Starting simulated dataset generation.")
    logger.info("Requested number of transactions: %s", num_transactions)

    # Define possible values for categorical features.
    transaction_types = [
        "purchase",
        "transfer",
        "withdrawal",
        "payment",
        "pix",
        "chargeback",
    ]

    merchant_categories = [
        "electronics",
        "fashion",
        "groceries",
        "travel",
        "gaming",
        "crypto",
        "restaurants",
        "pharmacy",
        "services",
        "marketplace",
    ]

    channels = [
        "mobile_app",
        "web",
        "atm",
        "pos",
        "api",
    ]

    device_types = [
        "android",
        "ios",
        "desktop",
        "atm_terminal",
        "pos_terminal",
        "unknown",
    ]

    # List of cities and their corresponding countries.
    cities_countries = [
        ("São Paulo", "Brazil"),
        ("Rio de Janeiro", "Brazil"),
        ("Fortaleza", "Brazil"),
        ("Recife", "Brazil"),
        ("Salvador", "Brazil"),
        ("Belo Horizonte", "Brazil"),
        ("Curitiba", "Brazil"),
        ("Manaus", "Brazil"),
        ("Brasília", "Brazil"),
        ("Porto Alegre", "Brazil"),
        ("Lisbon", "Portugal"),
        ("Miami", "United States"),
        ("New York", "United States"),
        ("Buenos Aires", "Argentina"),
        ("Santiago", "Chile"),
        ("Bogotá", "Colombia"),
        ("Mexico City", "Mexico"),
        ("Lagos", "Nigeria"),
        ("Moscow", "Russia"),
        ("Bangkok", "Thailand"),
    ]

    # Set of countries considered high-risk for fraud.
    high_risk_countries = {
        "Nigeria",
        "Russia",
        "Thailand",
        "Colombia",
        "Mexico",
    }

    # Define the start date for transactions (180 days ago from now).
    start_date = datetime.now() - timedelta(days=180)

    # Generate random customer IDs.
    customer_ids = np.random.randint(10000, 16000, size=num_transactions)

    # Generate random transaction dates within the last 180 days, including hours, minutes, and seconds.
    transaction_dates = [
        start_date + timedelta(
            days=int(np.random.randint(0, 180)),
            hours=int(np.random.randint(0, 24)),
            minutes=int(np.random.randint(0, 60)),
            seconds=int(np.random.randint(0, 60)),
        )
        for _ in range(num_transactions)
    ]

    # Select transaction locations based on predefined probabilities, simulating varying traffic.
    selected_locations = np.random.choice(
        range(len(cities_countries)),
        size=num_transactions,
        p=[
            0.13,  # São Paulo
            0.10,  # Rio de Janeiro
            0.08,  # Fortaleza
            0.06,  # Recife
            0.06,  # Salvador
            0.06,  # Belo Horizonte
            0.05,  # Curitiba
            0.04,  # Manaus
            0.05,  # Brasília
            0.04,  # Porto Alegre
            0.03,  # Lisbon
            0.04,  # Miami
            0.03,  # New York
            0.04,  # Buenos Aires
            0.03,  # Santiago
            0.04,  # Bogotá
            0.04,  # Mexico City
            0.03,  # Lagos
            0.03,  # Moscow
            0.02,  # Bangkok
        ],
    )

    # Extract cities and countries from the selected locations.
    cities = [cities_countries[i][0] for i in selected_locations]
    countries = [cities_countries[i][1] for i in selected_locations]

    # Generate transaction types based on predefined probabilities.
    transaction_type_values = np.random.choice(
        transaction_types,
        size=num_transactions,
        p=[0.42, 0.18, 0.10, 0.15, 0.12, 0.03],
    )

    # Generate merchant categories based on predefined probabilities.
    merchant_category_values = np.random.choice(
        merchant_categories,
        size=num_transactions,
        p=[0.12, 0.12, 0.15, 0.08, 0.08, 0.04, 0.13, 0.10, 0.08, 0.10],
    )

    # Generate transaction channels based on predefined probabilities.
    channel_values = np.random.choice(
        channels,
        size=num_transactions,
        p=[0.48, 0.24, 0.08, 0.15, 0.05],
    )

    # Generate device types based on predefined probabilities.
    device_type_values = np.random.choice(
        device_types,
        size=num_transactions,
        p=[0.42, 0.25, 0.18, 0.05, 0.08, 0.02],
    )

    # Simulate the number of previous transactions for each customer using a Poisson distribution.
    previous_transactions_count = np.random.poisson(
        lam=35, # Average rate of previous transactions.
        size=num_transactions,
    )

    # Simulate average transaction amounts for customers using a log-normal distribution.
    average_customer_amount = np.round(
        np.random.lognormal(mean=4.8, sigma=0.65, size=num_transactions),
        2,
    )

    # Generate a multiplier to vary transaction amounts around the customer's average.
    amount_multiplier = np.random.lognormal(
        mean=0.1, # Mean of the log-normal distribution.
        sigma=0.9, # Standard deviation of the log-normal distribution.
        size=num_transactions,
    )

    # Calculate the final transaction amount.
    amount = np.round(average_customer_amount * amount_multiplier, 2)

    # Extract transaction hours from the generated dates.
    transaction_hours = [date.hour for date in transaction_dates]

    # Determine if a transaction is foreign (outside Brazil).
    is_foreign_transaction = np.array([country != "Brazil" for country in countries])
    # Determine if a transaction is in a high-risk country.
    is_high_risk_country = np.array(
        [country in high_risk_countries for country in countries]
    )

    # Determine if a transaction occurred during night hours (00:00 to 05:00).
    is_night_transaction = np.array(
        [(hour >= 0 and hour <= 5) for hour in transaction_hours]
    )

    # Calculate the ratio of the transaction amount to the customer's average amount.
    amount_above_avg_ratio = amount / average_customer_amount

    # Initialize fraud probability with a base rate.
    fraud_probability = np.full(num_transactions, 0.015)

    # Adjust fraud probability based on various factors:
    # High transaction amount relative to average.
    fraud_probability += np.where(amount_above_avg_ratio > 3, 0.08, 0)
    fraud_probability += np.where(amount_above_avg_ratio > 6, 0.14, 0)
    # Foreign transactions.
    fraud_probability += np.where(is_foreign_transaction, 0.04, 0)
    # Transactions in high-risk countries.
    fraud_probability += np.where(is_high_risk_country, 0.10, 0)
    # Nighttime transactions.
    fraud_probability += np.where(is_night_transaction, 0.04, 0)
    # Transactions via API channel.
    fraud_probability += np.where(channel_values == "api", 0.04, 0)
    # Transactions from unknown device types.
    fraud_probability += np.where(device_type_values == "unknown", 0.08, 0)
    # Transactions in cryptocurrency merchant category.
    fraud_probability += np.where(merchant_category_values == "crypto", 0.08, 0)
    # Chargeback transaction type.
    fraud_probability += np.where(transaction_type_values == "chargeback", 0.08, 0)

    # Clip fraud probability to be within a reasonable range (0 to 0.85).
    fraud_probability = np.clip(fraud_probability, 0, 0.85)

    # Assign 'is_fraud' (1 or 0) based on the calculated fraud probability using a binomial distribution.
    is_fraud = np.random.binomial(1, fraud_probability)

    # Create a Pandas DataFrame from the generated data.
    df = pd.DataFrame(
        {
            "transaction_id": [f"TXN{str(i).zfill(8)}" for i in range(1, num_transactions + 1)],
            "customer_id": [f"CUST{customer_id}" for customer_id in customer_ids],
            "transaction_date": transaction_dates,
            "transaction_hour": transaction_hours,
            "amount": amount,
            "transaction_type": transaction_type_values,
            "merchant_category": merchant_category_values,
            "channel": channel_values,
            "device_type": device_type_values,
            "city": cities,
            "country": countries,
            "previous_transactions_count": previous_transactions_count,
            "average_customer_amount": average_customer_amount,
            "is_foreign_transaction": is_foreign_transaction.astype(int), # Convert boolean to integer (0 or 1).
            "is_high_risk_country": is_high_risk_country.astype(int),     # Convert boolean to integer (0 or 1).
            "is_fraud": is_fraud,
        }
    )

    # Introduce some null values in a controlled manner to demonstrate handling
    # in the transformation step.
    null_sample_size = int(num_transactions * 0.01) # 1% of transactions will have nulls.

    null_columns = [
        "merchant_category",
        "channel",
        "device_type",
        "city",
    ]

    # For each specified column, randomly select indices and set values to NaN.
    for column in null_columns:
        null_indices = np.random.choice(df.index, size=null_sample_size, replace=False)
        df.loc[null_indices, column] = np.nan

    logger.info("Dataset generated successfully.")
    logger.info("Total records: %s", len(df))
    logger.info("Total simulated frauds: %s", int(df["is_fraud"].sum()))
    logger.info(
        "Percentage of frauds: %.2f%%",
        df["is_fraud"].mean() * 100,
    )

    return df


def save_dataset(df: pd.DataFrame) -> None:
    """
    Saves the generated dataset to 'raw' and 'sample' layers.

    Args:
        df (pd.DataFrame): The DataFrame to be saved.
    """

    # Ensure the 'data/raw' and 'data/sample' directories exist.
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/sample", exist_ok=True)

    # Save the full DataFrame to the raw data path.
    df.to_csv(RAW_DATA_PATH, index=False, encoding="utf-8")

    # Create a sample DataFrame (1000 random rows) and save it.
    sample_df = df.sample(n=1000, random_state=42)
    sample_df.to_csv(SAMPLE_DATA_PATH, index=False, encoding="utf-8")

    logger.info("Raw file saved to: %s", RAW_DATA_PATH)
    logger.info("Sample file saved to: %s", SAMPLE_DATA_PATH)


def main() -> None:
    """
    Executes the extraction/simulation pipeline.
    """

    logger.info("Executing extraction pipeline.")

    # Generate transaction data with 50,000 transactions.
    df = generate_transaction_data(num_transactions=50000)
    # Save the generated dataset.
    save_dataset(df)

    logger.info("Extraction pipeline finished successfully.")


if __name__ == "__main__":
    # This block ensures that 'main()' is called only when the script is executed directly,
    # not when it's imported as a module.
    main()