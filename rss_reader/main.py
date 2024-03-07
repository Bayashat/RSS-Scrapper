from argparse import ArgumentParser
from typing import Optional, Sequence
import xml.etree.ElementTree as ET
import requests
import json as JSON

from parser import UnhandledException, rss_parser


def main(argv: Optional[Sequence] = None):
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
        data = rss_parser(xml, args.limit, args.json)
        if args.json:
            print(JSON.loads("\n".join(data)))
        else:
            print("\n".join(data))   
        
    except Exception as e:
        raise UnhandledException(e)


main()