from datetime import datetime
import json
import markdownify
import os
from pathlib import Path
import re
import sys
import yaml

# Get base directory
base_dir = Path(__file__).parent.parent.parent.absolute()

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
    date_time = datetime.strptime(
        json_item['date_gmt'], "%Y-%m-%dT%H:%M:%S.000Z")
    date_string = date_time.strftime("%Y-%m-%d")
    markdown_file_location = os.path.join(
        content_location, date_string + "-" + title_clean + ".md")

    print(f"Writing {markdown_file_location}")

    # Get image path
    image_path = "https://www.misantropolis.de" + \
        json_item['image'] if json_item['image'].startswith(
            "/") else json_item['image']

    # Compile .md content
    post_content = json_item['content']

    # Replace <iframe>
    post_content = re.sub("<iframe(.*?)>(.*)</iframe>",
                          r"[iframe\1]", post_content)
    post_content = markdownify.markdownify(post_content)
    post_content = re.sub(
        "\[iframe(.*?)\]", r"<iframe\1></iframe>\n", post_content)

    # Compile YAML
    yaml_object = {
        'title': str(json_item['title']).replace("\"", "\\\""),
        'date': date_time,
        'category': json_item['category'],
        'tags': json_item['tags'] if json_item['tags'] else [],
        'image': image_path
    }

    content = '''---
{yaml}
---

{content}
'''.format(yaml=yaml.dump(yaml_object, allow_unicode=True, sort_keys=False), content=post_content.strip())

    # Write .md file
    with open(markdown_file_location, "w+", encoding='utf-8') as markdown_file:
        markdown_file.write(content)
