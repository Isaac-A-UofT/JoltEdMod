from fastapi import FastAPI, HTTPException
from typing import Optional
import os
from pydantic import BaseModel
from tutorials_generator.api_helper import module, curriculum, curriculum_template

app = FastAPI()

# Define the request models
class CurriculumRequest(BaseModel):
    topic: str
    identity: Optional[str] = "Professor of Computer Science"
    target_audience: Optional[str] = "first year computer science students"

class ModuleRequest(BaseModel):
    topic: str
    identity: Optional[str] = "Professor of Computer Science"
    target_audience: Optional[str] = "first year computer science students"

def read_modules_as_json(md_path, jupyter_path):
    response_data = {}

    # Read Markdown file
    if os.path.isfile(md_path):
        with open(md_path, "r") as md_file:
            response_data["wiki"] = md_file.read()
    else:
        response_data["wiki"] = None  # Handle file not found

    # Read Jupyter Notebook file
    if os.path.isfile(jupyter_path):
        with open(jupyter_path, "r") as jupyter_file:
            response_data["jupyter"] = jupyter_file.read()
    else:
        response_data["jupyter"] = None  # Handle file not found

    return response_data


def read_curriculum_as_json(md_dir, jupyter_dir):
    response_data = {
        "markdown_files": [],  # List to store lists of Markdown file contents
        "jupyter_files": []    # List to store lists of Jupyter Notebook file contents
    }

    # Get a list of subdirectories from both the Markdown and Jupyter directories
    md_folders = [f.path for f in os.scandir(md_dir) if f.is_dir()]
    jupyter_folders = [f.path for f in os.scandir(jupyter_dir) if f.is_dir()]

    # Iterate through the Markdown folders
    for md_folder in md_folders:
        folder_data = []  # List to store contents of the current Markdown folder
        md_files = [f for f in os.listdir(md_folder) if f.endswith('.md')]

        for md_file in md_files:
            with open(os.path.join(md_folder, md_file), "r") as file:
                folder_data.append(file.read())  # Append the content of the Markdown file

        response_data["markdown_files"].append(folder_data)  # Append the inner list to the outer list

    # Iterate through the Jupyter folders
    for jupyter_folder in jupyter_folders:
        folder_data = []  # List to store contents of the current Jupyter folder
        jupyter_files = [f for f in os.listdir(jupyter_folder) if f.endswith('.ipynb')]

        for jupyter_file in jupyter_files:
            with open(os.path.join(jupyter_folder, jupyter_file), "r") as file:
                folder_data.append(file.read())  # Append the content of the Jupyter file

        response_data["jupyter_files"].append(folder_data)  # Append the inner list to the outer list

    return response_data

# Define the asynchronous functions
async def generate_curriculum(topic, identity, target_audience):
    try:
        curriculum_file_path = f"./Curriculum/{topic}/{identity}"
        curriculum_template_path = f"./CurriculumTemplates/{topic}/{identity}/template.json"
        if not os.path.exists(curriculum_file_path):
            if not os.path.exists(curriculum_template_path):
                await curriculum_template(topic, identity, target_audience, curriculum_template_path, "gpt-4o")
            await curriculum(identity, target_audience, "gpt-4o", curriculum_file_path, curriculum_template_path)
        
        files_data = read_curriculum_as_json(f"{curriculum_file_path}/Wiki", f"{curriculum_file_path}/Interactive_Tutorials")

        return {"status": 200, **files_data}
    except Exception as e:
        print(f"Error in generate_curriculum: {e}")
        return {"status": 500}

async def generate_module(topic, identity="Professor of Computer Science", target_audience="first year computer science students"):
    try:
        jupyter_file_path = f'./modules/{topic}/{identity}/{target_audience}/output.ipynb'
        md_file_path = f'./modules/{topic}/{identity}/{target_audience}/output.md'

        if not os.path.isfile(f"./modules/{topic}/{identity}"):
            await module(topic, identity, target_audience, jupyter_file_path, md_file_path, "gpt-4o")

        files_data = read_modules_as_json(md_file_path, jupyter_file_path)

        return {"status": 200, **files_data}
    except Exception as e:
        print(f"Error in generate_module: {e}")
        return {"status": 500}

# POST endpoint for curriculum_template
@app.post("/generate_curriculum")
async def create_curriculum(request: CurriculumRequest):
    result = await generate_curriculum(
        request.topic,
        request.identity,
        request.target_audience,
    )
    return result

# POST endpoint for module
@app.post("/generate_module")
async def create_module(request: ModuleRequest):
    result = await generate_module(
        request.topic,
        request.identity,
        request.target_audience,
    )
    return result