from fastapi import FastAPI, HTTPException
from typing import Optional
import uuid
import json
from pydantic import BaseModel
import nbformat
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from api_tutorials_generator.api_helper import module, curriculum, curriculum_template

REGION = "us-east-2"

# Initialize the S3 client
s3_client = s3_client = boto3.client("s3")

app = FastAPI()


class CurriculumRequest(BaseModel):
    topic: str
    identity: Optional[str] = "Professor of Computer Science"
    target_audience: Optional[str] = "first year computer science students"
    generate_wiki: bool = False

class ModuleRequest(BaseModel):
    topic: str
    identity: Optional[str] = "Professor of Computer Science"
    target_audience: Optional[str] = "first year computer science students"
    generate_wiki: bool = False


# Define the asynchronous functions
async def generate_curriculum(topic, identity, target_audience, generate_wiki = False):
    try:

        template = json.loads(await curriculum_template(topic, identity, target_audience, "gpt-4o"))
        files_data = await curriculum(identity, target_audience, template, "gpt-4o", template, generate_wiki)

        return {"status": 200, **files_data}
    except Exception as e:
        print(f"Error in generate_curriculum: {e}")
        return {"status": 500}

async def generate_module(topic, identity="Professor of Computer Science", target_audience="first year computer science students", generate_wiki = False):
    try:
        files_data = await module(topic, identity, target_audience, "gpt-4o", generate_wiki)
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
    # Generate the module
    result = await generate_module(
        request.topic,
        request.identity,
        request.target_audience,
        request.generate_wiki or False
    )
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail=f"Failed generate file")    
    try:
        # Define the bucket name and file name with UUID
        bucket_name = "joltedmod"
        unique_id = str(uuid.uuid4())
        file_name = f"{request.topic.replace(' ', '_')}_{unique_id}.ipynb"

        # Upload the notebook to S3

        try:
            notebook_raw_text = nbformat.writes(result['notebook'])
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=notebook_raw_text,
                ContentType="text/plain"  # Change content type to 'text/plain'
            )
        except Exception as e:
            print(f"Error during S3 put_object: {e}")
            raise


        # Generate a pre-signed URL for the uploaded file
        file_url = f"https://{bucket_name}.s3.{REGION}.amazonaws.com/{file_name}"
        return {"status": 200, "url": file_url}

    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"Failed send file")