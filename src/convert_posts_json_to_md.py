from datetime import datetime
import json
import markdownify
import os
from pathlib import Path
import re
import sys

# Get base directory
base_dir = Path(__file__).parent.parent.absolute()

# Get location of .json file
args = sys.argv[1:]
json_location = args[0] if args else os.path.join(
    base_dir, "feeds", "original", "posts.json")

# Parse JSON
with open(json_location, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Determine content location
content_location = os.path.join(base_dir, "content", Path(json_location).stem)

# Go through all items and convert each to an .md file
for json_item in json_data:
    # Compile .md file name
    title_clean = json_item['permalink'].split("/")[-2]
    date_string = (datetime.strptime(json_item['date_gmt'], "%Y-%m-%dT%H:%M:%S.000Z")).strftime("%Y-%m-%d")
    markdown_file_location = os.path.join(
        content_location, date_string + "-" + title_clean + ".md")

    print(f"Writing {markdown_file_location}")

    # Get image path
    image_path = "https://www.misantropolis.de" + json_item['image'] if json_item['image'].startswith("/") else json_item['image']
   
    # Compile .md content
    post_content = json_item['content']
    post_content = re.sub("<iframe(.*?)>(.*)</iframe>", r"[iframe\1]", post_content)
    post_content = markdownify.markdownify(post_content)
    post_content = re.sub("\[iframe(.*?)\]", r"<iframe\1></iframe>\n", post_content)

    content = '''---
title: "{title}"
category: {category}
tags: {tags}
image: {image}
---

{content}'''.format(title=str(json_item['title']).replace("\"", "\\\""), category=json_item['category'], image=image_path, tags=json_item['tags'], content=post_content)

    # Write .md file
    with open(markdown_file_location, "w+", encoding='utf-8') as markdown_file:
        markdown_file.write(content)