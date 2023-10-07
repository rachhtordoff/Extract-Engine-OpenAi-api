from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.chains import create_extraction_chain
from src.config import Config
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DataExtractor:
    def __init__(self, api_key=Config.OPENAI_API_KEY):
        self.llm = ChatOpenAI(temperature=1,
                        model="gpt-3.5-turbo",
                        openai_api_key=api_key,
                        max_tokens=4097)

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

    def custom_template_data_extract(self, web_scraped_text, phrases):

        property_phrases = {}
        for phrase in phrases:
            property_phrases.update({
                phrase.replace(' ', '_'): {"type": "string"}
            })
        schema = {
            "properties": property_phrases
        }
        chain = create_extraction_chain(schema, self.llm)
        output = chain.run(web_scraped_text)
        return output

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
