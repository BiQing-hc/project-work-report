#!/usr/bin/env python3
"""Read local Git commit evidence within a report's calendar-date bounds."""

import argparse
from datetime import date, datetime
import json
import re
import subprocess
import sys


def git(repo, *arguments):
    result = subprocess.run(
        ["git", "-C", repo, *arguments],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or f"Git exited with code {result.returncode}")
    return result.stdout


def read_commits(repo, ref, start, end):
    tip = git(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").strip()
    raw_log = git(
        repo,
        "log",
        "--no-patch",
        "--no-show-signature",
        "--no-notes",
        "--encoding=UTF-8",
        "-z",
        "--format=tformat:%H%x00%P%x00%cI%x00%aI%x00%an%x00%s%x00%b",
        f"--since-as-filter={start.isoformat()}",
        f"--until={end.isoformat()}",
        tip,
        "--",
    )
    fields = raw_log.removesuffix("\0").split("\0") if raw_log else []
    if len(fields) % 7:
        raise ValueError("Unexpected git log output. Use git log to inspect this revision directly.")

    commits = []
    for index in range(0, len(fields), 7):
        sha, parents, committed_at, authored_at, author, subject, body = fields[index:index + 7]
        committed = datetime.fromisoformat(committed_at).astimezone(start.tzinfo)
        if start <= committed < end:
            commits.append({
                "sha": sha,
                "parents": parents.split(),
                "committed_at": committed.isoformat(),
                "authored_at": authored_at,
                "author": author,
                "subject": subject,
                "body": body.strip(),
            })

    return {
        "ref": ref,
        "tip": tip,
        "start_inclusive": start.isoformat(),
        "end_exclusive": end.isoformat(),
        "is_shallow": git(repo, "rev-parse", "--is-shallow-repository").strip() == "true",
        "commits": commits,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Local Git working directory")
    parser.add_argument("--ref", default="HEAD", help="Local revision to read, default HEAD")
    parser.add_argument("--start", type=date.fromisoformat, required=True, help="First day, YYYY-MM-DD")
    parser.add_argument("--end-before", type=date.fromisoformat, required=True, help="First day to exclude")
    parser.add_argument("--offset", default="+08:00", help="Report UTC offset, e.g. +08:00 or --offset=-05:00")
    args = parser.parse_args()

    if args.start >= args.end_before:
        parser.error("--end-before must be after --start")
    if not re.fullmatch(r"[+-](?:[01][0-9]|2[0-3]):[0-5][0-9]", args.offset):
        parser.error("--offset must have the form +08:00 or -05:00")
    start = datetime.fromisoformat(f"{args.start}T00:00:00{args.offset}")
    end = datetime.fromisoformat(f"{args.end_before}T00:00:00{args.offset}")

    try:
        result = read_commits(args.repo, args.ref, start, end)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot read Git evidence: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
