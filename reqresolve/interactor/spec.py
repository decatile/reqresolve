import re

from dataclasses import dataclass

RE = re.compile(
    r'(?P<name>[a-z0-9_-]+)(\[(?P<extras>[a-z0-9_-]+(,[a-z0-9_-]+)*)])?(?P<version>(==|>=|<=|~=).*)?',
    re.IGNORECASE
)


@dataclass
class PackageSpec:
    name: str
    extra: str | None
    version: str | None

    def __str__(self):
        result = self.name
        if self.extra:
            result += f'[{self.extra}]'
        if self.version:
            result += self.version
        return result

    def versioned(self, value: str):
        return PackageSpec(self.name, self.extra, value)

    @property
    def unconstrained(self):
        return self.version is None

    @staticmethod
    def parse(value: str):
        value = value.strip().replace(' ', '')

        result = RE.fullmatch(value)
        if result is None:
            raise ValueError

        return PackageSpec(
            result.group('name'),
            result.group('extras') or None,
            result.group('version') or None
        )
