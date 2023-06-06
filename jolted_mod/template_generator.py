import json


class TemplateGenerator:
    def __init__(self, topic, identity, target_audience):
        self.topic = topic
        self.identity = identity
        self.target_audience = target_audience

    def generate_tutorial_code_template(self):
        template = {
            "blocks": [
                {
                    "type": "SeedBlock",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a metaphor without code",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a concrete code example that's thoroughly commented",
                    "target_audience": self.target_audience,
                    "context": 1,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KnowledgeTestingBlock",
                    "n": 1,
                    "question_type": "programming problem",
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KnowledgeTestingBlock",
                    "n": 1,
                    "question_type": "programming problem",
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                    "cell_type": "CODE",
                    "context": 3,
                },
            ]
        }
        return template

    def generate_wiki_code_template(self):
        template = {
            "blocks": [
                {
                    "type": "SeedBlock",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a metaphor without code",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a concrete code example that's thoroughly commented",
                    "target_audience": self.target_audience,
                    "context": 1,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "3 example use cases",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KnowledgeTestingBlock",
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
                    "type": "SeedBlock",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a metaphor",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a concrete example that's thoroughly explained based on the previous metaphor",
                    "target_audience": self.target_audience,
                    "context": 1,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KnowledgeTestingBlock",
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
                    "type": "SeedBlock",
                    "identity": self.identity,
                    "topic": self.topic,
                    "target_audience": self.target_audience,
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a metaphor",
                    "target_audience": self.target_audience,
                    "context": None,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "ExplanatoryBlock",
                    "topic": self.topic,
                    "method_of_teaching": "a concrete example that's thoroughly explained based on the previous metaphor",
                    "target_audience": self.target_audience,
                    "context": 1,
                    "cell_type": "MARKDOWN",
                },
                {
                    "type": "KnowledgeTestingBlock",
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

    def save_template_to_file(self, file_path, code=True, template_type="notebook"):
        if code:
            if template_type == "notebook":
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
