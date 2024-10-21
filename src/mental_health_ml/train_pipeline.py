from src.mental_health_ml.data_ingest import ingest_data
from src.mental_health_ml.data_preprocess import preprocess_data
import mlflow


def train_pipeline(ingest_data, preprocess_data):
    with mlflow.start_run():
        sample_df = ingest_data()
        (X_train, X_test, y_train, y_test) = preprocess_data(sample_df)
        mlflow.log_param("data_version", sample_df.iloc[1, 1])
        return X_train, X_test, y_train, y_test
    # model = model_train(x_train, x_test, y_train, y_test)
    # mse, rmse = evaluation(model, x_test, y_test)


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = train_pipeline(ingest_data, preprocess_data)
    print(X_train, X_test, y_train, y_test)
