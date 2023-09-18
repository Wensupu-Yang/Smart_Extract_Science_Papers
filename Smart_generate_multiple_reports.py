import openai
from time import sleep
from halo import Halo
import textwrap
import yaml
import os
import PyPDF2


# File operations
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

def save_yaml(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)

def open_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

def load_prompts(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data['system_prompt'], data


# API functions
def chatbot(conversation, model="gpt-3.5-turbo-16k", temperature=0):
    max_retry = 7
    retry = 0
    while True:
        try:
            spinner = Halo(text='Thinking...', spinner='dots')
            spinner.start()
            
            response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature)
            text = response['choices'][0]['message']['content']

            spinner.stop()
            
            return text, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = conversation.pop(0)
                print('\n\n DEBUG: Trimming oldest message')
                continue
            retry += 1
            if retry >= max_retry:
                print(f"\n\nExiting due to excessive errors in API: {oops}")
                exit(1)
            print(f'\n\nRetrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)

def chat_print(text):
    formatted_lines = [textwrap.fill(line, width=120, initial_indent='    ', subsequent_indent='    ') for line in text.split('\n')]
    formatted_text = '\n'.join(formatted_lines)
    print('\n\n\nCHATBOT:\n\n%s' % formatted_text)

if __name__ == '__main__':
    # instantiate chatbot, variables
    openai.api_key = open_file('key_openai.txt').strip()

    # Load SYSTEM_PROMPT and FOLLOW_UP_PROMPTS from the YAML file
    SYSTEM_PROMPT, FOLLOW_UP_PROMPTS = load_prompts('prompts.yaml')
    FOLLOW_UP_PROMPTS.pop('system_prompt')  # Remove the system_prompt key from the dictionary

    # Get list of all PDF files in the input folder
    pdf_files = [f for f in os.listdir('input/') if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        # Check if the report already exists in the output folder
        filename = 'output/' + pdf_file.replace('.pdf', '.txt')
        if os.path.exists(filename):
            continue

        # Open the PDF file
        with open('input/' + pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            paper = ''
            for page_num in list(range(0,len(pdf_reader.pages))):
                page = pdf_reader.pages[page_num]
                paper += page.extract_text()

        if len(paper) > 50000:
            paper = paper[0:50000]
        
        ALL_MESSAGES = [{'role':'system', 'content': SYSTEM_PROMPT + paper}]
        report = ''
        
        # Initial prompt
        response, tokens = chatbot(ALL_MESSAGES)
        chat_print(response)
        ALL_MESSAGES.append({'role':'assistant', 'content': response})
        report += '\n\n\n\nQ: %s\n\nA: %s' % (SYSTEM_PROMPT, response)
        
        # Follow-up prompts based on the response
        if response in FOLLOW_UP_PROMPTS:
            for p in FOLLOW_UP_PROMPTS[response]:
                ALL_MESSAGES.append({'role':'user', 'content': p})
                response, tokens = chatbot(ALL_MESSAGES)
                chat_print(response)
                ALL_MESSAGES.append({'role':'assistant', 'content': response})
                report += '\n\n\n\nQ: %s\n\nA: %s' % (p, response)

        # Save the report
        save_file(filename, report.strip())
