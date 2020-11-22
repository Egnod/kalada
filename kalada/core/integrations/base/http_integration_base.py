from abc import ABC, abstractmethod
from typing import Optional

import fake_headers
import httpx


class BaseHTTPIntegration(ABC):
    @property
    @abstractmethod
    def identity(self) -> str:
        pass

    def __init__(
        self,
        session: Optional[httpx.AsyncClient] = None,
        close_after: bool = True,
    ) -> None:
        self._session: Optional[httpx.AsyncClient] = session
        self._close_after: bool = close_after
        self._self_session: Optional[httpx.AsyncClient] = None

    @property
    def session(self) -> httpx.AsyncClient:
        if self._session:
            return self._session
        elif not self._self_session:
            self._self_session = httpx.AsyncClient(headers=fake_headers.Headers().generate())

        return self._self_session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._close_after and not self._session:
            await self.session.aclose()
