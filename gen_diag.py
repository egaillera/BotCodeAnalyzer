
import os
import subprocess
import openai
import sys
import webbrowser
import argparse

from langchain.chat_models import AzureChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def create_code_chain(openai,dialogs_code_language):
    # Init LLM to analize bot code
    llm_code = AzureChatOpenAI(deployment_name="egiGPT4", temperature=0.7, 
                        openai_api_key=openai.api_key, 
                        openai_api_base=openai.api_base,
                        openai_api_version = openai.api_version)

    system_message_template = "You are an AI code analyzer that read {code_language} code that implemetns a bot framework dialog, and explain the flow of the dialog \
                    from the point of view of the user interacting with the dialog. \
                    Avoid any explanation about the code and just explain the flow from the point of view of the user that is interacting with the dialog, \
                    numbering the different steps"

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message_template)
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt.format(code_language=dialogs_code_language), human_message_prompt])

    return LLMChain(llm=llm_code, prompt=chat_prompt)


def create_diagram_chain(openai):
    llm_diagram = AzureChatOpenAI(deployment_name="egiGPT4", temperature=0.7, 
                      openai_api_key=openai.api_key, 
                      openai_api_base=openai.api_base,
                      openai_api_version = openai.api_version)

    system_template = "You are an AI flow chart generator that read the description of a flow implemented by a bot, and generate mermaid code to draw a diagram  \
                    that represents the flow from the point of view of the user interacting with the dialog. \
                    Avoid any explanation about the flow and just generate the mermaid code to draw the diagram that represents the flow from the point of \
                    view of the user that is interacting with the bot"
                  

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    return LLMChain(llm=llm_diagram, prompt=chat_prompt)

def clean_mermaid_code(code):

    # Find graph line
    lines = code.split('\n')
    graph_line_index = next((i for i, line in enumerate(lines) if line.strip().startswith('graph')), None)

    if graph_line_index is not None:
        # Remove previous lines
        lines = lines[graph_line_index:]

    end_line_index = next((i for i, line in enumerate(lines) if line.strip().startswith('```')), None)

    if end_line_index is not None:
        # Remove subsequentlines
        lines = lines[:end_line_index]

    # Join line in a single string
    mermaid_code = '\n'.join(lines)

    return mermaid_code


def main():

    # Prepare parser for arguments
    parser = argparse.ArgumentParser(description='Code analyzer of bot dialogs')
    parser.add_argument('-f', '--file', type=str, help='File name with the code to analyze')
    parser.add_argument('-l', '--language',
                    type=str,
                    choices=['Typescript', 'C#'],
                    default='Typescript', required=False,
                    help='Programming language in which the code is written')
    args = parser.parse_args()

    # Configure Azure OpenAI Service API from .env file
    openai.api_type = os.environ["OPENAI_API_TYPE"]
    openai.api_base = os.environ["OPENAI_API_BASE"]
    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.api_version = os.environ["OPENAI_API_VERSION"]

    # Define language in which bot dialogs are written
    code_language = args.language

    # Create chain with the model that analyzes code and writes the flow from user POV
    code_chain=create_code_chain(openai,code_language)
    # Create chain with the model that generates the mermaid diagram taking the flow as input
    diagram_chain=create_diagram_chain(openai)

    # This is the overall chain where we run these two chains in sequence.
    from langchain.chains import SimpleSequentialChain
    overall_chain = SimpleSequentialChain(chains=[code_chain, diagram_chain], verbose=True)

    with open(args.file, 'r') as file:
        code_to_analyze = file.read()

    result = overall_chain.run(code_to_analyze)
    print(result)

    # Extract code, because LLM could add explanations and write to file
    mermaid_code = clean_mermaid_code(result)
    with open("diagram.mmd",'w') as diagram_description:
        diagram_description.write(mermaid_code)

    # Draw a PDF image taking the mermaid code as input and display it
    subprocess.call(["mmdc", "-i", "diagram.mmd", "-o", "diagram.pdf"])
    webbrowser.open('file:///' + os.getcwd() + '/diagram.pdf')
   

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()