from typing import List, Tuple, Any, Optional
import aiohttp
import aiofiles
import nbformat as nbf
import uuid
from alive_progress import alive_bar
from colorama import Fore, Style
import asyncio
from jolted_mod.cell_type import CellType
import openai
import os
from jolted_mod.block_factory import BlockFactory
from jolted_mod.LLM_service import chat_completion_create
from jolted_mod.block import Block, BLOCK_TYPES
from jolted_mod.module_types import ModuleType


class ContentGeneratorError(Exception):
    pass


class ContentGenerator:
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        system_block: Optional[Block] = None,
        max_tokens: int = 1024,
        n: int = 1,
        stop: Any = None,
        temperature: float = 0.7,
        blocks: List[Block] = [],
    ):
        self.model = model
        self.system_block = system_block
        self.max_tokens = max_tokens
        self.n = n
        self.stop = stop
        self.temperature = temperature
        self._set_api_key()
        self.blocks = blocks

    def _set_api_key(self):
        """Set OpenAI API key from the environment variable."""
        try:
            openai.api_key = os.environ.get("OPENAI_API_KEY")
            if not openai.api_key:
                raise ValueError("Environment variable OPENAI_API_KEY not set")
        except Exception as e:
            raise ContentGeneratorError(f"Failed to set API key: {e}")

    async def create_module(self, config: dict, type: ModuleType) -> Any:
        """Create a Module of type JupyterNotebook or Wiki (markdown) Notebook from the given config dictionary."""
        try:
            blocks = await self._parse_config(config)
        except Exception as e:
            raise ContentGeneratorError(f"Failed to parse config: {e}")

        try:
            await self._update_context(config, blocks)
        except Exception as e:
            raise ContentGeneratorError(f"Failed to update context: {e}")

        if blocks[0].type == BLOCK_TYPES.SEED_BLOCK.name:
            self.system_block = blocks.pop(0)

        try:
            async with aiohttp.ClientSession() as self._session:
                blocks = await self._generate_all_block_content(blocks)
        except Exception as e:
            raise ContentGeneratorError(f"Failed to generate block content: {e}")

        module: Any
        try:
            if type == ModuleType.NOTEBOOK:
                nb = nbf.v4.new_notebook()
                module = self._generate_notebook_cells(blocks, nb)
            elif type == ModuleType.WIKI:
                module = self._create_markdown_text(blocks)
            else:
                raise ValueError(f"Invalid module type: {type}")
        except Exception as e:
            raise ContentGeneratorError(f"Failed to create module: {e}")

        return module

    async def _parse_config(self, config: dict) -> List[Block]:
        """Parse the given config dictionary and create blocks asynchronously."""
        try:
            blocks: List[Block] = []
            for block_config in config["blocks"]:
                block = BlockFactory.create_block(block_config)
                blocks.append(block)

            return blocks
        except Exception as e:
            raise ContentGeneratorError(f"Failed to parse config: {e}")

    async def _update_context(self, config: dict, blocks: List[Block]) -> None:
        """Update block context using the given config dictionary asynchronously."""
        try:
            for block, block_config in zip(blocks, config["blocks"]):
                if "context" in block_config and block_config["context"] is not None:
                    block.set_context(blocks[block_config["context"]])
        except Exception as e:
            raise ContentGeneratorError(f"Failed to update context: {e}")

    async def _generate_all_block_content(self, blocks: List[Block]) -> List[Block]:
        """Generate content for all blocks asynchronously."""
        try:
            dependent_blocks, independent_blocks = self._split_blocks(blocks)

            spinner_style = "waves"

            with alive_bar(len(blocks), spinner=spinner_style, bar="smooth") as pbar:
                await asyncio.gather(
                    *[
                        self.generate_block_content(block)
                        for block in independent_blocks
                    ]
                )
                pbar(len(independent_blocks))
                for block in dependent_blocks:
                    await self.generate_block_content(block)
                    pbar(len(dependent_blocks))
            return blocks
        except Exception as e:
            raise ContentGeneratorError(f"Failed to generate block content: {e}")

    def _split_blocks(self, blocks: List[Block]) -> Tuple[List[Block], List[Block]]:
        """Split blocks into dependent and independent blocks."""
        try:
            dependent_blocks = [block for block in blocks if block.context is not None]
            independent_blocks = [block for block in blocks if block.context is None]
            return dependent_blocks, independent_blocks
        except Exception as e:
            raise ContentGeneratorError(f"Failed to split blocks: {e}")

    def _generate_notebook_cells(self, blocks: List[Block], nb: Any) -> Any:
        """Generate notebook cells from given blocks asynchronously."""
        try:
            for block in blocks:
                if block.cell_type == CellType.CODE:
                    new_cell = nbf.v4.new_code_cell(block.content)
                    new_cell["id"] = str(uuid.uuid4())  # Generate and set cell id
                    nb.cells.append(new_cell)
                elif block.cell_type == CellType.MARKDOWN:
                    nb.cells.append(nbf.v4.new_markdown_cell(block.content))
            return nb
        except Exception as e:
            raise ContentGeneratorError(f"Failed to generate notebook cells: {e}")

    def _create_markdown_text(self, blocks: List[Block]) -> str:
        """Create a markdown file from the given blocks."""
        try:
            markdown_text = ""
            for block in blocks:
                markdown_text += block.content
            return markdown_text
        except Exception as e:
            raise ContentGeneratorError(f"Failed to create markdown text: {e}")

    async def generate_block_content(self, block):
        while True:
            try:
                response = await chat_completion_create(
                    session=self._session,
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
                block.set_content(response["choices"][0]["message"]["content"])
                break  # If the response was successful, break out of the loop

            except Exception as e:
                if "429" in str(e):  # Check if the error code is 429
                    wait_time = (
                        60  # You can set this to the desired waiting time in seconds
                    )
                    print(f"Error 429 encountered. Retrying in {wait_time} seconds...")
                    # Use asyncio.sleep instead of time.sleep for async code
                    await asyncio.sleep(wait_time)
                else:
                    raise ContentGeneratorError(
                        f"Failed to generate block content: {e}"
                    )  # If it's another exception, raise it as ContentGeneratorError
