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
                "Description": self.channel.findtext('description'),
                # ... other channel information
            }

    def parse_items_stout(self, limit: int) -> List[str]:
        output = []
        self.items = self.root.findall(".//item")
        self.limit = limit
        # Limit news topics if this parameter provided
        if limit:
            self.items = self.items[:limit]
  
        for item in self.items:
            item_dict = {
                "Title": item.findtext('title'),
                "Author": item.findtext('author'),
                "Published": item.findtext('pubDate'),
                "Link": item.findtext('link'),
                "Category": item.findtext('category'),
                "Description": item.findtext('description')
            }

            # Filter out items with a value of None
            item_dict = {key: value for key, value in item_dict.items() if value is not None}   
            
            output.append(item_dict)
                
        return output
    
    def parse_items_json(self, limit: int) -> List[str]:
        output = []
        self.items = self.root.findall(".//item")
        self.limit = limit
        # Limit news topics if this parameter provided
        if limit:
            self.items = self.items[:limit]
  
        for item in self.items:
            item_dict = {
                "title": item.findtext('title'),
                "author": item.findtext('author'),
                "pubDate": item.findtext('pubDate'),
                "link": item.findtext('link'),
                "category": item.findtext('category'),
                "description": item.findtext('description')
            }
            
            # Filter out items with a value of None
            item_dict = {key: value for key, value in item_dict.items() if value is not None}
            output.append(item_dict)
                
        return output
    
    def to_json(self, limit: int) -> str:
        channel_data: Optional[dict] = self.parse_channel()
        items_data: List[dict] = self.parse_items_json(limit)
        
        data = {
            "title": channel_data.get("Feed"),
            "link": channel_data.get("Link"),
            "description": channel_data.get("Description"),
            "items": items_data
        }
        return json.dumps(data, indent=2)
    