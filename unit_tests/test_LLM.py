import unittest
import numpy as np
from src.utils.LLM import TextRegressor

class TestTextRegressor(unittest.TestCase):
    def setUp(self):
        # Initialize TextRegressor with a small number of features for testing
        self.text_regressor = TextRegressor(max_features=10)
        self.data_json = {
            'input': ['This is a test.', 'Another test.', 'Yet another test.'],
            'output': [1.0, 2.0, 3.0]
        }

    def test_initialization(self):
        # Test whether the model initializes correctly
        self.assertIsInstance(self.text_regressor.model, tf.keras.Sequential)
        self.assertEqual(len(self.text_regressor.model.layers), 3)

    def test_train(self):
        # Test if the training method works and updates the mse
        mse = self.text_regressor.train(self.data_json)
        self.assertIsNotNone(self.text_regressor.mse)
        self.assertIsInstance(mse, float)

    def test_predict(self):
        # Test the predict method on a simple input
        self.text_regressor.train(self.data_json)
        prediction = self.text_regressor.predict('Testing predict method.')
        self.assertIsInstance(prediction, np.float32)

    def test_predict_without_training(self):
        # Ensuring that predict method raises an error when called without training
        with self.assertRaises(ValueError):
            self.text_regressor.predict('Should raise an error.')

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
