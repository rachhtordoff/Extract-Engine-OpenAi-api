from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.document_loaders import WebBaseLoader, PyPDFLoader
from langchain.chains import create_extraction_chain
from src.config import Config
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils.aws_s3 import AWSService
import openai
import json
import os

os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY

class DataExtractor:
    def __init__(self, api_key=Config.OPENAI_API_KEY):
        self.llm = ChatOpenAI(temperature=1,
                        model="gpt-3.5-turbo",
                        openai_api_key=api_key,
                        max_tokens=3000)

    def extract_from_bank_statement(self, data):
        schema = {
            "properties": {
                "name": {"type": "string"},
                "address": {"type": "string"},
                "opening_balance": {"type": "integer"},
                "closing_balance": {"type": "integer"},
                "income/salary_total": {"type": "integer"},
                "Outgoings/Expenses_total": {"type": "integer"}
            }
        }
        chain = create_extraction_chain(schema, self.llm)
        output = chain.run(data)
        return output

    def get_query_from_url(self, urls, phrases):

        output = []

        for url in urls:
            loader = WebBaseLoader(url)
            data = loader.load()

            index = VectorstoreIndexCreator().from_loaders([loader])

            prompt = f"Extract relevant information about the following phrases {', '.join(phrases)}"

            output.append({url: index.query(prompt)})
    
        return output

    def get_query_from_pdfs(self, file_details, phrases):

        output = []

        for detail in file_details:
            AWSService().download_file(detail['folder_id'], detail['doc_name'])

            loader = PyPDFLoader(f'/opt/src/documents/{detail["doc_name"]}')
            data = loader.load()

            index = VectorstoreIndexCreator().from_loaders([loader])

            prompt = f"Extract relevant information about the following phrases {', '.join(phrases)}"

            output.append({detail["doc_name"]: index.query(prompt)})
        
            if os.path.exists(f"/opt/src/documents/{detail['doc_name']}"):
                os.remove(f"/opt/src/documents/{detail['doc_name']}")

        return output


    def summerize_data_extract(self, output):

        get_max_tokens = 3000 - len(output)
        llm = ChatOpenAI(temperature=1,
                        model="gpt-3.5-turbo",
                        openai_api_key=Config.OPENAI_API_KEY,
                        max_tokens=get_max_tokens)

        prompt = f"""Given the json output: '{output}'
        
        sumarise the outputs and return
        in a structured format like JSON
        """
        openai.api_key = Config.OPENAI_API_KEY
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.2,
            max_tokens=get_max_tokens,
            n=1,
            stop=None
        )
        output_text = response.choices[0].text.strip()
        return json.loads(output_text)

    def custom_template_data_extract(self, web_scraped_text, phrases):

        get_max_tokens = 4097 - len(web_scraped_text)
        llm = ChatOpenAI(temperature=1,
                        model="gpt-3.5-turbo",
                        openai_api_key=Config.OPENAI_API_KEY,
                        max_tokens=get_max_tokens)

        prompt = f"""Given the text: '{web_scraped_text}'
        
        extract relevant information about the following phrases {', '.join(phrases)} 
        in a structured format like JSON
        """
        openai.api_key = Config.OPENAI_API_KEY
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.2,
            max_tokens=get_max_tokens,
            n=1,
            stop=None
        )

        output_text = {}
        choices = response.choices
        if choices != []:
            output_text = choices[0].text.strip()

        return json.loads(output_text)

    def reduce_summarize_pdf_data(self, data):
        chain = load_summarize_chain(self.llm, chain_type='map_reduce')
        output = chain.run(data)
        return output        

    def chunk_data(self, data):
        c_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=1)
        return c_splitter.split_text(data)


class TemplateFormatter:
    def format_from_json(self, json_data):
        created_template = '''
        Please extract the fol
        '''
        if json_data.get('selectedCuisine') != 'Pot Luck':
            created_template += ' Focus on a {selectedCuisine} inspired meal.'
        if json_data.get('selectedCalorie') == 'Yes':
            created_template += ' Please include a calorie breakdown'
        if json_data.get('selectedDietry'):
            created_template += ' Please make sure the recipe is {dietaryString}'
        prompted_template = ChatPromptTemplate.from_template(created_template)
        if json_data.get('selectedDietry'):
            dietaryString = ', '.join(json_data.get('selectedDietry'))
            filled_template = prompted_template.format_messages(
                selectedNo=json_data.get('selectedNo'),
                selectedCuisine=json_data.get('selectedCuisine'),
                dietaryString=dietaryString
            )
        else:
            filled_template = prompted_template.format_messages(
                selectedNo=json_data.get('selectedNo'),
                selectedCuisine=json_data.get('selectedCuisine'),
            )
        return filled_template

    def format_second_template(self, json_data):
        created_template = '''
        Make sure this recipe is in the following format
        ingredients will expire soon and are in the recipe have been specified
        ingredients are in the pantry (other items) and are in the recipe have been specified
        any ingredients in the recipe that are not owned yet are displayed in a shopping list.
        full cooking instructions have been supplied
        '''
        if json_data.get('selectedCalorie') == 'Yes':
            created_template += ' A full calorie breakdown has been included'
        prompted_template = ChatPromptTemplate.from_template(created_template)
        return prompted_template


class ChatResponder:
    def __init__(self, temperature=0.0):
        self.chat = OpenAI(temperature=temperature)

    def get_response(self, prompt, prompt2):
        chain1 = LLMChain(llm=self.chat, prompt=prompt)
        chain2 = LLMChain(llm=self.chat, prompt=prompt2)
        simple_sequential_chain = SimpleSequentialChain(chains=(chain1, chain2), verbose=True)
        simple_sequential_chain.run('can you give me a recipe')
