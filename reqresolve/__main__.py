import asyncio
import sys
from argparse import ArgumentParser
from pathlib import Path

import rich
from rich.progress import Progress

from reqresolve.git import find_newest_change
from reqresolve.interactor import for_filepath as interactor_for_filepath
from reqresolve.pypi import PypiClient


async def _main() -> None:
    parser = ArgumentParser()
    parser.add_argument('-r',
                        '--root',
                        default='.',
                        help="Root of the repository (default '.')")
    parser.add_argument('-f',
                        '--file',
                        default='requirements.txt',
                        help="Relative path (from root) to requirements file (default 'requirements.txt')")
    parser.add_argument('-d',
                        '--dry-run',
                        action='store_true',
                        help='Output packages into console (it helps when writing to specific format is not supported)')
    args = parser.parse_args(sys.argv[1:])
    fullpath = str(Path(args.root) / args.file)
    before_time = find_newest_change(args.root, args.file)
    interactor = interactor_for_filepath(fullpath)
    packages = interactor.load_specs()
    unconstrained_packages = [pkg.name for pkg in packages if pkg.unconstrained]

    if len(unconstrained_packages) == 0:
        rich.print('[yellow]Nothing to do')
        return

    with Progress(transient=True) as p:
        task = p.add_task('Working...', total=len(unconstrained_packages))
        mappings = await PypiClient(
            before_time,
            lambda: p.update(task, advance=1)
        ).query_packages(unconstrained_packages)

    packages = [
        i.versioned(f'<={mappings[i.name]}') if i.unconstrained else i
        for i in packages
    ]
    if not args.dry_run:
        interactor.save_specs(packages)
    else:
        rich.print(f'[blue]{interactor.dump_specs(packages)}')


def main() -> None:
    asyncio.run(_main())

if __name__ == '__main__':
    main()
