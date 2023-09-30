from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.chains import create_extraction_chain
from src.config import Config

def call_bank_statement(data):

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

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=Config.OPENAI_API_KEY)
    chain = create_extraction_chain(schema, llm)
    output = chain.run(data)
    return output

def custom_template_data_extract(web_scraped_text, phrases):

    property_phrases = {}
    for phrase in phrases:
        property_phrases.update({
            phrase.replace(' ','_'): {"type": "string"}
        })

    schema = {
        "properties": property_phrases
    }

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=Config.OPENAI_API_KEY)
    chain = create_extraction_chain(schema, llm)
    output = chain.run(web_scraped_text)
    return output


def format_template(json):
    created_template = '''
    Please extract the fol
    '''
    
    if json.get('selectedCuisine') != 'Pot Luck':
        created_template += ' Focus on a {selectedCuisine} inspired meal.'
    if json.get('selectedCalorie') == 'Yes':
        created_template += ' Please include a calorie breakdown'
    if json.get('selectedDietry'):
        
        created_template += ' Please make sure the recipe is {dietaryString}'

    prompted_template = ChatPromptTemplate.from_template(created_template)

    if json.get('selectedDietry'): 
        dietaryString = ', '.join(json.get('selectedDietry'))
        filled_template = prompted_template.format_messages(
                selectedNo=json.get('selectedNo'),
                selectedCuisine=json.get('selectedCuisine'),
                dietaryString=dietaryString
        )
    else:
        filled_template = prompted_template.format_messages(
            selectedNo=json.get('selectedNo'),
            selectedCuisine=json.get('selectedCuisine'),
        )

    return filled_template


def format_template_second(json):

    created_template = '''

    Make sure this recipe is in the following format
    
    ingredients will expire soon and are in the recipe have been specified
    ingredients are in the pantry (other items) and are in the recipe have been specified
    any ingredients in the recipe that are not owned yet are displayed in a shopping list.
    
    full cooking instructions have been supplied
    
    '''
    if json.get('selectedCalorie') == 'Yes':
        created_template += ' A full calorie breakdown has been included'

    prompted_template = ChatPromptTemplate.from_template(created_template)


    return prompted_template


def get_chat_response(prompt, prompt2, json):
    chat = OpenAi(temparature=0.0)
    
    chain1 = LLMChain(llm=chat, prompt=prompt)
    chain2 = LLMChain(llm=chat, prompt=prompt2)

    simple_sequential_chain = SimpleSequentialChain(chains=(chain1, chain2), verbose=True)
    simple_sequential_chain.run('can you give me a recipe')
