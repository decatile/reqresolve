import asyncio
import os.path
from typing import cast

import rich
import rich.logging
from rich.progress import Progress

from bartender import cli
from bartender.git import find_newest_change
from bartender.interactor import for_filepath as interactor_for_filepath
from bartender.log import L, setup_logging
from bartender.pypi import PypiClient


async def _main() -> None:
    args = cli.parse()
    setup_logging(args.verbose)

    match args.command:
        case 'query':
            L.info(f'Using resolved time {args.time}')
            with Progress(transient=True) as p:
                task = p.add_task('Working...', total=len(args.packages))
                mappings = await PypiClient(
                    args.time,
                    lambda: p.update(task, advance=1)
                ).query_packages(args.packages)
            rich.get_console().rule('Results')
            for pkg in args.packages:
                print(f'{pkg}<={mappings[pkg]}')

        case 'file':
            fullpath = cast(str, os.path.join(args.root, args.file))
            before_time = find_newest_change(args.root, args.file)
            interactor = interactor_for_filepath(fullpath)
            packages = interactor.load_specs()
            unconstrained_packages = [pkg.name for pkg in packages if pkg.unconstrained]

            if len(unconstrained_packages) == 0:
                L.info('Nothing to do')
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
                rich.get_console().rule('Results')
                rich.print(f'{interactor.dump_specs(packages)}')


def main() -> None:
    asyncio.run(_main())


if __name__ == '__main__':
    main()
