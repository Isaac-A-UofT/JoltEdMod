import os
import openai
import time
import re
from tqdm import tqdm
from tutorials_generator.block_factory import BlockFactory

class CurriculumGenerator:
    def __init__(self, model="gpt-4o", system_block=None, max_tokens=1024, n=1, stop=None, temperature=0.7, blocks=None):
        self.model = model
        self.system_block = system_block
        self.max_tokens = max_tokens
        self.n = n
        self.stop = stop
        self.temperature = temperature
        self._set_api_key()
        self.blocks = blocks
        self.model = model
        self.template = {}
        return 
    
    def _set_api_key(self):
        """Set OpenAI API key from the environment variable."""
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("Environment variable OPENAI_API_KEY not set")
    
    def generate_curriculum_template(self, topic, identity, target, output):
        self.template = {
            "blocks": [
                {
                    "type": "SeedBlock",
                    "identity": identity,
                    "topic": topic,
                    "target_audience": target,
                    "entry": "tutorial"
                },
                {
                    "type": "CurriculumBlock",
                    "identity": identity,
                    "topic": topic,
                    "target_audience": target,
                    "entry": "curriculum"
                }
            ]
        }
        blocks = self._create_content()
        self.create_markdown_file(blocks, output)
    
    def _create_content(self):
        blocks = self.parse_config_file(self)

        if blocks[0].type == 'SeedBlock':
            self.system_block = blocks[0]
            blocks.pop(0)
        else:
            self.system_block = None

        self.generate_all_block_content(blocks)
        return blocks

    @staticmethod
    def parse_config_file(self):
        blocks = []
        for block_config in self.template['blocks']:
            block = BlockFactory.create_block(block_config)
            blocks.append(block)
        return blocks

    def generate_all_block_content(self, blocks):
        with tqdm(total=len(blocks), desc="Generating block content") as pbar:
            for block in blocks:
                self.generate_block_content(block)
                pbar.update(1)
    
    def create_markdown_file(self, blocks, file_path):
        content = ""
        with open(file_path, "w", encoding='utf-8') as f:
            for block in blocks:
                content += block.content

            cleaned_text = re.sub(r'```.*', '', content)
            f.write(cleaned_text)
    
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
            