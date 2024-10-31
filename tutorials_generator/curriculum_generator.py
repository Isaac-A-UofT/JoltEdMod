import os
import openai
import asyncio
import re
from tqdm import tqdm
from tutorials_generator.block_factory import BlockFactory
import aiofiles

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
    
    async def generate_curriculum_template(self, topic, identity, target, output):
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
        blocks = await self._create_content()  # Wait for content generation to complete
        await self.create_markdown_file(blocks, output)
    
    async def _create_content(self):
        blocks = self.parse_config_file(self)

        if blocks[0].type == 'SeedBlock':
            self.system_block = blocks[0]
            blocks.pop(0)
        else:
            self.system_block = None

        # Generate content for all blocks asynchronously
        await self.generate_all_block_content(blocks)  # Wait for all content generation
        return blocks

    @staticmethod
    def parse_config_file(self):
        blocks = []
        for block_config in self.template['blocks']:
            block = BlockFactory.create_block(block_config)
            blocks.append(block)
        return blocks

    async def generate_all_block_content(self, blocks):
        with tqdm(total=len(blocks), desc="Generating block content") as pbar:
            tasks = [self.generate_block_content(block) for block in blocks]
            await asyncio.gather(*tasks)  # Wait for all tasks to complete
            pbar.update(len(blocks))  # Update progress bar after all blocks are done

    async def create_markdown_file(self, blocks, file_path):
        content = ""
        async with aiofiles.open(file_path, "w", encoding='utf-8') as f:
            for block in blocks:
                content += block.content

            cleaned_text = re.sub(r'```.*', '', content)
            await f.write(cleaned_text)
    
    async def generate_block_content(self, block):
        while True:
            try:
                response = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=[{
                        "role": "system",
                        "content": self.system_block.generate_prompt(),
                    }, {
                        "role": "user",
                        "content": block.generate_prompt(),
                    }],
                    max_tokens=self.max_tokens,
                    n=self.n,
                    stop=self.stop,
                    temperature=self.temperature,
                )
                response_content = response["choices"][0]["message"]["content"]
                block.set_content(response_content)
                break 
            except Exception as e:
                if "429" in str(e):
                    wait_time = 60
                    print(f"Error 429 encountered. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    raise