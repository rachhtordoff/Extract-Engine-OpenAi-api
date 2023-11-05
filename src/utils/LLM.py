import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd


class TextRegressor:
    def __init__(self, max_features=5000):
        self.vectorizer = TfidfVectorizer(max_features=max_features)
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_dim=max_features),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.mse = None

    def train(self, data_json):
        df = pd.DataFrame(data_json)
        X = self.vectorizer.fit_transform(df['input']).toarray()
        y = df['output'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train, epochs=10, validation_split=0.2)

        y_pred = self.model.predict(X_test)
        self.mse = mean_squared_error(y_test, y_pred.flatten())

        return self.mse

    def predict(self, prompt):
        prompt_vector = self.vectorizer.transform([prompt]).toarray()
        response = self.model.predict(prompt_vector)
        return response[0][0]
