import tomllib
from io import StringIO
from typing import Never

from bartender.interactor.abc import AbstractInteractor
from bartender.interactor.exception import (
    InvalidSpecifierException,
    MalformedSpecifiersException,
    UnsupportedOperationException
)
from bartender.interactor.pyproject.model import FileModel
from bartender.interactor.spec import PackageSpec
from bartender.log import L


class PyprojectInteractor(AbstractInteractor):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def _open_dependencies(self) -> list[str]:
        L.debug('Load dependencies from file')
        L.debug(f'Open file at {self._filepath}')
        with open(self._filepath, 'rb') as f:
            L.debug('Parse in TOML format')
            obj = tomllib.load(f)
            L.debug('Verify file structure and get dependencies')
            return FileModel(**obj).project.dependencies

    def load_specs(self) -> list[PackageSpec]:
        result: list[PackageSpec] = []
        errors: list[InvalidSpecifierException] = []

        for dep in self._open_dependencies():
            dep = PackageSpec.normalize(dep)
            try:
                result.append(PackageSpec.parse(dep))
                L.debug(f'Detected dependency {dep}')
            except ValueError:
                errors.append(InvalidSpecifierException(dep))

        if errors:
            raise MalformedSpecifiersException(self._filepath, errors)

        L.info(f'Loaded {len(result)} dependencies from file')

        return result

    def save_specs(self, specs: list[PackageSpec]) -> Never:
        raise UnsupportedOperationException(
            'Saving to pyproject.toml is not supported, use --dry-run to get dependencies content'
        )

    def dump_specs(self, specs: list[PackageSpec]) -> str:
        io = StringIO()
        io.write('dependencies = [\n')
        for spec in specs:
            io.write(f'    "{str(spec)}",\n')
        io.write(']')
        return io.getvalue()


__all__ = ('PyprojectInteractor',)
