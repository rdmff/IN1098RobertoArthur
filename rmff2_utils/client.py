import flwr as fl
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Carrega dataset
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Modelo local
model = LogisticRegression(max_iter=200)

class FlowerClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return [p for p in model.coef_.ravel()] + [model.intercept_[0]]

    def set_parameters(self, parameters):
        # Reconstrói os parâmetros no formato do sklearn
        num_features = X_train.shape[1]
        model.coef_ = np.array(parameters[:-1]).reshape(1, num_features)
        model.intercept_ = np.array([parameters[-1]])

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        model.fit(X_train, y_train)
        return self.get_parameters({}), len(X_train), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        preds = model.predict(X_test)
        accuracy = accuracy_score(y_test, preds)
        return float(0.0), len(X_test), {"accuracy": accuracy}

if __name__ == "__main__":
    fl.client.start_numpy_client(server_address="localhost:8080", client=FlowerClient())
