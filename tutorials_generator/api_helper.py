import json
import os
from tutorials_generator.template_generator import TemplateGenerator
from tutorials_generator.content_generator import ContentGenerator
from tutorials_generator.curriculum_generator import CurriculumGenerator


async def create_module(topic, identity = 'professor of computer science', target_audience='first year computer science students', tutorial_output_file='output.ipynb', wiki_output_file='output.md', model='gpt-4o', tutorial_output='tutorial_template.json', wiki_output='wiki_template.json'):

    # Generate and save the template
    template_generator = TemplateGenerator(topic, identity, target_audience)
    if tutorial_output != "tutorial_template.json":
        tutorial_template_file = f"{tutorial_output}/tutorial_template.json"
    if wiki_output != "wiki_template.json":
        wiki_template_file = f"{wiki_output}/tutorial_template.json"

    template_generator.save_tutorial_template_to_file(tutorial_template_file)
    template_generator.save_wiki_template_to_file(wiki_template_file)
    # Generate cell content using the ContentGenerator
    cg = ContentGenerator(model=model)
    await cg.create_notebook(tutorial_template_file, tutorial_output_file)
    await cg.create_wiki(wiki_template_file, wiki_output_file)


async def module(topic, identity, target_audience, tutorial_output_file, wiki_output_file, model):
    # Generate and save the template
    template_generator = TemplateGenerator(topic, identity, target_audience)
    tutorial_template_file = f'./modules/{topic}/{identity}/{target_audience}/tutorial_template.json'
    wiki_template_file = f'./modules/{topic}/{identity}/{target_audience}/wiki_template.json'
    if not os.path.exists(tutorial_template_file):
        await template_generator.save_tutorial_template_to_file(tutorial_template_file)

    if not os.path.exists(wiki_template_file):
        await template_generator.save_wiki_template_to_file(wiki_template_file)

    # Generate cell content using the ContentGenerator
    cg = ContentGenerator(model=model)
    await cg.create_notebook(tutorial_template_file, tutorial_output_file)
    await cg.create_wiki(wiki_template_file, wiki_output_file)

async def curriculum(identity, target_audience, model, curriculum_file_destination, curriculum_file):
    if not curriculum_file:
        raise Exception("A curriculum file must be provided.")
    
    if not curriculum_file_destination:
        curriculum_file_destination = "./Curriculum"

    with open(curriculum_file) as f:
        curriculum_data = json.load(f)
    if 'topics' not in curriculum_data:
        raise Exception(
            "The curriculum file must contain a 'topics' key with a list of topics.")

    os.makedirs(f"{curriculum_file_destination}/Wiki", exist_ok=True)
    os.makedirs(f"{curriculum_file_destination}/Interactive_Tutorials", exist_ok=True)

    for topic_index, topic in enumerate(curriculum_data['topics']):
        topic_name = topic['name']
        wiki_output = f"{curriculum_file_destination}/Wiki/{topic_index + 1}_{topic_name}"
        tutorial_output = f"{curriculum_file_destination}/Interactive_Tutorials/{topic_index + 1}_{topic_name}"
        os.makedirs(wiki_output, exist_ok=True)
        os.makedirs(tutorial_output, exist_ok=True)
        for subtopic_index, subtopic in enumerate(topic['subtopics']):
            tutorial_output_file = f"{tutorial_output}/subtopic_{subtopic_index + 1}.ipynb"
            wiki_output_file = f"{wiki_output}/subtopic_{subtopic_index + 1}.md"
            await create_module(subtopic, identity, target_audience,
                   tutorial_output_file, wiki_output_file, model, wiki_output, tutorial_output)

async def curriculum_template(topic, identity, target_audience, curriculum_output_file, model):
    # Generate and save the template
    ctg = CurriculumGenerator(model=model)
    if not os.path.exists(curriculum_output_file):
            os.makedirs(os.path.dirname(curriculum_output_file), exist_ok=True)
    await ctg.generate_curriculum_template(topic, identity, target_audience, curriculum_output_file)