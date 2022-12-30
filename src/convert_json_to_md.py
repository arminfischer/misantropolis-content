import json
import markdownify
import os
from pathlib import Path
import sys

# Get base directory
base_dir = Path(__file__).parent.parent.absolute()

# Get location of .json file
args = sys.argv[1:]
json_location = args[0] if args else os.path.join(
    base_dir, "feeds", "posts.json")

# Parse JSON
with open(json_location, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Determine content location
content_location = os.path.join(base_dir, "content", Path(json_location).stem)

# Go through all items and convert each to an .md file
for json_item in json_data[0:1]:
    markdown_file_location = os.path.join(
        content_location, json_item['title'] + ".md")

    content = '''---
title: {title}
category: {category}
permalink: {permalink}
tags: {tags}
date: {date}
image: {image}
---

{content}
    '''.format(title=json_item['title'], category=json_item['category'], permalink=json_item['title'], date=json_item['date_gmt'], image=json_item['image'], tags=json_item['tags'], content=markdownify.markdownify(json_item['content']))

    with open(markdown_file_location, "w+") as markdown_file:
        markdown_file.write(content)
