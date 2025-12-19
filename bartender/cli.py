from argparse import ArgumentParser, Namespace
from datetime import datetime, UTC
from typing import Callable


def datetime_like(is_local: bool) -> Callable[[str], datetime]:
    # noinspection PyBroadException
    def inner(value: str) -> datetime:
        try:
            num = int(value)
            return datetime.fromtimestamp(num, tz)
        except Exception:
            return datetime.fromisoformat(value).replace(tzinfo=tz)

    tz = datetime.now(UTC).astimezone().tzinfo if is_local else UTC
    inner.__name__ = 'datetime-like'
    return inner


def parse() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-v',
                        '--verbose',
                        action='count',
                        default=0,
                        help='-v : INFO, -vv : DEBUG messages')

    subparsers = parser.add_subparsers(dest='command')

    query_parser = subparsers.add_parser('query', help='Query packages without reading any file')
    query_parser.add_argument('packages',
                              nargs='+',
                              help='Package names to query')
    query_parser_group = query_parser.add_mutually_exclusive_group(required=True)
    query_parser_group.add_argument('-l',
                                    '--local-time',
                                    dest='time',
                                    type=datetime_like(True),
                                    help='Local time before which we query package versions (ISO | unix)')
    query_parser_group.add_argument('-u',
                                    '--utc-time',
                                    dest='time',
                                    type=datetime_like(False),
                                    help='UTC time before which we query package versions (ISO | unix)')

    file_parser = subparsers.add_parser('file', help='Query packages from selected file and write results into it')
    file_parser.add_argument('-r',
                             '--root',
                             default='.',
                             help="Root of the repository (default '.')")
    file_parser.add_argument('-f',
                             '--file',
                             default='requirements.txt',
                             help="Relative path (from root) to requirements file (default 'requirements.txt')")
    file_parser.add_argument('-d',
                             '--dry-run',
                             action='store_true',
                             help='Output packages into console (it helps when writing to specific format is not supported)')

    return parser.parse_args()
