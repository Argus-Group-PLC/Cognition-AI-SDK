from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Cognition, AsyncCognition

class SyncAPIResource:
    def __init__(self, client: "Cognition") -> None:
        self._client = client

class AsyncAPIResource:
    def __init__(self, client: "AsyncCognition") -> None:
        self._client = client
