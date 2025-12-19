from .abc import AbstractInteractor
from .pyproject import PyprojectInteractor
from .requirements import RequirementsInteractor
from .exception import InvalidSpecifierException, UnsupportedOperationException, MalformedSpecifiersException
from ..log import L


def for_filepath(filepath: str) -> AbstractInteractor:
    if filepath.endswith('.txt'):
        L.info('Detected plaintext (requirements.txt) file')
        return RequirementsInteractor(filepath)
    elif filepath.endswith('.toml'):
        L.info('Detected toml (pyproject.toml) file')
        return PyprojectInteractor(filepath)
    else:
        raise ValueError('Invalid file extension (.txt or .toml expected)')


__all__ = ('for_filepath', 'InvalidSpecifierException', 'UnsupportedOperationException', 'MalformedSpecifiersException')
