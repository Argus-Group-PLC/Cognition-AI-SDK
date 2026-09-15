from typing import Optional, List, Dict, Any, Generator, AsyncGenerator
from ..types import AskRequest, Message
from .base import SyncAPIResource, AsyncAPIResource

class Completions(SyncAPIResource):
    def create(
        self,
        *,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        stream: bool = False,
        tools: Optional[List[Dict[str, Any]]] = None,
        image_url: Optional[str] = None,
        image: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
        enable_web_search: Optional[bool] = None,
        chat_id: Optional[str] = None,
    ) -> Any:
        if not prompt and not messages:
            raise ValueError("Either 'prompt' or 'messages' must be provided.")
            
        req = AskRequest(
            prompt=prompt,
            messages=messages,
            model=model,
            temperature=temperature,
            stream=stream,
            tools=tools,
            image_url=image_url,
            image=image,
            response_format=response_format,
            enable_web_search=enable_web_search,
            chat_id=chat_id
        )
        
        if stream:
            return self._stream_request(req.model_dump(exclude_none=True))
        else:
            response = self._client.request("POST", "/ask", json=req.model_dump(exclude_none=True))
            return response.json()
            
    def _stream_request(self, payload: dict) -> Generator[str, None, None]:
        with self._client.stream("POST", "/ask", json=payload) as response:
            for line in response.iter_lines():
                if line.startswith("data: "):
                    yield line[6:]
                elif line and not line.startswith(":"):
                    yield line

class AsyncCompletions(AsyncAPIResource):
    async def create(
        self,
        *,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        stream: bool = False,
        tools: Optional[List[Dict[str, Any]]] = None,
        image_url: Optional[str] = None,
        image: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
        enable_web_search: Optional[bool] = None,
        chat_id: Optional[str] = None,
    ) -> Any:
        if not prompt and not messages:
            raise ValueError("Either 'prompt' or 'messages' must be provided.")
            
        req = AskRequest(
            prompt=prompt,
            messages=messages,
            model=model,
            temperature=temperature,
            stream=stream,
            tools=tools,
            image_url=image_url,
            image=image,
            response_format=response_format,
            enable_web_search=enable_web_search,
            chat_id=chat_id
        )
        
        if stream:
            return self._stream_request(req.model_dump(exclude_none=True))
        else:
            response = await self._client.request("POST", "/ask", json=req.model_dump(exclude_none=True))
            return response.json()
            
    async def _stream_request(self, payload: dict) -> AsyncGenerator[str, None]:
        async with self._client.stream("POST", "/ask", json=payload) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    yield line[6:]
                elif line and not line.startswith(":"):
                    yield line

class Chat(SyncAPIResource):
    @property
    def completions(self) -> Completions:
        return Completions(self._client)

class AsyncChat(AsyncAPIResource):
    @property
    def completions(self) -> AsyncCompletions:
        return AsyncCompletions(self._client)
