from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import json
import pandas as pd


def teach_model(json):
    # read json into dataframe
    df = pd.DataFrame(json)

    # convert text data into numerical format
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(data['input'])

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, data['output'], test_size=0.2, random_state=42)

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Compute the mean squared error
    mse = mean_squared_error(y_test, y_pred)


def predict_response(prompt):
    prompt_vector = vectorizer.transform([prompt])
    response = model.predict(prompt_vector)
    return response[0]