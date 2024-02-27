#!/usr/bin/env python3

import urllib.request
from pathlib import Path

page = 1

for page in range(1,76):
    url = "https://kde.org/announcements/"
    if page > 1:
        url += f"page/{page}"

    print(f"Getting {url}...")
    contents = urllib.request.urlopen(url).read()

    path = Path("announcements") / f"page-{page:02d}.html"
    print(f"Writing {path}...")

    with path.open("wb") as f:
        f.write(contents)
