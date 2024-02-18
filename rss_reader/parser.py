import xml.etree.ElementTree as ET
import json
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
        self.channel = self.root.find("channel")
        if self.channel:
            return {
                "Feed": self.channel.findtext('title'),
                "Link": self.channel.findtext('link'),
                # ... other channel information
            }

    def parse_items(self) -> List[str]:
        output = []
        self.items = self.root.findall(".//item")
        for item in self.items:
            title = item.findtext('title')
            author = item.findtext('author')
            pub_date = item.findtext('pubDate')
            link = item.findtext('link')
            category = item.findtext('category')
            description = item.findtext('description')

            output.append({
                "Title": title,
                "Author": author,
                "Published": pub_date,
                "Link": link,
                "Category": category,
                "Description": description
            })
                
        return output
    
    def to_json(self) -> str:
        channel_data = self.parse_channel()
        items_data = self.parse_items()
        
        data = {
            "Feed": channel_data["Feed"],
            "Link": channel_data["Link"],
            # Other channel information
            
            "Title": items_data["Title"],
            "Author": items_data["Author"],
            "Published": items_data["Published"],
            "Link": items_data["Link"],
            "Category": items_data["Category"],
            "Description": items_data["Description"]
        }
        
        return json.dumps(data, indent=2)