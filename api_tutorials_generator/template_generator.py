import json
import os

class TemplateGenerator:

    def __init__(self, topic, identity, target_audience):
        self.topic = topic
        self.identity = identity
        self.target_audience = target_audience

    def generate_tutorial_template(self):
        template = {
            "blocks": [
                {
                    "type": "SeedBlock",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "entry": "tutorial"
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a metaphor without code",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                    "entry": "tutorial"
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a concrete code example that's thoroughly commented",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                    "entry": "tutorial"
                },
                {
                    "type": "KnowledgeTestingBlock",
                    "n": 1,
                    "question_type": "programming problem",
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                    "entry": "tutorial"
                },
                {
                    "type": "KnowledgeTestingBlock",
                    "n": 1,
                    "question_type": "programming problem",
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "cell_type": "CODE",
                    "context": 3,
                    "entry": "tutorial"
                }
            ]
        }
        return template
    
    def generate_wiki_template(self):
        template = {
            "blocks": [
                {
                    "type": "SeedBlock",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "entry": "wiki"
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a metaphor without code",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                    "entry": "wiki"
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a concrete code example that's thoroughly commented",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                    "entry": "wiki"
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "3 example use cases",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                    "entry": "wiki"
                },
                {
                    "type": "KnowledgeTestingBlock",
                    "n": 5,
                    "question_type": "multiple choice",
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                    "entry": "wiki"
                }
            ]
        }
        return template
    
    def generate_curriculum_template(self):
        template = {
                    "type": "CurriculumBlock",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "entry": "curriculum"
                },
        return template

    def save_tutorial_template_to_file(self, file_path):
        template = self.generate_tutorial_template()
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(template, f, indent=2)

    def save_wiki_template_to_file(self, file_path):
        template = self.generate_wiki_template()
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(template, f, indent=2)
