import xml.etree.ElementTree as ET
import json as JSON
from typing import List, Optional


class UnhandledException(Exception):
    pass


def extract_channel_info(channel, json_format=False):
    if json_format == False:
        info = {
            "Feed": channel.findtext('title'),
            "Link": channel.findtext('link'),
            "Last Build Date": channel.findtext('lastBuildDate'),
            "Publish Date": channel.findtext('pubDate'),
            "Language": channel.findtext('language'),
            "Categories": [category.text for category in channel.findall('category')],
            "Editor": channel.findtext('managingEditor'),
            "Description": channel.findtext('description')
        }
        
        # Filter out elements with a value of None
        info = {key: value for key, value in info.items() if (value is not None and value != [])}
        
        # Convert categories to string
        categories = info.get("Categories")
        if categories is not None:
            info["Categories"] = ",".join(categories)
    
    else:
        info = {
            "title": channel.findtext('title'),
            "link": channel.findtext('link'),
            "lastBuildDate": channel.findtext('lastBuildDate'),
            "pubDate": channel.findtext('pubDate'),
            "language": channel.findtext('language'),
            "category": [category.text for category in channel.findall('category')],
            "managingEditor": channel.findtext('managingEditor'),
            "description": channel.findtext('description')
        }
        
    # Filter out elements with a value of None
    info = {key: value for key, value in info.items() if (value is not None and value != [])}
    
    return info

def extract_plain_text_item_info(item):
    item_info = {
        "Title": item.findtext('title'),
        "Author": item.findtext('author'),
        "Published": item.findtext('pubDate'),
        "Link": item.findtext('link'),
        "Category": item.findtext('category'),
        "Description": item.findtext('description')
    }

    # Filter out items with a value of None
    item_info = {key: value for key, value in item_info.items() if value is not None}

    return item_info

def extract_json_item_info(item):
    item_info = {
        "title": item.findtext('title'),
        "author": item.findtext('author'),
        "pubDate": item.findtext('pubDate'),
        "link": item.findtext('link'),
        "category": [category.text for category in item.findall('category')],
        "description": item.findtext('description')
    }
    
    # Filter out items with a value of None
    item_info = {key: value for key, value in item_info.items() if value is not None}
    
    return item_info

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
        channel_info = extract_channel_info(channel, json_format=json)
        
    # Extract information from <item> elements
            
    items = root.findall(".//item")
    
    if limit:
            items = items[:limit]
            
    # Choose the appropriate extraction function based on the json parameter
    extract_item_info = extract_json_item_info if json else extract_plain_text_item_info
    
    item_list = [extract_item_info(item) for item in items]


    if json:
        # Don't add items if not provided
        if not item_list:
            data = channel_info
        else:
            data = {
                **channel_info,
                "items": item_list if item_list else []
            }
        
        # Convert the dictionary into a JSON string
        json_data = JSON.dumps(data, ensure_ascii=False)

        # Split the string into lines for the final result
        return json_data.splitlines()

        
    output = dict(channel_info, **{"items": item_list})

    # Convert the list of dictionaries into a formatted string
    res = []
    for key, value in output.items():
        if key == "items":
            res.append("\n")
            for item in value:
                for k, v in item.items():
                    if k == "Description":
                        res.append(f"\n{v}")
                        continue
                    res.append(f"{k}: {v}")
                res.append("\n")
        else:
            res.append(f"{key}: {value}")
            
    return res
