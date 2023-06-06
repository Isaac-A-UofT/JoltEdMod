from abc import ABC, abstractmethod
from jolted_mod.cell_type import CellType
from jolted_mod.config import prompts


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
        type="SeedBlock",
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
        method_of_teaching: str,
        target_audience: str,
        cell_type: str,
        context=None,
        type="ExplanatoryBlock",
    ):
        self.topic = topic
        self.method_of_teaching = method_of_teaching
        self.target_audience = target_audience
        super().__init__(CellType[cell_type.upper()], type=type)

    def generate_prompt(self) -> str:
        type_of_cell = "Markdown" if self.cell_type == CellType.MARKDOWN else "Code"
        return prompts["ExplanatoryBlock"].format(
            type_of_cell=type_of_cell,
            topic=self.topic,
            method_of_teaching=self.method_of_teaching,
            target_audience=self.target_audience,
        )


class KnowledgeTestingBlock(Block):
    def __init__(
        self,
        n: int,
        question_type: str,
        target_audience: str,
        topic: str,
        cell_type: str,
        context=None,
        type="KnowledgeTestingBlock",
    ):
        self.n = n
        self.question_type = question_type
        self.target_audience = target_audience
        self.topic = topic
        super().__init__(CellType[cell_type.upper()], type=type)

    def generate_prompt(self) -> str:
        if self.cell_type == CellType.MARKDOWN:
            return prompts["KnowledgeTestingBlock"]["markdown"].format(
                n=self.n,
                question_type=self.question_type,
                target_audience=self.target_audience,
                topic=self.topic,
            )
        else:
            context_content = self.context.content if self.context else ""
            return prompts["KnowledgeTestingBlock"]["code"].format(
                n=self.n,
                question_type=self.question_type,
                target_audience=self.target_audience,
                topic=self.topic,
                context_content=context_content,
            )
