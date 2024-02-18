from argparse import ArgumentParser
from typing import List, Optional, Sequence
import xml.etree.ElementTree as ET
import requests


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.
    """
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        raise UnhandledException(f"Error parsing XML: {e}")

    output = []

    # Extract information from <channel> element
    channel = root.find("channel")
    if channel:
        title = channel.findtext('title')
        link = channel.findtext('link')
        last_build_date = channel.findtext('lastBuildDate')
        pub_date = channel.findtext('pubDate')
        language = channel.findtext('language')
        categories = [category.text for category in channel.findall('.//category')]
        managing_editor = channel.findtext('managingEditor')
        description = channel.findtext('description')
        items = [item.findtext('title') for item in root.findall('.//item')]
        
        output.extend([
            f"Feed: {title}",
            f"Link: {link}",
            f"Last Build Date: {last_build_date}",
            f"Publish Date: {pub_date}",
            f"Language: {language}",
            f"Categories: {categories}",
            f"Editor: {managing_editor}",
            f"Description: {description}",
            f"Items: {items}"
        ])        
        
    # Extract information from <item> elements
    items = root.findall(".//item")
    for item in items:
        title = item.findtext('title')
        author = item.findtext('author')
        pub_date = item.findtext('pubDate')
        link = item.findtext('link')
        category = item.findtext('category')
        description = item.findtext('description')

        # Format the output for each item
        output.extend([
            f"\nTitle: {title}",
            f"Author: {author}",
            f"Published: {pub_date}",
            f"Link: {link}",
            f"Category: {category}",
            f"\n{description}"]
        )

    return output

def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)
    xml = requests.get(args.source).text
    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
