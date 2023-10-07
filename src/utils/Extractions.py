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

    def extract_and_format_textblock(self):
        output = {}
        MAX_CHUNK_SIZE = 2500  # Set the chunk size
        for key, value in self.scraped_websites.items():
            print(len(value))

            chunks = DataExtractor().chunk_data(value)
           
            for i, chunk in enumerate(chunks):
                generate_template = DataExtractor().custom_template_data_extract(chunk, self.phrases_list)
                
                # Append or merge the extracted data in output
                if key in output:
                    output[key].update({f"chunk_{i}": generate_template})
                else:
                    output[key] = {f"chunk_{i}": generate_template}
        return output

    def extract_and_format_pdf(self):
        output = {}
        MAX_CHUNK_SIZE = 2500  # Set the chunk size
        for key, value in self.scraped_websites.items():
            print(len(value))

            summarized_data = DataExtractor().reduce_summarize_pdf_data(value)

            chunks = []
            
            # If value is too large, split it into chunks
            if len(summarized_data) > MAX_CHUNK_SIZE:
                while len(summarized_data) > MAX_CHUNK_SIZE:
                    # Find the last full word within the MAX_CHUNK_SIZE
                    idx = summarized_data.rfind(' ', 0, MAX_CHUNK_SIZE)
                    
                    # If unable to find a splitting point, force a split at MAX_CHUNK_SIZE
                    idx = idx if idx != -1 else MAX_CHUNK_SIZE
                    
                    chunks.append(summarized_data[:idx])
                    summarized_data = summarized_data[idx:]
            else:
                chunks.append(summarized_data)
            
            for i, chunk in enumerate(chunks):
                generate_template = DataExtractor().custom_template_data_extract(chunk, self.phrases_list)
                
                # Append or merge the extracted data in output
                if key in output:
                    output[key].update({f"chunk_{i}": generate_template})
                else:
                    output[key] = {f"chunk_{i}": generate_template}
        
        return output
