"""Convert GitHub's paginated issue response into Jekyll feed data."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup


TITLE_PREFIX = "[动态]"
LOCAL_TIME = ZoneInfo("Asia/Shanghai")
OUTPUT = Path(__file__).resolve().parents[1] / "_data" / "moments.json"


def collect_moments(pages, owner):
    moments = []
    for page in pages:
        for issue in page:
            if (
                "pull_request" in issue
                or issue["state"] != "open"
                or (issue.get("user") or {}).get("login", "").lower() != owner.lower()
                or not issue["title"].startswith(TITLE_PREFIX)
            ):
                continue

            title = issue["title"].removeprefix(TITLE_PREFIX).strip()
            # GitHub's HTML representation has already sanitized the Markdown.
            body = BeautifulSoup(issue["body_html"] or "", "html.parser")
            photos = []
            for image in body.find_all("img"):
                src = image.get("src", "")
                if urlsplit(src).scheme != "https":
                    continue
                photos.append({"src": src, "alt": image.get("alt", "")})
                parent = image.parent
                image.decompose()
                if parent.name == "a" and not parent.decode_contents().strip():
                    parent.decompose()
            for paragraph in body.find_all("p"):
                if not paragraph.decode_contents().strip():
                    paragraph.decompose()

            if not title and not photos and not body.get_text(strip=True) and not body.find("video"):
                continue

            created_at = issue["created_at"]
            local_date = datetime.fromisoformat(created_at).astimezone(LOCAL_TIME).date()
            moments.append(
                {
                    "number": issue["number"],
                    "title": title,
                    "body": str(body).strip(),
                    "photos": photos,
                    "created_at": created_at,
                    "date": local_date.isoformat(),
                }
            )
    return sorted(moments, key=lambda moment: (moment["created_at"], moment["number"]), reverse=True)


if __name__ == "__main__":
    moments = collect_moments(json.load(sys.stdin), os.environ["GITHUB_REPOSITORY_OWNER"])
    OUTPUT.write_text(json.dumps(moments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {len(moments)} moments")
