from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri
from zenml.pipelines import pipeline

from src.mental_health_ml.data_ingest import ingest_data
from src.mental_health_ml.data_preprocess import preprocess_data


@pipeline
def train_pipeline(ingest_data, preprocess_data):
    sample_df = ingest_data()
    (X_train, X_test, y_train, y_test) = preprocess_data(sample_df)
    # model = model_train(x_train, x_test, y_train, y_test)
    # mse, rmse = evaluation(model, x_test, y_test)


if __name__ == "__main__":
    # training = train_pipeline(
    #     ingest_data(),
    #     preprocess_data(),
    # train_model(),
    # evaluation(),
    # )
    # training.run()
    sample_df = ingest_data()
    (X_train, X_test, y_train, y_test) = preprocess_data(sample_df)
    print(y_test)
