import pytest
import pytest_asyncio
from jolted_mod import create_notebook_module, create_wiki_module


@pytest.mark.asyncio
async def test_create_notebook_module():
    topic = "Introduction to Python"
    identity = "Computer Science Instructor"
    target_audience = "CS101 Students"
    model = "gpt-3.5-turbo"

    # Run create_notebook_module and check that it doesn't return None
    result = await create_notebook_module(topic, identity, target_audience, model)
    print(result)
    assert result is not None, "Notebook content is None"


@pytest.mark.asyncio
async def test_create_wiki_module():
    topic = "Data Structures in Python"
    identity = "Computer Science Instructor"
    target_audience = "CS201 Students"
    model = "gpt-3.5-turbo"

    # Run create_wiki_module and check that it doesn't return None
    result = await create_wiki_module(topic, identity, target_audience, model)
    print(result)
    assert result is not None, "Wiki content is None"
