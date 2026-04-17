import os
import pandas as pd
import sys
import json
from datetime import datetime
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import time
from config import get_db_config, get_row_limit


DEBUG = False

# Columns that don't contribute to churn prediction — dropped before training
irrelevant_columns = [
    "upload_timestamp", "upload file", "type", "warranty", "office date", "office time in",
    "defect / damage type", "responsible party", "final status", "month", "source", "carrier"
]


def safe_load_from_db(sql_query, conn, max_retries=5, wait_seconds=2):
    retries = 0
    while retries < max_retries:
        df = pd.read_sql_query(sql_query, conn)

        if not df.empty:
            print(f"Successfully loaded {len(df)} rows from database.")
            return df

        print(f"Empty dataframe pulled. Retrying in {wait_seconds} seconds...")
        time.sleep(wait_seconds)
        retries += 1

    raise ValueError("Failed to load non-empty dataframe after retries.")


def preprocess_data(input_file, output_file, mode="train"):
    print(f"Loading data from {input_file} in {mode} mode...")

    if input_file == "from_db":
        import psycopg2
        from sqlalchemy import create_engine
        DB_CONFIG = get_db_config()

        engine_str = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
        engine = create_engine(engine_str)

        LIMIT = get_row_limit()

        query = f"""
            SELECT * FROM devices
            WHERE upload_file = (
                SELECT upload_file
                FROM devices
                ORDER BY upload_timestamp DESC
                LIMIT 1
            )
            ORDER BY upload_timestamp DESC
            LIMIT {LIMIT};
        """

        df = safe_load_from_db(query, engine)
        df.drop(columns=["device_id"], inplace=True, errors="ignore")

    else:
        if input_file.endswith(".xls") or input_file.endswith(".xlsx"):
            df = pd.read_excel(input_file, engine="openpyxl")
        else:
            df = pd.read_csv(input_file)

    print(f"Raw columns BEFORE normalization or dropping:\n{df.columns.tolist()}\n")

    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_").str.replace("#", "num").str.replace("/", "_")

    print(f"Columns after loading and normalization: {df.columns.tolist()}")

    normalized_irrelevant = [col.lower().strip().replace(" ", "_").replace("#", "num").replace("/", "_") for col in irrelevant_columns]

    today = datetime.today()

    if 'active_date' in df.columns:
        df['active_date'] = pd.to_datetime(df['active_date'], errors="coerce")

        median_date = df['active_date'].median()
        if pd.isnull(median_date):
            median_date = datetime.today() - pd.Timedelta(days=365)
        df['active_date'] = df['active_date'].fillna(median_date)
        df['days_since_activation'] = (today - df['active_date']).dt.days

        # Devices active for more than 30 days are past the return window — assume not churned
        if 'churn' not in df.columns:
            df['churn'] = None
        df.loc[df['churn'].isna() & (df['days_since_activation'] > 30), 'churn'] = 0
        df['churn'] = df['churn'].astype('Int64')

    if 'sim_info' in df.columns:
        def extract_carrier(x):
            try:
                if isinstance(x, float) or x is None:
                    return None
                x = x.strip().lower()
                if x == "uninserted":
                    return None
                data = json.loads(x)
                return data[0]['carrier_name'] if data else None
            except json.JSONDecodeError:
                return None

        df['carrier'] = df['sim_info'].apply(extract_carrier)
        df['sim_info'] = df['sim_info'].apply(lambda x: 0 if str(x).strip().lower() == "uninserted" else 1)

    if {'interval_date', 'last_boot_date'}.intersection(df.columns):
        if 'interval_date' in df.columns:
            df['interval_date'] = pd.to_datetime(df['interval_date'], errors="coerce")
        if 'last_boot_date' in df.columns:
            df['last_boot_date'] = pd.to_datetime(df['last_boot_date'], errors="coerce")
        df['most_recent_use'] = df[[c for c in ['interval_date', 'last_boot_date'] if c in df.columns]].max(axis=1)

        if 'most_recent_use' in df.columns and 'active_date' in df.columns:
            df['days_since_last_use'] = (today - df['most_recent_use']).dt.days
            df['days_used_since_activation'] = (df['most_recent_use'] - df['active_date']).dt.days
            df['active_ratio'] = df['days_used_since_activation'] / df['days_since_activation'].replace(0, 1)

        df.drop(columns=['most_recent_use'], inplace=True, errors="ignore")

    if mode == "train":
        df.drop(columns=[col for col in normalized_irrelevant if col in df.columns], inplace=True)

    if 'product_model_num' in df.columns:
        df['product_model_num'] = df['product_model_num'].astype(str)
        df['product_model_encoded'] = OrdinalEncoder().fit_transform(df[['product_model_num']])
        df.drop(columns=['product_model_num'], inplace=True)

    # Shouldn't ever be needed, but ensures device number is saved.
    if "device_number" in df.columns:
        df_device_numbers = df[["device_number"]].copy()
        df.drop(columns=["device_number"], inplace=True)
        df_device_numbers.to_csv("temp_device_numbers.csv", index=False)

    # Drop churn before fitting the preprocessor, then reattach after
    if 'churn' in df.columns:
        churn_series = df['churn']
        df.drop(columns=['churn'], inplace=True)
    else:
        churn_series = None

    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    print(f"Columns going into transformers:\nNumerical: {numerical_cols}\nCategorical: {categorical_cols}\n")

    transformers = []
    if numerical_cols:
        transformers.append(('num', Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), numerical_cols))

    if categorical_cols:
        transformers.append(('cat', Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
        ]), categorical_cols))

    if transformers:
        preprocessor = ColumnTransformer(transformers)
        df_processed = preprocessor.fit_transform(df)
        df_processed = pd.DataFrame(df_processed, columns=preprocessor.get_feature_names_out())
    else:
        print("No features to transform. Skipping transformation step.")
        df_processed = pd.DataFrame()

    if mode == "train" and churn_series is not None:
        df_processed['churn'] = churn_series.values
        df_processed.dropna(subset=['churn'], inplace=True)

    print("Transformed feature names (line-by-line):")
    for col in df_processed.columns:
        print(f"  {col}")

    df_processed.to_csv(output_file, index=False)

    if DEBUG:
        print("Final Processed Columns:", df.columns.tolist())
        df.to_csv("debug_processed_data.csv", index=False)

    print(f"Data processing complete. Processed dataset saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python data_processing.py <input_file> <output_file> <mode: train/predict>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    mode = sys.argv[3].lower()
    if mode not in ["train", "predict"]:
        print("Error: Mode must be 'train' or 'predict'")
        sys.exit(1)
    preprocess_data(input_path, output_path, mode)
