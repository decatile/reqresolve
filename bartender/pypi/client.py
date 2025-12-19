import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, Generator, Iterable, Callable

from httpx import AsyncClient, Response

from bartender.log import L
from bartender.pypi.exception import PackageNotFoundException, NoSuitableVersionException


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
        L.debug(f'Request metadata for package {package_name}')
        resp = await self._inner.get(f'https://pypi.org/pypi/{package_name}/json')

        if resp.status_code == 404:
            raise PackageNotFoundException(package_name)

        resp.raise_for_status()

        L.info(f'Requested metadata for package {package_name}')
        for entry in self._parse_response(resp):
            L.debug(f'Try version {entry.version} at {entry.time}')
            if entry.time < self._before_time:
                L.info(f'Found suitable version {entry.version} for package {package_name}')
                self._mapping[package_name] = entry.version
                self._on_done()
                return

        raise NoSuitableVersionException(package_name)

    async def query_packages(self, packages: Iterable[str]) -> dict[str, str]:
        await asyncio.gather(*(self._task(package) for package in packages))
        return self._mapping
