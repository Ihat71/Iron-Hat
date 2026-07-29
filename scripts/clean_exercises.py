import logging
from pathlib import Path
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent

LOG_DIR = SCRIPT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "gym_exercise_dataset.csv"
PROCESSED_DATA_PATH = ROOT_DIR / "data" / "processed" / "exercises.json"

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def load() -> pd.DataFrame:
    logger.info("Loading raw dataset...")

    df = pd.read_csv(RAW_DATA_PATH)

    logger.info("Loaded %d exercises.", len(df))

    return df


def inspect_data(df: pd.DataFrame) -> None:
    logger.info("Dataset shape: %s", df.shape)

    logger.info(
        "Columns:\n%s",
        df.columns.tolist()
    )

    logger.info(
        "Missing values:\n%s",
        df.isna().sum()
    )

    string_columns = df.select_dtypes(include=str).columns

    for col in string_columns:
        logger.info(
            "\n%s value counts:\n%s",
            col,
            df[col].value_counts(dropna=False).head(20)
        )

    logger.info(
        "Checking squat rows:\n%s",
        df[df["Exercise Name"] == "Squat"]
    )


def validate_data(df: pd.DataFrame) -> None:
    required_columns = {
        "Exercise Name",
        "Equipment",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    if len(df) < 100:
        raise ValueError(
            "Dataset looks suspiciously small."
        )

    logger.info("Validation passed.")


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Standardizing column names...")

    df = df.rename(columns = {"Difficulty (1-5)":"difficulty"})

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    df = df.rename(
        columns={
            "exercise_name": "name"
        }
    )

    logger.info(
        "Standardized columns: %s",
        df.columns.tolist()
    )

    return df


def clean_rows(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning row values...")

    string_columns = df.select_dtypes(
        include=str
    ).columns

    for col in string_columns:
        df[col] = (
            df[col]
            .fillna("")
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
            .str.replace(
                r"[\u200b-\u200d]",
                "",
                regex=True
            )
        )

    # Only trim exercise names.
    # Avoid title() because it can ruin names like EZ Bar.
    df["name"] = df["name"].str.strip()

    muscle_columns = [
        col for col in df.columns
        if "_muscles" in col
    ]

    for col in muscle_columns:
        df[col] = df[col].str.rstrip(",")

    logger.info("Finished cleaning rows.")

    return df


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Checking normalization requirements...")

    # No normalization required currently.
    # Add mappings here if future datasets need them.

    logger.info("Normalization complete.")

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(
        "Skipping duplicate removal because repeated names may represent variations."
    )

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Handling missing values...")

    before = len(df)

    df = df.dropna(
        subset=["name"]
    )

    removed = before - len(df)

    logger.info(
        "Removed %d rows missing exercise names.",
        removed
    )

    return df


def export(df: pd.DataFrame) -> None:
    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_json(
        PROCESSED_DATA_PATH,
        orient="records",
        indent=2
    )

    logger.info(
        "Exported %d exercises to %s",
        len(df),
        PROCESSED_DATA_PATH
    )


def main():

    df = load()

    inspect_data(df)

    validate_data(df)

    df = standardize_columns(df)

    df = clean_rows(df)

    df = normalize(df)

    df = remove_duplicates(df)

    df = handle_missing_values(df)

    export(df)
    
    logger.info(
        "Exercise cleaning pipeline completed successfully."
    )


if __name__ == "__main__":
    main()