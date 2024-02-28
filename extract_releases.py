#!/usr/bin/env python3

from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
import re

page = 1

def identify_release_by_url(url):
    m = re.search("kde.org/announcements/(.*)", url)
    if m:
        path = m.group(1).split("/")
        category = path[0]
        norelease_matches = ["conf-kde", "gsoc", "forum", "wikimedia", "announcement", "akademy", "fsfe", "cebit", "doc-loc", "response", "lwe", "k2", "sfcvs", "corel", "dld", "suse", "caldera"]
        if any(x in category for x in norelease_matches):
            return "norelease", None
        if "kirigami" in category:
            return "kirigami", None
        if "koffice" in category:
            return "koffice", None
        version1 = path[1]
        version2 = path[2]
        if "rc" in version2 or category == "megarelease":
            return "pre", None
        if category == "1-2-3" or category == "4":
            return "kde", version1
        if category == "gear":
            return "gear", version1
        if category == "frameworks":
            return "frameworks", version2
        version3 = path[2]
        if category == "plasma":
            return "plasma", version3
    return None, None

def identify_release_by_title(title):
    pre_matches = ["Release Candidate", "Beta", "beta", "Alpha", " RC"]
    if any(x in title for x in pre_matches):
        return "pre", None

    norelease_matches = ["conf.kde.in", "Summer of Code", "Eco-Certified", "PinePhone", "Purism", "Forum", "Wikimedia", "aKademy", "ZD Innovation", "Delix", "SuSE", "Support Of KDE", "CeBIT", "SourceForge", "LinuxWorld", "GNOME", "Stallman", "Linux Congress", "KDE Project Announced", "FSFE", "KDE 2 Launch Pad", "Corel"]
    if any(x in title for x in norelease_matches):
        return "norelease", None

    m = re.search("KDE Gear\D+([\d\.]+)", title)
    if m:
        return "gear", m.group(1)

    m = re.search("Frameworks (.*)", title)
    if m:
        return "frameworks", m.group(1)

    m = re.search("Plasma ([\d\.]+)", title)
    if m:
        return "plasma", m.group(1)

    m = re.search("([\d\.]+) Releases", title)
    if m:
        return "releases", m.group(1)

    m = re.search("KDE's (.*) Apps Update", title)
    if m:
        return "apps-update", m.group(1)

    m = re.search("Applications ([\d\.]+)", title)
    if m:
        return "applications", m.group(1)

    m = re.search("Kirigami (.*)", title)
    if m:
        return "kirigami", m.group(1)

    m = re.search("Applications and Platform ([\d\.]+)", title)
    if m:
        return "applications-platform", m.group(1)

    m = re.search("Software Compilation (.*)", title)
    if m:
        return "compilation", m.group(1)

    m = re.search("KDE (.*) Release", title)
    if m:
        return "kde", m.group(1)

    m = re.search("KOffice (.*) Release", title)
    if m:
        return "koffice", m.group(1)

    return None, None

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
                        stream, version = identify_release_by_title(title)
                    if element["class"][0] == "post-entry":
                        link = element.find("a")["href"]
#                        stream, version = identify_release_by_url(link)
                csv.write(f'{stream},{version},{date},"{title}",{link}\n')
