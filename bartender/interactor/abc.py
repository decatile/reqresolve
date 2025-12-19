from abc import ABC, abstractmethod

from bartender.interactor.spec import PackageSpec


class AbstractInteractor(ABC):
    @abstractmethod
    def load_specs(self) -> list[PackageSpec]: ...

    @abstractmethod
    def save_specs(self, specs: list[PackageSpec]) -> None: ...

    @abstractmethod
    def dump_specs(self, specs: list[PackageSpec]) -> str: ...
