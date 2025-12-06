import tomllib
from io import StringIO

from reqresolve.interactor.abc import AbstractInteractor
from reqresolve.interactor.exception import (
    InvalidSpecifierException,
    MalformedSpecifiersException,
    UnsupportedOperationException
)
from reqresolve.interactor.spec import PackageSpec


class PyprojectInteractor(AbstractInteractor):
    def __init__(self, filepath: str):
        self._filepath = filepath

    def load_specs(self) -> list[PackageSpec]:
        result: list[PackageSpec] = []
        errors: list[InvalidSpecifierException] = []

        with open(self._filepath, 'rb') as f:
            obj = tomllib.load(f)
            deps: list[str] = obj['project']['dependencies']
            for dep in deps:
                try:
                    result.append(PackageSpec.parse(dep))
                except ValueError:
                    errors.append(InvalidSpecifierException(dep.strip()))

        if errors:
            raise MalformedSpecifiersException(self._filepath, errors)

        return result

    def save_specs(self, specs: list[PackageSpec]):
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
