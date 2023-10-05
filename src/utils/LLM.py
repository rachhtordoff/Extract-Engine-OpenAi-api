from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd


class TextRegressor:
    def __init__(self, max_features=5000):
        self.vectorizer = TfidfVectorizer(max_features=max_features)
        self.model = LinearRegression()
        self.mse = None

    def train(self, data_json):
        """
        Train the model with data from a JSON.

        :param data_json: dict, contains 'input' and 'output' keys with text and target data
        """
        df = pd.DataFrame(data_json)
        X = self.vectorizer.fit_transform(df['input'])
        X_train, X_test, y_train, y_test = train_test_split(X, df['output'], test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        self.mse = mean_squared_error(y_test, y_pred)

        return self.mse

    def predict(self, prompt):
        """
        Predict a response based on a text prompt.

        :param prompt: str, the text input for prediction
        :return: The model's prediction
        """
        prompt_vector = self.vectorizer.transform([prompt])
        response = self.model.predict(prompt_vector)
        return response[0]
