import xml.etree.ElementTree as ET
from typing import List, Optional


class UnhandledException(Exception):
    pass


class RSSParser:
    def __init__(self, xml: str):
        try:
            self.root = ET.fromstring(xml)
        except ET.ParseError as e:
            raise UnhandledException(f"Error parsing XML: {e}")

    def parse_channel(self) -> List[str]:
        output = []
        channel = self.root.find("channel")
        if channel:
            title = channel.findtext('title')
            link = channel.findtext('link')
            # ... other channel information extraction
            output.extend([
                f"Feed: {title}",
                f"Link: {link}",
                # ... other channel information
            ])
        return output
