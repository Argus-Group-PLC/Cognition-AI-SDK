from typing import Any, Optional
from .base import SyncAPIResource, AsyncAPIResource
from ..types import GenerateImageRequest

class Images(SyncAPIResource):
    def generate(
        self,
        *,
        prompt: str,
        model: str = "flux-1-schnell",
        negative_prompt: Optional[str] = None,
        response_format: str = "binary"
    ) -> Any:
        req = GenerateImageRequest(prompt=prompt, model=model, negative_prompt=negative_prompt, response_format=response_format)
        res = self._client.request("POST", "/generate_image", json=req.model_dump(exclude_none=True))
        
        if response_format == "binary":
            return res.content
        return res.json()

class AsyncImages(AsyncAPIResource):
    async def generate(
        self,
        *,
        prompt: str,
        model: str = "flux-1-schnell",
        negative_prompt: Optional[str] = None,
        response_format: str = "binary"
    ) -> Any:
        req = GenerateImageRequest(prompt=prompt, model=model, negative_prompt=negative_prompt, response_format=response_format)
        res = await self._client.request("POST", "/generate_image", json=req.model_dump(exclude_none=True))
        
        if response_format == "binary":
            return res.content
        return res.json()
