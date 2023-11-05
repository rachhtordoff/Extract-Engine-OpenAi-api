import unittest
from unittest.mock import patch
from src.utils.Extractions import DataBankStatementExtractor, WebScrapedDataExtractor
from src import app


class TestDataBankStatementExtractor(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()

    @patch('src.utils.Extractions.PDFExtractor.extract_text')
    @patch('src.utils.Extractions.DataExtractor.extract_from_bank_statement')
    def test_extract_and_format(self, mock_extract_from_bank_statement, mock_extract_text):
        mock_extract_text.return_value = "extracted_text"
        mock_extract_from_bank_statement.return_value = "formatted_data"

        extractor = DataBankStatementExtractor('dummy_path')
        result = extractor.extract_and_format()

        mock_extract_text.assert_called_once_with('dummy_path')
        mock_extract_from_bank_statement.assert_called_once_with('extracted_text')
        self.assertEqual(result, 'formatted_data')

if __name__ == '__main__':
    unittest.main()
