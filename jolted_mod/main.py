import asyncio
from jolted_mod.template_generator import TemplateGenerator
from jolted_mod.content_generator import ContentGenerator
from typing import Any, Dict


async def create_notebook_module(topic: str, identity: str = 'professor of computer science',
                                 target_audience: str = 'first year computer science students',
                                 model: str = 'gpt-3.5-turbo') -> Dict[str, Any]:
    """
    Creates a notebook module based on the provided topic.

    Args:
        topic (str): The topic for the notebook.
        identity (str): The identity of the content creator.
        target_audience (str): The target audience of the notebook.
        model (str): The AI model used for content generation.

    Returns:
        Dict[str, Any]: The generated notebook content.
    """

    if not topic:
        raise ValueError('Topic cannot be empty')

    # Generate the template
    template_generator = TemplateGenerator(topic, identity, target_audience)
    tutorial_template = template_generator.save_tutorial_template_to_file(
        'tutorial_template.json')

    # Generate cell content using the ContentGenerator
    cg = ContentGenerator(model=model)
    tutorial_content = await cg.create_notebook('tutorial_template.json')

    return tutorial_content


async def create_wiki_module(topic: str, identity: str = 'professor of computer science',
                             target_audience: str = 'first year computer science students',
                             model: str = 'gpt-3.5-turbo') -> str:
    """
    Creates a wiki module based on the provided topic.

    Args:
        topic (str): The topic for the wiki.
        identity (str): The identity of the content creator.
        target_audience (str): The target audience of the wiki.
        model (str): The AI model used for content generation.

    Returns:
        str: The generated wiki content in markdown format.
    """

    if not topic:
        raise ValueError('Topic cannot be empty')

    # Generate the template
    template_generator = TemplateGenerator(topic, identity, target_audience)
    wiki_template = template_generator.save_wiki_template_to_file(
        'wiki_template.json')

    # Generate cell content using the ContentGenerator
    cg = ContentGenerator(model=model)
    wiki_content = await cg.create_wiki('wiki_template.json')

    return wiki_content


async def create_curriculum(curriculum_data: Dict[str, Any], identity: str = 'Professor of Computer Science',
                            target_audience: str = 'first year computer science students',
                            model: str = 'gpt-3.5-turbo') -> Dict[str, Any]:
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

    if 'topics' not in curriculum_data:
        raise ValueError(
            "The curriculum data must contain a 'topics' key with a list of topics.")

    curriculum = {}
    for topic_index, topic in enumerate(curriculum_data['topics']):
        topic_name = topic['name']
        topic_content = {}
        for subtopic_index, subtopic in enumerate(topic['subtopics']):
            tutorial_content = await create_notebook_module(subtopic, identity, target_audience, model)
            wiki_content = await create_wiki_module(subtopic, identity, target_audience, model)
            topic_content[subtopic] = {
                "tutorial": tutorial_content, "wiki": wiki_content}
        curriculum[topic_name] = topic_content
    return curriculum
