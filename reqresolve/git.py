from datetime import datetime, timezone, timedelta

from pygit2 import Repository, Commit


def find_newest_change(repository_root: str, relative_filepath: str) -> datetime:
    repo = Repository(repository_root)

    unix_time = (0, 0)
    commit: Commit | None = None
    for blame_hunk in repo.blame(relative_filepath):
        commit = repo.get(blame_hunk.orig_commit_id)
        assert commit is not None, 'cannot find a commit belongs to blame hunk'
        if commit.commit_time > unix_time:
            unix_time = commit.commit_time
    return datetime.fromtimestamp(unix_time,
                                  timezone(timedelta(minutes=commit.commit_time_offset)))
