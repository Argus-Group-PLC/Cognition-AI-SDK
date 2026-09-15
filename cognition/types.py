from typing import Any, Dict, List, Optional, Union, Generator, AsyncGenerator
from pydantic import BaseModel, ConfigDict

class Message(BaseModel):
    role: str
    content: str
    
class AskRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    prompt: Optional[str] = None
    messages: Optional[List[Message]] = None
    model: str = "llama-3.1-8b-instant"
    temperature: float = 0.7
    stream: bool = False
    tools: Optional[List[Dict[str, Any]]] = None
    image_url: Optional[str] = None
    image: Optional[str] = None
    response_format: Optional[Dict[str, Any]] = None
    enable_web_search: Optional[bool] = None
    chat_id: Optional[str] = None

class TranscribeRequest(BaseModel):
    model: str = "whisper-large-v3-turbo"
    response_format: str = "json"
    file_base64: Optional[str] = None

class TTSRequest(BaseModel):
    input: str
    model: str = "deepgram/aura-1"
    voice: str = "asteria"
    encoding: str = "binary"

class GenerateImageRequest(BaseModel):
    prompt: str
    model: str = "flux-1-schnell"
    negative_prompt: Optional[str] = None
    response_format: str = "binary"
