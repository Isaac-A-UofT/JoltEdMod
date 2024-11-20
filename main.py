from fastapi import FastAPI, HTTPException
from typing import Optional
import json
from pydantic import BaseModel
from api_tutorials_generator.api_helper import module, curriculum, curriculum_template

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


# Define the asynchronous functions
async def generate_curriculum(topic, identity, target_audience):
    try:

        template = json.loads(await curriculum_template(topic, identity, target_audience, "gpt-4o"))
        files_data = await curriculum(identity, target_audience, template, "gpt-4o", template)

        return {"status": 200, **files_data}
    except Exception as e:
        print(f"Error in generate_curriculum: {e}")
        return {"status": 500}

async def generate_module(topic, identity="Professor of Computer Science", target_audience="first year computer science students"):
    try:
        files_data = await module(topic, identity, target_audience, "gpt-4o")
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

import asyncio

if __name__ == "__main__":
    asyncio.run(main())