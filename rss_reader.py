from argparse import ArgumentParser
from typing import Optional, Sequence
import requests
from rss_reader.parser import RSSParser, UnhandledException

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
    
    if not args.source:
        parser.print_help()
        return 1
    
    xml = requests.get(args.source).text
    try:
        rss_parser = RSSParser(xml)
        if args.json:
            print(rss_parser.to_json())
        else:
            output = dict(rss_parser.parse_channel(), **{"items": rss_parser.parse_items()})
            
            for key, value in output.items():
                if key == "items":
                    print()
                    for item in value:
                        for k,v in item.items():
                            print(f"{k}: {v}")
                        print()
                else:
                    print(f"{key}: {value}")
        return 0
    except Exception as e:
        raise UnhandledException(e)

if __name__ == "__main__":
    main()