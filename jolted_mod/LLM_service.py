import openai
import asyncio


async def chat_completion_create(
    session, model, messages, max_tokens, n, stop, temperature
):
    url = f"https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "n": n,
        "stop": stop,
        "temperature": temperature,
    }

    while True:
        try:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    raise Exception(
                        f"Error: {response.status}, {await response.text()}"
                    )
                return await response.json()

        except Exception as e:
            if "429" in str(e):  # Check if the error code is 429
                wait_time = (
                    60  # You can set this to the desired waiting time in seconds
                )
                print(f"Error 429 encountered. Retrying in {wait_time} seconds...")
                # Use asyncio.sleep instead of time.sleep for async code
                await asyncio.sleep(wait_time)
            else:
                raise  # If it's another exception, raise it as usual
