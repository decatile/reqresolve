from datetime import datetime, UTC

import pytest
from reqresolve.pypi.client import PypiClient
from reqresolve.pypi.exception import NoSuitableVersionException, PackageNotFoundException


@pytest.mark.asyncio
async def test_existing_package() -> None:
    client = PypiClient(datetime.now(UTC))
    resp = await client.query_packages(['numpy'])
    assert len(resp) == 1


@pytest.mark.asyncio
async def test_non_existing_package() -> None:
    with pytest.raises(PackageNotFoundException):
        client = PypiClient(datetime.now(UTC))
        await client.query_packages(['-1'])


@pytest.mark.asyncio
async def test_no_matching_versions() -> None:
    with pytest.raises(NoSuitableVersionException):
        client = PypiClient(datetime(1900, 1, 1).astimezone(UTC))
        await client.query_packages(['numpy'])
