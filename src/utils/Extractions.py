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
    def __init__(self, website_urls, phrases_list):
        self.website_urls = website_urls
        self.phrases_list = phrases_list

    def extract_and_format_textblock(self):
        output = {}
        for key, value in self.data.items():
            chunks = DataExtractor().chunk_data(value)
            counter = 1
            for chunk in chunks:
                generate_template = DataExtractor().custom_template_data_extract(chunk, self.phrases_list)

                if key in output:
                    for template_key, template_value in generate_template.items():
                        if template_key in output[key].get(f"result_{counter}", {}):
                            output[key][f"result_{counter}"][template_key] += template_value
                        else:
                            if f"result_{counter}" in output[key]:
                                output[key][f"result_{counter}"].update({template_key: template_value})
                            else:
                                output[key][f"result_{counter}"] = {template_key: template_value}
                else:
                    output[key] = {f"result_{counter}": generate_template}
                counter += 1
        return output
