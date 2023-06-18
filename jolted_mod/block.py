from abc import ABC, abstractmethod
from jolted_mod.cell_type import CellType
from jolted_mod.config import prompts
from typing import Optional
from enum import Enum, auto


class BLOCK_TYPES(Enum):
    SEED_BLOCK = auto()
    EXPLANATORY_BLOCK = auto()
    KNOWLEDGE_TESTING_BLOCK = auto()


class Block(ABC):
    def __init__(
        self, cell_type: CellType, content: str = "", context=None, type="Base"
    ):
        self.cell_type = cell_type
        self.context = context
        self.content = content
        self.type = type

    def set_context(self, context_block):
        self.context = context_block

    def set_content(self, content: str):
        self.content = content

    @abstractmethod
    def generate_prompt(self) -> str:
        pass


class SeedBlock(Block):
    def __init__(
        self,
        identity: str,
        topic: str,
        target_audience: str,
        context=None,
        type="SEED_BLOCK",
    ):
        self.identity = identity
        self.topic = topic
        self.target_audience = target_audience
        super().__init__(CellType.MARKDOWN, type=type)

    def generate_prompt(self) -> str:
        return prompts["SeedBlock"].format(
            identity=self.identity,
            topic=self.topic,
            target_audience=self.target_audience,
        )


class ExplanatoryBlock(Block):
    def __init__(
        self,
        topic: str,
        knowledge_component: str,
        instructional_event: str,
        target_audience: str,
        cell_type: str,
        context: Optional[int] = None,
        type="EXPLANATORY_BLOCK",
    ):
        self.topic = topic
        self.knowledge_component = knowledge_component
        self.instructional_event = instructional_event
        self.target_audience = target_audience
        self.context = context
        super().__init__(CellType[cell_type.upper()], type=type)

    def generate_prompt(self) -> str:
        type_of_cell = "Markdown" if self.cell_type == CellType.MARKDOWN else "Code"
        return prompts["ExplanatoryBlockKC"].format(
            type_of_cell=type_of_cell,
            topic=self.topic,
            instructional_event=self.instructional_event,
            target_audience=self.target_audience,
            knowledge_component=self.knowledge_component,
        )


class KnowledgeTestingBlock(Block):
    def __init__(
        self,
        n: int,
        question_type: str,
        target_audience: str,
        topic: str,
        knowledge_component: str,
        cell_type: str,
        context: Optional[Block],
        type="KNOWLEDGE_TESTING_BLOCK",
    ):
        self.n = n
        self.question_type = question_type
        self.target_audience = target_audience
        self.topic = topic
        self.knowledge_component = knowledge_component
        self.context = context
        super().__init__(CellType[cell_type.upper()], type=type)

    def generate_prompt(self) -> str:
        if self.cell_type == CellType.MARKDOWN:
            return prompts["KnowledgeTestingBlockKC"]["markdown"].format(
                n=self.n,
                question_type=self.question_type,
                target_audience=self.target_audience,
                topic=self.topic,
                knowledge_component=self.knowledge_component,
            )
        else:
            context_content = self.context.content if self.context else ""
            return prompts["KnowledgeTestingBlockKC"]["code"].format(
                n=self.n,
                question_type=self.question_type,
                target_audience=self.target_audience,
                topic=self.topic,
                context_content=context_content,
                knowledge_component=self.knowledge_component,
            )
