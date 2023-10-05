import unittest
from src.utils.LLM import TextRegressor
import numpy as np


class TestTextRegressor(unittest.TestCase):
    def setUp(self):
        self.regressor = TextRegressor(max_features=1000)

        # Dummy data
        self.data = {
            'input': ['The cat in the hat', 'A quick brown fox', 'Jump over the lazy dog'],
            'output': [1, 2, 3]
        }

        self.single_prompt = 'The cat in the hat'

    def test_train(self):
        mse = self.regressor.train(self.data)
        self.assertIsNotNone(mse)
        self.assertIsInstance(mse, float)

    def test_predict(self):
        self.regressor.train(self.data)

        prediction = self.regressor.predict(self.single_prompt)
        self.assertIsNotNone(prediction)
        self.assertIsInstance(prediction, np.float64)


if __name__ == '__main__':
    unittest.main()
