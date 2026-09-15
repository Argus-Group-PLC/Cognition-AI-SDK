import os
from typing import Optional, Dict, Any, Generator, AsyncGenerator
import httpx

from .exceptions import CognitionError, make_status_error

# Forward import
from .resources.chat import Chat
from .resources.audio import Audio
from .resources.images import Images
from .resources.chat import AsyncChat
from .resources.audio import AsyncAudio
from .resources.images import AsyncImages

class BaseClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.argusgroup.co.uk/v1/cognition"):
        self.api_key = api_key or os.environ.get("COGNITION_API_KEY")
        if not self.api_key:
            raise ValueError("The api_key client option must be set either by passing api_key to the client or by setting the COGNITION_API_KEY environment variable")
        
        self.base_url = base_url
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response: httpx.Response) -> httpx.Response:
        if not response.is_success:
            try:
                body = response.json()
            except Exception:
                body = {"details": response.text}
            raise make_status_error(response.status_code, body)
        return response

class Cognition(BaseClient):
    """Synchronous client for the Cognition API."""
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.argusgroup.co.uk/v1/cognition", timeout: float = 60.0):
        super().__init__(api_key, base_url)
        self._client = httpx.Client(base_url=self.base_url, headers=self._headers, timeout=timeout)
        
        self.chat = Chat(self)
        self.audio = Audio(self)
        self.images = Images(self)

    def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        response = self._client.request(method, path, **kwargs)
        return self._handle_response(response)
        
    import contextlib
    
    @contextlib.contextmanager
    def stream(self, method: str, path: str, **kwargs) -> Generator[httpx.Response, None, None]:
        request = self._client.build_request(method, path, **kwargs)
        with self._client.stream(method, request.url, **kwargs) as response:
            if not response.is_success:
                response.read()
                self._handle_response(response)
            yield response

    def ask(self, **kwargs) -> Any:
        """Alias for chat.completions.create"""
        return self.chat.completions.create(**kwargs)

    def __enter__(self):
        self._client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.__exit__(exc_type, exc_val, exc_tb)

class AsyncCognition(BaseClient):
    """Asynchronous client for the Cognition API."""
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.argusgroup.co.uk/v1/cognition", timeout: float = 60.0):
        super().__init__(api_key, base_url)
        self._client = httpx.AsyncClient(base_url=self.base_url, headers=self._headers, timeout=timeout)
        
        self.chat = AsyncChat(self)
        self.audio = AsyncAudio(self)
        self.images = AsyncImages(self)

    async def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        response = await self._client.request(method, path, **kwargs)
        return self._handle_response(response)

    import contextlib
    
    @contextlib.asynccontextmanager
    async def stream(self, method: str, path: str, **kwargs) -> AsyncGenerator[httpx.Response, None]:
        request = self._client.build_request(method, path, **kwargs)
        async with self._client.stream(method, request.url, **kwargs) as response:
            if not response.is_success:
                await response.aread()
                self._handle_response(response)
            yield response

    async def ask(self, **kwargs) -> Any:
        """Alias for chat.completions.create"""
        return await self.chat.completions.create(**kwargs)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.__aexit__(exc_type, exc_val, exc_tb)
