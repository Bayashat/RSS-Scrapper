# RSS Reader

A pure command-line RSS reader written in pure Python.

## Overview

RSS Reader is a lightweight tool for parsing and displaying information from RSS feeds. It can handle both plain text and JSON output formats.

## Features

- Parse XML-formatted RSS feeds
- Display information about RSS channels and items
- Format output as plain text or JSON

## Installation

```bash
pip install -r requirements.txt
```

## Usage
```bash
cd rss_reader
python main.py [source] [--json] [--limit LIMIT]
```

## Options
```
`source`: RSS URL
`--json`: Print result as JSON in stdout
`--limit LIMIT`: Limit the number of news topics
```

## Examples
1. Parse an RSS feed and display information in plain text:
```bash
python main.py https://example.com/rss-feed
```


2. Parse an RSS feed and display information in JSON format:

```bash
python main.py https://example.com/rss-feed --json
```

3. Limit the number of displayed news topics:

```bash
python main.py https://example.com/rss-feed --limit 5
```