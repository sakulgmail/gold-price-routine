#!/usr/bin/env python3
"""Send a LINE push notification. Reads LINE_ACCESS_TOKEN and LINE_USER_ID from env."""

import json
import os
import sys
import urllib.request

def main():
    token = os.environ.get("LINE_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")

    if not token or not user_id:
        missing = [v for v, val in [("LINE_ACCESS_TOKEN", token), ("LINE_USER_ID", user_id)] if not val]
        print(f"ERROR: missing environment variable(s): {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: send_line.py <message_text>", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]

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
        print(f"LINE API error: {e.code} {e.reason} — {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
