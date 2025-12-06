import os
from io import StringIO
from typing import TextIO

from reqresolve.interactor.abc import AbstractInteractor
from reqresolve.interactor.exception import InvalidSpecifierException, MalformedSpecifiersException
from reqresolve.interactor.spec import PackageSpec


class RequirementsInteractor(AbstractInteractor):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def load_specs(self) -> list[PackageSpec]:
        result: list[PackageSpec] = []
        errors: list[InvalidSpecifierException] = []

        with open(self._filepath) as f:
            for lineno, line in enumerate(f, 1):
                try:
                    result.append(PackageSpec.parse(line))
                except ValueError:
                    errors.append(InvalidSpecifierException(line.strip(), lineno))

        if errors:
            raise MalformedSpecifiersException(self._filepath, errors)

        return result

    def _save_specs_to(self, specs: list[PackageSpec], writer: TextIO) -> None:
        for spec in specs:
            writer.write(str(spec))
            writer.write('\n')

    def save_specs(self, specs: list[PackageSpec]) -> None:
        os.rename(self._filepath, self._filepath + '.bak')

        with open(self._filepath, 'w+') as f:
            self._save_specs_to(specs, f)

    def dump_specs(self, specs: list[PackageSpec]) -> str:
        io = StringIO()
        self._save_specs_to(specs, io)
        return io.getvalue()


__all__ = ('RequirementsInteractor',)
