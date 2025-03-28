from fastapi import FastAPI, HTTPException
from typing import Optional
import uuid
import json
from pydantic import BaseModel
import nbformat
import boto3
from mangum import Mangum
from botocore.exceptions import BotoCoreError, ClientError
from api_tutorials_generator.api_helper import module, curriculum, curriculum_template

REGION = "us-east-2"
IDENTITY="Professor of Computer Science"
TARGET_AUDIENCE="first year computer science students"
GENERATE_WIKI=False
MODEL="gpt-4o"

# Initialize the S3 client
s3_client = boto3.client("s3")

app = FastAPI()

class CurriculumRequest(BaseModel):
    topic: str
    identity: Optional[str] = IDENTITY
    target_audience: Optional[str] = TARGET_AUDIENCE
    generate_wiki: bool = GENERATE_WIKI

class ModuleRequest(BaseModel):
    topic: str
    identity: Optional[str] = IDENTITY
    target_audience: Optional[str] = TARGET_AUDIENCE
    generate_wiki: bool = GENERATE_WIKI


# Define the asynchronous functions
async def generate_curriculum(topic, identity, target_audience, generate_wiki = GENERATE_WIKI):
    try:

        template = json.loads(await curriculum_template(topic, identity, target_audience, MODEL))
        files_data = await curriculum(identity, target_audience, MODEL, template, generate_wiki)

        return {"status": 200, **files_data}
    except Exception as e:
        print(f"Error in generate_curriculum: {e}")
        return {"status": 500}

async def generate_module(topic, identity=IDENTITY, target_audience=TARGET_AUDIENCE, generate_wiki = GENERATE_WIKI):
    try:
        files_data = await module(topic, identity, target_audience, MODEL, generate_wiki)
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

@app.post("/generate_module")
async def create_module(request: ModuleRequest):
    result = await generate_module(
        request.topic,
        request.identity,
        request.target_audience,
        request.generate_wiki or GENERATE_WIKI
    )
    if result['status'] != 200:
        raise HTTPException(status_code=result['status'], detail="Failed to generate file")    
    
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

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send file")