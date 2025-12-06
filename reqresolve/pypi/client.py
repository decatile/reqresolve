import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, Generator, Iterable, Callable

import rich
from httpx import AsyncClient, Response

from reqresolve.pypi.exception import PackageNotFoundException, NoSuitableVersionException


@dataclass
class _ParseResponseEntry:
    version: str
    time: datetime


class PypiClient:
    def __init__(
            self,
            before_time: datetime,
            on_done: Callable[[], None] = lambda: None
    ) -> None:
        self._before_time = before_time
        self._inner = AsyncClient()
        self._mapping: dict[str, str] = {}
        self._tasks: list[Awaitable[None]] = []
        self._on_done = on_done

    def _parse_response(self, resp: Response) -> Generator[_ParseResponseEntry]:
        obj = resp.json()
        for version, releases in reversed(obj['releases'].items()):
            if not releases:
                continue

            upload_time = releases[0]['upload_time_iso_8601']
            yield _ParseResponseEntry(version, datetime.fromisoformat(upload_time))

    async def _task(self, package_name: str) -> None:
        resp = await self._inner.get(f'https://pypi.org/pypi/{package_name}/json')

        if resp.status_code == 404:
            raise PackageNotFoundException(package_name)

        resp.raise_for_status()

        for entry in self._parse_response(resp):
            if entry.time < self._before_time:
                self._mapping[package_name] = entry.version
                rich.print(f'[green]Found suitable version {entry.version} for package {package_name}')
                self._on_done()
                return

        raise NoSuitableVersionException(package_name)

    async def query_packages(self, packages: Iterable[str]) -> dict[str, str]:
        await asyncio.gather(*(self._task(package) for package in packages))
        return self._mapping
