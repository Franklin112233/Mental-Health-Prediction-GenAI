import logging
from pathlib import Path

import pandas as pd
import yaml

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PROJ_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJ_ROOT / "data"
REPORTS_DIR = PROJ_ROOT / "reports"


with Path(f"{Path(__file__).resolve().parent}/config.yml").open() as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError:
        logger.exception()


def create_sample_data(
    data_file: pd.DataFrame = config["raw_data_file"],
    fraction: float = config["sample_fraction"],
    random_state: int = config["random_state"],
) -> tuple:
    return (
        pd.read_csv(Path(DATA_DIR, data_file))
        .sample(frac=fraction, random_state=random_state)
        .reset_index(drop=True)
        .rename(
            columns={
                "Unnamed: 0": "index",
                "Name": "name",
                "Age": "age",
                "Marital Status": "marital_status",
                "Education Level": "education_level",
                "Number of Children": "num_of_children",
                "Smoking Status": "smoking_status",
                "Physical Activity Level": "physical_activity_level",
                "Employment Status": "employment_status",
                "Income": "income",
                "Alcohol Consumption": "alcohol_consumption",
                "Dietary Habits": "dietary_habits",
                "Sleeping Patterns": "sleeping_patterns",
                "History of Mental Illness": "history_of_mental_illness",
                "History of Substance Abuse": "history_of_substance_abuse",
                "Family History of Depression": "family_history_of_depression",
                "Chronic Medical Conditions": "chronic_medical_conditions",
            }
        )
        .to_csv(Path(DATA_DIR, "depression_data_sample.csv", index=False)),
        logger.info(f"Sample data created with fraction {fraction}"),
        logger.info(f"Sample data saved: {DATA_DIR}/depression_data_sample.csv"),
    )


def create_data_profile(data_file: pd.DataFrame = config["sample_data_file"]) -> None:
    from ydata_profiling import ProfileReport

    df_to_profile = pd.read_csv(Path(DATA_DIR, data_file), index_col=0)
    data_profile = ProfileReport(
        df_to_profile, title="Data Profiling Report", explorative=True
    )
    data_profile.to_file(Path(REPORTS_DIR, "depression_data_profile.html"))
    logger.info(
        f"Data profile created and saved: {REPORTS_DIR}/depression_data_profile.html"
    )


if __name__ == "__main__":
    create_sample_data()
    create_data_profile()
