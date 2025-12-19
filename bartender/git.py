import os.path
from datetime import datetime, timezone, timedelta
from typing import cast

from pygit2 import Repository, Commit

from bartender.log import L


def find_newest_change(repository_root: str, relative_filepath: str) -> datetime:
    L.debug(f'Opening git repository at {str(os.path.abspath(repository_root))}')

    repo = Repository(repository_root)

    time_unix = 0
    time_offset = 0
    for blame_hunk in repo.blame(relative_filepath):
        commit = cast(Commit | None, repo.get(blame_hunk.orig_commit_id))
        if commit is None:
            raise ValueError(f'Commit with ID {blame_hunk.orig_commit_id} is referenced by blame hunk, '
                             f'but an attempt to get its object from repo failed!')

        if commit.commit_time > time_unix:
            time_unix = commit.commit_time
            time_offset = commit.commit_time_offset

    dt = datetime.fromtimestamp(
        time_unix,
        timezone(timedelta(minutes=time_offset))
    )
    L.info(f'Found newest change at {dt}.')
    return dt
