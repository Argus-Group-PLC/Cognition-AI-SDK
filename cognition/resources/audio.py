from typing import Any, Optional
from .base import SyncAPIResource, AsyncAPIResource
from ..types import TranscribeRequest, TTSRequest

class Transcriptions(SyncAPIResource):
    def create(
        self,
        *,
        file: Optional[bytes] = None,
        file_base64: Optional[str] = None,
        model: str = "whisper-large-v3-turbo",
        response_format: str = "json"
    ) -> Any:
        if not file and not file_base64:
            raise ValueError("Either 'file' or 'file_base64' must be provided.")
            
        if file_base64:
            req = TranscribeRequest(file_base64=file_base64, model=model, response_format=response_format)
            res = self._client.request("POST", "/transcribe", json=req.model_dump(exclude_none=True))
        else:
            data = {"model": model, "response_format": response_format}
            files = {"file": file}
            res = self._client.request("POST", "/transcribe", data=data, files=files)
        return res.json()

class AsyncTranscriptions(AsyncAPIResource):
    async def create(
        self,
        *,
        file: Optional[bytes] = None,
        file_base64: Optional[str] = None,
        model: str = "whisper-large-v3-turbo",
        response_format: str = "json"
    ) -> Any:
        if not file and not file_base64:
            raise ValueError("Either 'file' or 'file_base64' must be provided.")
            
        if file_base64:
            req = TranscribeRequest(file_base64=file_base64, model=model, response_format=response_format)
            res = await self._client.request("POST", "/transcribe", json=req.model_dump(exclude_none=True))
        else:
            data = {"model": model, "response_format": response_format}
            files = {"file": file}
            res = await self._client.request("POST", "/transcribe", data=data, files=files)
        return res.json()

class Speech(SyncAPIResource):
    def create(
        self,
        *,
        input: str,
        model: str = "deepgram/aura-1",
        voice: str = "asteria",
        encoding: str = "binary"
    ) -> Any:
        req = TTSRequest(input=input, model=model, voice=voice, encoding=encoding)
        res = self._client.request("POST", "/tts", json=req.model_dump(exclude_none=True))
        
        if encoding == "binary":
            return res.content
        return res.json()

class AsyncSpeech(AsyncAPIResource):
    async def create(
        self,
        *,
        input: str,
        model: str = "deepgram/aura-1",
        voice: str = "asteria",
        encoding: str = "binary"
    ) -> Any:
        req = TTSRequest(input=input, model=model, voice=voice, encoding=encoding)
        res = await self._client.request("POST", "/tts", json=req.model_dump(exclude_none=True))
        
        if encoding == "binary":
            return res.content
        return res.json()

class Audio(SyncAPIResource):
    @property
    def transcriptions(self) -> Transcriptions:
        return Transcriptions(self._client)
        
    @property
    def speech(self) -> Speech:
        return Speech(self._client)

class AsyncAudio(AsyncAPIResource):
    @property
    def transcriptions(self) -> AsyncTranscriptions:
        return AsyncTranscriptions(self._client)
        
    @property
    def speech(self) -> AsyncSpeech:
        return AsyncSpeech(self._client)
