from pathlib import Path
from bookmarker.links_md_parser import parse


def main():
    links_md = Path.home() / "temp" / "links.md"
    with open(links_md) as f:
        bookmarks = parse(f)
    print(f"Parsed {len(bookmarks)} bookmarks")


if __name__ == "__main__":
    main()
