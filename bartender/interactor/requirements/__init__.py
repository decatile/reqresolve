import os
from io import StringIO
from typing import TextIO

from bartender.interactor.abc import AbstractInteractor
from bartender.interactor.exception import InvalidSpecifierException, MalformedSpecifiersException
from bartender.interactor.spec import PackageSpec
from bartender.log import L


class RequirementsInteractor(AbstractInteractor):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def _open_dependencies(self) -> list[str]:
        L.debug('Load dependencies from file')
        L.debug(f'Open file at {self._filepath}')
        with open(self._filepath, 'r') as f:
            return f.readlines()

    def load_specs(self) -> list[PackageSpec]:
        result: list[PackageSpec] = []
        errors: list[InvalidSpecifierException] = []

        with open(self._filepath) as f:
            for lineno, line in enumerate(f, 1):
                dep = PackageSpec.normalize(line)
                try:
                    result.append(PackageSpec.parse(dep))
                    L.debug(f'Detected dependency {dep}')
                except ValueError:
                    errors.append(InvalidSpecifierException(line, lineno))

        if errors:
            raise MalformedSpecifiersException(self._filepath, errors)

        L.info(f'Loaded {len(result)} dependencies from file')

        return result

    def _save_specs_to(self, specs: list[PackageSpec], writer: TextIO) -> None:
        for spec in specs:
            writer.write(str(spec))
            writer.write('\n')

    def save_specs(self, specs: list[PackageSpec]) -> None:
        L.debug(f'Rename {self._filepath} -> *.bak')
        os.rename(self._filepath, self._filepath + '.bak')

        L.debug(f'Write to new file at {self._filepath}')
        with open(self._filepath, 'w+') as f:
            self._save_specs_to(specs, f)

        L.info(f'Wrote to {self._filepath}, saved old as .bak')

    def dump_specs(self, specs: list[PackageSpec]) -> str:
        io = StringIO()
        self._save_specs_to(specs, io)
        return io.getvalue()


__all__ = ('RequirementsInteractor',)
