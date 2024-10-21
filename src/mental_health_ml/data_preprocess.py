import logging
from abc import ABC, abstractmethod
from typing import Annotated

import pandas as pd
from sklearn.model_selection import train_test_split

from src.mental_health_ml.utils import config


class DataStrategy(ABC):
    @abstractmethod
    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame | pd.Series:
        pass


class DataProcessStrategy(DataStrategy):
    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            return data.drop(
                [
                    "name",
                ],
                axis=1,
            )
        except Exception:
            logging.exception("An error occurred during data processing")
            raise


class DataSplitStrategy(DataStrategy):
    def handle_data(self, data: pd.DataFrame) -> tuple[pd.DataFrame | pd.Series]:
        try:
            X = data.drop("history_of_mental_illness", axis=1)
            y = data["history_of_mental_illness"]
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=config["test_size"],
                random_state=config["random_state"],
            )
            return (X_train, X_test, y_train, y_test)
        except Exception:
            logging.exception("An error occurred during data processing")
            raise


class DataPreprocessor:
    def __init__(self, data: pd.DataFrame, strategy: DataStrategy) -> None:
        self.df = data
        self.strategy = strategy

    def handle_data(self) -> pd.DataFrame | pd.Series:
        return self.strategy.handle_data(self.df)


def preprocess_data(
    data: pd.DataFrame,
) -> tuple[
    Annotated[pd.DataFrame, "x_train"],
    Annotated[pd.DataFrame, "x_test"],
    Annotated[pd.Series, "y_train"],
    Annotated[pd.Series, "y_test"],
]:
    try:
        preprocess_strategy = DataProcessStrategy()
        data_processor = DataPreprocessor(data, preprocess_strategy)
        processed_data = data_processor.handle_data()

        split_strategy = DataSplitStrategy()
        data_cleaning = DataPreprocessor(processed_data, split_strategy)
        (x_train, x_test, y_train, y_test) = data_cleaning.handle_data()
        return (x_train, x_test, y_train, y_test)
    except Exception:
        logging.exception("An error occurred during data processing")
        raise
