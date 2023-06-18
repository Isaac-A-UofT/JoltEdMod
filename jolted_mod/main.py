from jolted_mod.template_generator import TemplateGenerator
from jolted_mod.content_generator import ContentGenerator
from typing import Any, Dict, Optional
from jolted_mod.module_types import ModuleType
import asyncio

# import nbformat as nbf


class JoltedModException(Exception):
    """
    Custom exception type for Jolted Mod.
    """


async def get_default_notebook_template(
    topic: str,
    identity: str = "professor of computer science",
    target_audience: str = "first year computer science students",
    is_code: bool = True,
) -> Dict[str, Any]:
    try:
        template_generator = TemplateGenerator(topic, identity, target_audience)
        template = template_generator.create_template(
            code=is_code, template_type="notebook"
        )
        return template
    except Exception as e:
        raise Exception(f"Error occurred: {e}")
        return {}


async def create_notebook_module(
    topic: str,
    identity: str = "professor of computer science",
    target_audience: str = "first year computer science students",
    is_code: bool = True,
    model: str = "gpt-3.5-turbo",
    template: Optional[dict] = None,
) -> Dict[str, Any]:
    try:
        if not topic:
            raise ValueError("Topic cannot be empty")

        # Generate the template
        if not template:
            template_generator = TemplateGenerator(topic, identity, target_audience)
            template = template_generator.create_template(
                code=is_code, template_type="notebook"
            )
    except Exception as e:
        raise JoltedModException("Error generating notebook template.") from e

    try:
        # Generate cell content using the ContentGenerator
        cg = ContentGenerator(model=model)
        tutorial_content = await cg.create_module(template, type=ModuleType.NOTEBOOK)
    except Exception as e:
        raise JoltedModException("Error generating notebook content.") from e

    # nbf.write(tutorial_content, "test.ipynb")
    return tutorial_content


async def create_wiki_module(
    topic: str,
    identity: str = "professor of computer science",
    target_audience: str = "first year computer science students",
    is_code: bool = True,
    model: str = "gpt-3.5-turbo",
    template: Optional[dict] = None,
) -> str:
    try:
        if not topic:
            raise ValueError("Topic cannot be empty")

        # Generate the template
        if not template:
            template_generator = TemplateGenerator(topic, identity, target_audience)
            template = template_generator.create_template(
                code=is_code, template_type="wiki"
            )
    except Exception as e:
        raise JoltedModException("Error generating wiki template.") from e

    try:
        # Generate cell content using the ContentGenerator
        cg = ContentGenerator(model=model)
        wiki_content = await cg.create_module(template, type=ModuleType.WIKI)
    except Exception as e:
        raise JoltedModException("Error generating wiki content.") from e

    return wiki_content


async def create_curriculum(
    curriculum_data: Dict[str, Any],
    identity: str = "Professor of Computer Science",
    target_audience: str = "first year computer science students",
    is_code: bool = True,
    model: str = "gpt-3.5-turbo",
) -> Dict[str, Any]:
    """
    Creates a curriculum based on the provided curriculum data.

    Args:
        curriculum_data (Dict[str, Any]): The curriculum data containing topics and subtopics.
        identity (str): The identity of the content creator.
        target_audience (str): The target audience of the curriculum.
        model (str): The AI model used for content generation.

    Returns:
        Dict[str, Any]: The generated curriculum.
    """

    if "topics" not in curriculum_data:
        raise ValueError(
            "The curriculum data must contain a 'topics' key with a list of topics."
        )

    curriculum = {}
    for topic_index, topic in enumerate(curriculum_data["topics"]):
        topic_name = topic["name"]
        topic_content = {}
        for subtopic_index, subtopic in enumerate(topic["subtopics"]):
            tutorial_content = await create_notebook_module(
                subtopic, identity, target_audience, is_code, model
            )
            wiki_content = await create_wiki_module(
                subtopic, identity, target_audience, is_code, model
            )
            topic_content[subtopic] = {
                "tutorial": tutorial_content,
                "wiki": wiki_content,
            }
        curriculum[topic_name] = topic_content
    return curriculum


if __name__ == "__main__":
    # asyncio.run(create_notebook_module("Intro to for loops in python", model="gpt-4"))
    asyncio.run(create_notebook_module("Intro to for loops in python", model="gpt-4"))
