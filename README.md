# Cognition AI Python SDK

The official Python SDK for the Cognition AI API. This library provides convenient access to the Cognition AI REST API from Python applications. It includes both synchronous and asynchronous clients.

For the full REST API documentation, please visit the [Official Cognition AI Documentation](https://docs.argusgroup.co.uk/docs/cognition).

## Installation

You can install the package via `pip`:

```bash
pip install argus-cognition-ai
```

## Configuration

To use the SDK, you need a Cognition API key. 

The easiest way to provide the key is to set it as an environment variable:
```bash
export COGNITION_API_KEY="your-api-key-here"
```

Then simply initialize the client:
```python
from cognition import Cognition

client = Cognition()
```

Alternatively, you can pass the key directly during instantiation:
```python
from cognition import Cognition

client = Cognition(api_key="your-api-key-here")
```

## Usage

### Chat / Completions (`/ask`)

**Standard Request**
```python
response = client.ask(
    prompt="Hello, world!",
    model="llama-3.1-8b-instant"
)
print(response)
```

**Streaming Request**
```python
stream = client.ask(
    prompt="Tell me a joke",
    stream=True
)
for chunk in stream:
    print(chunk, end="")
```

### Text-to-Speech (`/tts`)
Convert text into spoken audio.

```python
audio_bytes = client.audio.speech.create(
    input="Welcome to Cognition AI.",
    voice="asteria",
    encoding="binary"
)

with open("speech.mp3", "wb") as f:
    f.write(audio_bytes)
```

### Transcriptions (`/transcribe`)
Transcribe audio files into text.

```python
with open("speech.mp3", "rb") as audio_file:
    response = client.audio.transcriptions.create(
        file=audio_file.read(),
        model="whisper-large-v3-turbo",
        response_format="json"
    )
print(response)
```

### Image Generation (`/generate_image`)
Generate images from text prompts.

```python
image_bytes = client.images.generate(
    prompt="A futuristic cityscape at sunset",
    model="flux-1-schnell",
    response_format="binary"
)

with open("image.png", "wb") as f:
    f.write(image_bytes)
```

## Async Support

The SDK fully supports asynchronous operations using `AsyncCognition`:

```python
import asyncio
from cognition import AsyncCognition

async def main():
    client = AsyncCognition()
    
    response = await client.ask(
        prompt="Explain quantum computing in one sentence."
    )
    print(response)

asyncio.run(main())
```

### Async Streaming

```python
async def stream_example():
    client = AsyncCognition()
    stream = await client.ask(
        prompt="Write a short poem.",
        stream=True
    )
    async for chunk in stream:
        print(chunk, end="")
```

## Error Handling

The SDK raises structured exceptions for API errors, allowing you to catch specific status codes:

```python
from cognition.exceptions import AuthenticationError, RateLimitError, CognitionError

try:
    client.ask(prompt="Hello")
except AuthenticationError as e:
    print("Invalid API Key!")
except RateLimitError as e:
    print("Hit rate limit:", e)
except CognitionError as e:
    print(f"General API error: {e}")
```

## Connection Pooling

For optimal performance when making multiple requests, you can use the client as a context manager to share the underlying HTTP connection pool:

```python
with Cognition() as client:
    resp1 = client.ask(prompt="First question")
    resp2 = client.ask(prompt="Second question")
```

For async:
```python
async with AsyncCognition() as client:
    resp1 = await client.ask(prompt="First question")
    resp2 = await client.ask(prompt="Second question")
```
