from datetime import datetime, timezone, timedelta
from typing import cast

import rich
from pygit2 import Repository, Commit


def find_newest_change(repository_root: str, relative_filepath: str) -> datetime:
    repo = Repository(repository_root)

    time_unix = 0
    time_offset = 0
    for blame_hunk in repo.blame(relative_filepath):
        commit = cast(Commit | None, repo.get(blame_hunk.orig_commit_id))
        assert commit is not None
        if commit.commit_time > time_unix:
            time_unix = commit.commit_time
            time_offset = commit.commit_time_offset

    dt = datetime.fromtimestamp(
        time_unix,
        timezone(timedelta(minutes=time_offset))
    )
    rich.print(f'[yellow]Found newest change at {dt}.')
    return dt
