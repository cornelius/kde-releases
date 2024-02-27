#!/usr/bin/env python3

from pathlib import Path
from bs4 import BeautifulSoup

page = 1

csv_path = Path("all-kde-releases.csv")
with csv_path.open("w") as csv:
    csv.write("Day,Date,Title,Link\n")
    for page in range(1,76):
        path = Path("announcements") / f"page-{page:02d}.html"

        with path.open() as f:
            contents = f.read()

            soup = BeautifulSoup(contents, "html.parser")

            main = soup.find("div", id="main").find("div")
            for release in main.findAll("div", recursive=False):
                date = None
                title = None
                link = None
                for element in release.findChildren():
                    if element["class"][0] == "text-lighter":
                        date = element.text
                    if element.name == "h3":
                        title = element.text
                    if element["class"][0] == "post-entry":
                        link = element.find("a")["href"]
                csv.write(f'{date},"{title}",{link}\n')
