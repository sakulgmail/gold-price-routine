#!/usr/bin/env python3
"""
Commit+push a report file to git and send a LINE push notification.

Usage:
    python3 send_line.py "<message>" [--report-file path/to/report.md]

Environment variables required for LINE:
    LINE_ACCESS_TOKEN   LINE Messaging API channel access token
    LINE_USER_ID        LINE user ID (Uxxxxxxxxx…)

The --report-file argument, if given, is staged, committed, and pushed to
origin/main BEFORE the LINE message is sent. The commit message is derived
from the filename. Exits non-zero if git or LINE steps fail.
"""

import json
import os
import subprocess
import sys
import urllib.request


def git_commit_and_push(report_file: str) -> None:
    repo_root = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()

    filename = os.path.basename(report_file)
    commit_msg = f"report: gold price outlook {os.path.splitext(filename)[0]}"

    def run(cmd):
        result = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed: {' '.join(cmd)}\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )
        return result.stdout.strip()

    run(["git", "add", report_file])
    run(["git", "commit", "-m", commit_msg])

    # Retry push up to 3 times. Push current HEAD to origin/main explicitly,
    # since the checked-out local branch is not always named "main".
    for attempt in range(1, 4):
        result = subprocess.run(
            ["git", "push", "origin", "HEAD:main"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"Git push succeeded (attempt {attempt}).")
            return
        print(f"Git push attempt {attempt} failed: {result.stderr.strip()}", file=sys.stderr)
        if attempt < 3:
            import time; time.sleep(2 ** attempt)

    raise RuntimeError("Git push failed after 3 attempts.")


LINE_MAX_CHARS = 5000  # LINE Messaging API hard limit per text message


def send_line(text: str) -> None:
    token = os.environ.get("LINE_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")

    if len(text) > LINE_MAX_CHARS:
        print(
            f"WARNING: message is {len(text)} chars, truncating to {LINE_MAX_CHARS}.",
            file=sys.stderr,
        )
        text = text[: LINE_MAX_CHARS - 1] + "…"

    missing = [v for v, val in [("LINE_ACCESS_TOKEN", token), ("LINE_USER_ID", user_id)] if not val]
    if missing:
        raise RuntimeError(f"Missing environment variable(s): {', '.join(missing)}")

    body = json.dumps({
        "to": user_id,
        "messages": [{"type": "text", "text": text}],
    }).encode()

    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/push",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"LINE API response: {resp.status} {resp.reason}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"LINE API error: {e.code} {e.reason} — {e.read().decode()}")


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: send_line.py \"<message>\" [--report-file path/to/report.md]", file=sys.stderr)
        sys.exit(1)

    message = args[0]
    report_file = None

    if "--report-file" in args:
        idx = args.index("--report-file")
        if idx + 1 >= len(args):
            print("ERROR: --report-file requires a path argument", file=sys.stderr)
            sys.exit(1)
        report_file = args[idx + 1]

    exit_code = 0

    if report_file:
        try:
            git_commit_and_push(report_file)
        except Exception as e:
            print(f"ERROR (git): {e}", file=sys.stderr)
            exit_code = 1

    try:
        send_line(message)
    except Exception as e:
        print(f"ERROR (LINE): {e}", file=sys.stderr)
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
