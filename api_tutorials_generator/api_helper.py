import json
import os
from api_tutorials_generator.template_generator import TemplateGenerator
from api_tutorials_generator.api_content_generator import ContentGenerator
from api_tutorials_generator.curriculum_generator import CurriculumGenerator


async def create_module(topic, identity = 'professor of computer science', target_audience='first year computer science students', model='gpt-4o'):
    # Generate and save the template
    template_generator = TemplateGenerator(topic, identity, target_audience)

    tutorial_template = template_generator.generate_tutorial_template()
    wiki_template = template_generator.generate_wiki_template()

    # Generate cell content using the ContentGenerator
    cg = ContentGenerator(model=model)
    notebook = await cg.create_notebook(tutorial_template)
    wiki = await cg.create_wiki(wiki_template)
    return {"notebook": notebook, "wiki": wiki}


async def module(topic, identity, target_audience, model):
    # Generate and save the template
    template_generator = TemplateGenerator(topic, identity, target_audience)

    tutorial_template = template_generator.generate_tutorial_template()
    wiki_template = template_generator.generate_wiki_template()

    # Generate cell content using the ContentGenerator
    cg = ContentGenerator(model=model)
    notebook = await cg.create_notebook(tutorial_template)
    wiki = await cg.create_wiki(wiki_template)
    return {"notebook": notebook, "wiki": wiki}

async def curriculum(identity, target_audience, model, curriculum):
    curriculum_data = []
    for topic_index, topic in enumerate(curriculum['topics']):
        topic_name = topic['name']
        subtopics = []
        for subtopic_index, subtopic in enumerate(topic['subtopics']):
            data = await create_module(subtopic, identity, target_audience, model)
            subtopics.append({subtopic: data})

        curriculum_data.append({topic_name: subtopics})

async def curriculum_template(topic, identity, target_audience, model):
    # Generate and save the template
    ctg = CurriculumGenerator(model=model)

    return await ctg.generate_curriculum_template(topic, identity, target_audience)