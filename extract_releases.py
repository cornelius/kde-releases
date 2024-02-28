#!/usr/bin/env python3

from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
import re

page = 1

def identify_release(url, title):
    norelease_matches = ["Eco-Certified"]
    if any(x in title for x in norelease_matches):
        return "norelease", None

    pre_matches = ["Beta"]
    if any(x in title for x in pre_matches):
        return "pre", None

    m = re.search("KDE Gear\D+([\d\.]+)", title)
    if m:
        return "gear", m.group(1)

    m = re.search("Plasma ([\d\.]+)", title)
    if m:
        return "plasma", m.group(1)

    m = re.search("kde.org/announcements/(.*)", url)
    if m:
        path = m.group(1).split("/")
        category = path[0]
        norelease_matches = ["conf-kde", "gsoc", "forum", "wikimedia", "announcement", "akademy", "fsfe", "cebit", "doc-loc", "response", "lwe", "k2", "sfcvs", "corel", "dld", "suse", "caldera", "plasma-mobile"]
        if any(x in category for x in norelease_matches):
            return "norelease", None
        if "kirigami" in category:
            return None, None
        if "koffice" in category:
            return None, None
        version1 = path[1]
        version2 = path[2]
        if "rc" in version2 or "rc" in version1 or category == "megarelease":
            return "pre", None
        if category == "1-2-3" or category == "4":
            if "beta" in version1 or "alpha" in version1:
                return "pre", None
            if version1 == "3.0.5a":
                return "kde", version1
            versions = version1.split(".")
            if versions[0] == "1" and int(versions[1]) >= 89:
                return "pre", None
            m = re.search("^[\d\.]+$", version1)
            if m:
                return "kde", version1
            return None, None
        if category == "gear":
            return "gear", version1
        if category == "frameworks":
            if "alpha" in version1 or "tp" in version1:
                return "pre", None
            return "frameworks", version2
        if category == "releases":
            return "releases", version1
        if category == "applications":
            if version1 == "14.12.0":
                return "applications", "14.12"
            return "applications", version1
        version3 = path[2]
        if "alpha" in version3 or "rc" in version3 or "rc" in version2:
            return "pre", None
        if category == "plasma":
            if "alpha" in version1:
                return "pre", None
            return "plasma", version3
    return None, None

releases = {}

csv_path = Path("all-kde-releases.csv")
with csv_path.open("w") as csv:
    csv.write("Date,Title,Link\n")
    for page in range(1,76):
        path = Path("announcements") / f"page-{page:02d}.html"

        with path.open() as f:
            contents = f.read()

            soup = BeautifulSoup(contents, "html.parser")

            main = soup.find("div", id="main").find("div")
            for release in main.findAll("div", recursive=False):
                date = None
                title = None
                stream = None
                link = None
                for element in release.findChildren():
                    if element["class"][0] == "text-lighter":
                        date_str = element.text.split(",")[1]
                        date = datetime.strptime(date_str, " %d %B %Y").date()
                    if element.name == "h3":
                        title = element.text.replace("\n"," ")
                    if element["class"][0] == "post-entry":
                        link = element.find("a")["href"]
                stream, version = identify_release(link, title)
                if stream == None or stream == "pre" or stream == "norelease":
                    continue
                if stream in releases.keys():
                    releases[stream].append(version)
                else:
                    releases[stream] = [version]
                csv.write(f'{stream},{version},{date},"{title}",{link}\n')

if True:
    for stream in releases.keys():
        print(stream)
        print("  ", releases[stream])
