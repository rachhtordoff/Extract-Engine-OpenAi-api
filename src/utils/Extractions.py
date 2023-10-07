import PyPDF2
from src.utils.open_api import DataExtractor


class PDFExtractor:
    @staticmethod
    def extract_text(pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text


class DataBankStatementExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_and_format(self):
        extracted_text = PDFExtractor().extract_text(self.pdf_path)
        generate_template = DataExtractor().extract_from_bank_statement(extracted_text)
        return generate_template


class WebScrapedDataExtractor:
    def __init__(self, scraped_websites, phrases_list):
        self.scraped_websites = scraped_websites
        self.phrases_list = phrases_list

    def extract_and_format(self):
        output = {}
        for key, value in self.scraped_websites.items():
            generate_template = DataExtractor().custom_template_data_extract(value, self.phrases_list)
            output.update({key: generate_template})
        return output
