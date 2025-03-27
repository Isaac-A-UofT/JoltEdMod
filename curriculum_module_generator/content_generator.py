import os
import openai
import nbformat as nbf
import markdown2
from markdownify import markdownify as md
import json
import uuid
import time
import re
import asyncio
from tqdm import tqdm
from curriculum_module_generator.block import Block
from curriculum_module_generator.cell_type import CellType
from curriculum_module_generator.block_factory import BlockFactory


class ContentGenerator:
    def __init__(self, model="gpt-4o", system_block=None, max_tokens=1024, n=1, stop=None, temperature=0.7, blocks=None):
        self.model = model
        self.system_block = system_block
        self.max_tokens = max_tokens
        self.n = n
        self.stop = stop
        self.temperature = temperature
        self._set_api_key()
        self.blocks = blocks

    def _set_api_key(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("Environment variable OPENAI_API_KEY not set")

    def generate_block_content(self, block):
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": self.system_block.generate_prompt(),
                        },
                        {"role": "user", "content": block.generate_prompt()},
                    ],
                    max_tokens=self.max_tokens,
                    n=self.n,
                    stop=self.stop,
                    temperature=self.temperature,
                )
                # Get the content from the response
                response_content = response["choices"][0]["message"]["content"]

                if block.type == "KnowledgeTestingBlock" and block.entry == "tutorial":
                    # Split the content into blocks based on language identifiers
                    language, response_content = self.parse_code_blocks(response_content)

                    block.set_language(language)

                block.set_content(response_content)
                break  # If successful, break out of the loop

            except Exception as e:
                if "429" in str(e):  # Check if the error code is 429
                    wait_time = 60  # You can set this to the desired waiting time in seconds
                    print(
                        f"Error 429 encountered. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise  # If it's another exception, raise it as usual

    def generate_all_block_content(self, blocks):
        with tqdm(total=len(blocks), desc="Generating block content") as pbar:
            for block in blocks:
                self.generate_block_content(block)
                pbar.update(1)

    def create_notebook(self, config_file, output_file):
        nb = nbf.v4.new_notebook()
        blocks = self._create_content(config_file)
        self._generate_notebook_blocks(blocks, nb)
        nbf.write(nb, output_file)

        return nb

    def _generate_notebook_blocks(self, blocks, nb):
        for block in blocks:
            if block.cell_type == CellType.CODE:
                new_cell = nbf.v4.new_code_cell(block.content)
                new_cell['id'] = str(uuid.uuid4())  # Generate and set cell id
                
                # Set the language in the metadata
                if hasattr(block, 'language') and block.language:
                    new_cell.metadata['language'] = block.language
                    new_cell.metadata['kernelspec'] = {
                        "display_name": block.language.capitalize(),
                        "language": block.language,
                        "name": block.language.lower()
                    }
                
                nb.cells.append(new_cell)
            elif block.cell_type == CellType.MARKDOWN:
                nb.cells.append(nbf.v4.new_markdown_cell(block.content))
        
        return nb



    def create_markdown_file(self, blocks, file_path):
        markdown_text = ""
        with open(file_path, "w") as f:
            for block in blocks:
                markdown_text += markdown2.markdown(block.content, extras=["fenced-code-blocks"])
            f.write(md(markdown_text))

    def create_wiki(self, config_file, output_file):
        blocks = self._create_content(config_file)
        self.create_markdown_file(blocks, output_file)

    def _create_content(self, config_file):
        blocks = self.parse_config_file(config_file)
        self.update_context(config_file, blocks)

        if blocks[0].type == 'SeedBlock':
            self.system_block = blocks[0]
            blocks.pop(0)
        else:
            self.system_block = None

        self.generate_all_block_content(blocks)
        return blocks

    @staticmethod
    def update_context(config_file, blocks):
        with open(config_file) as f:
            config = json.load(f)
            for block, block_config in zip(blocks, config['blocks']):
                if 'context' in block_config and block_config['context'] is not None:
                    block.set_context(blocks[block_config['context']])

    @staticmethod
    def parse_config_file(config_file):
        with open(config_file) as f:
            config = json.load(f)
            blocks = []
            for block_config in config['blocks']:
                block = BlockFactory.create_block(block_config)
                blocks.append(block)
            return blocks

    @staticmethod  
    def parse_code_blocks(content):
        """Parse the API response content to extract code blocks and their languages."""

        code_blocks = []
        pattern = r'```(\w*)\n(.*?)```'  # Language is optional
        matches = re.findall(pattern, content, re.DOTALL)

        # If matches are found, process them
        if matches:
            first_lang = matches[0][0] if matches[0][0] else None  # Get the first language
            combined_code = []

            for lang, code in matches:
                if lang == first_lang or first_lang is None:  # Append code to combined_code
                    combined_code.append(code.strip())
            
            # Append the first language (or None) and the combined code as a single string
            return (first_lang, '\n'.join(combined_code))
        else:
            # If no code blocks are found, return the entire content with None for language
            return (None, content.strip())