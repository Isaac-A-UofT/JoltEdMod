import json
from jolted_mod.block_factory import BlockFactory
from typing import List, Optional
from pydantic import BaseModel


class BlockConfig(BaseModel):
    """Used to configure a block in a tutorial or wiki. Later instantiated into a Block Object"""

    type: str
    topic: str
    target_audience: str
    cell_type: str
    identity: Optional[str] = None
    knowledge_component: Optional[str] = None
    instructional_event: Optional[str] = None
    context: Optional[int] = None
    n: Optional[int] = None
    question_type: Optional[str] = None


class Template(BaseModel):
    blocks: List[BlockConfig]


class TemplateGenerator:
    def __init__(self, topic, identity, target_audience):
        self.topic = topic
        self.identity = identity
        self.target_audience = target_audience

    def generate_tutorial_code_template(self):
        template = {
            "blocks": [
                {
                    "type": "SEED_BLOCK",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "knowledge_component": f"A conceptual understanding of {self.topic}",
                    "instructional_event": "a metaphor without code",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "knowledge_component": f"A concrete understanding of the syntax of {self.topic}",
                    "instructional_event": f"A detailed breakdown of an example of the syntax of {self.topic}. It should be like the anatomy of {self.topic}'s syntax",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "knowledge_component": f"A concrete understanding of how to use {self.topic} to solve real-world problems",
                    "instructional_event": "A series of worked examples based on real-world use cases explained with highly detailed and well documented code",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KNOWLEDGE_TESTING_BLOCK",
                    "n": 1,
                    "question_type": "programming problem",
                    "topic": self.topic,
                    "knowledge_component": f"How to apply {self.topic} to solve real-world problems",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KNOWLEDGE_TESTING_BLOCK",
                    "n": 1,
                    "question_type": "programming problem",
                    "topic": self.topic,
                    "knowledge_component": f"How to apply {self.topic} to solve real-world problems",
                    "target_audience": self.target_audience,
                    "context": 4,
                    "cell_type": "CODE",
                },
            ]
        }
        return template

    def generate_wiki_code_template(self):
        template = {
            "blocks": [
                {
                    "type": "SEED_BLOCK",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "instructional_event": "a metaphor without code",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "instructional_event": "a concrete code example that's thoroughly commented",
                    "target_audience": self.target_audience,
                    "context": 1,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "instructional_event": "3 example use cases",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KNOWLEDGE_TESTING_BLOCK",
                    "n": 5,
                    "question_type": "multiple choice",
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
            ]
        }
        return template

    def generate_tutorial_noncode_template(self):
        template = {
            "blocks": [
                {
                    "type": "SEED_BLOCK",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "instructional_event": "a metaphor",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "instructional_event": "a concrete example that's thoroughly explained based on the previous metaphor",
                    "target_audience": self.target_audience,
                    "context": 1,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KNOWLEDGE_TESTING_BLOCK",
                    "n": 1,
                    "question_type": "essay question",
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
            ]
        }
        return template

    def generate_wiki_noncode_template(self):
        template = {
            "blocks": [
                {
                    "type": "SEED_BLOCK",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "instructional_event": "a metaphor",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "EXPLANATORY_BLOCK",
                    "topic": self.topic,
                    "instructional_event": "a concrete example that's thoroughly explained based on the previous metaphor",
                    "target_audience": self.target_audience,
                    "context": 1,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KNOWLEDGE_TESTING_BLOCK",
                    "n": 1,
                    "question_type": "essay question",
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
            ]
        }
        return template

    def create_template(self, code=True, template_type="notebook") -> dict:
        if code:
            if template_type == "notebook":
                print("Generating notebook code template...")
                template = self.generate_tutorial_code_template()
            elif template_type == "wiki":
                template = self.generate_wiki_code_template()
        else:
            if template_type == "notebook":
                template = self.generate_tutorial_noncode_template()
            elif template_type == "wiki":
                template = self.generate_wiki_noncode_template()
        return template

    def save_template_to_file(self, file_path, code=True, template_type="notebook"):
        if code:
            if template_type == "notebook":
                print("Generating notebook code template...")
                template = self.generate_tutorial_code_template()
            elif template_type == "wiki":
                template = self.generate_wiki_code_template()
        else:
            if template_type == "notebook":
                template = self.generate_tutorial_noncode_template()
            elif template_type == "wiki":
                template = self.generate_wiki_noncode_template()

        with open(file_path, "w") as f:
            json.dump(template, f, indent=2)
        return template
