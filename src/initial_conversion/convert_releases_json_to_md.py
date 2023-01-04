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
    base_dir, "feeds", "original", "releases.json")

# Parse JSON
with open(json_location, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Determine content location
content_location = os.path.join(base_dir, "content", Path(json_location).stem)

# Go through all items and convert each to an .md file
for json_item in json_data:
    # Compile .md file name
    slug = json_item['slug']
    date_time = datetime.strptime(
        json_item['date'], "%Y-%m-%dT%H:%M:%S.000Z")
    date_string = date_time.strftime("%Y-%m-%d")
    markdown_file_location = os.path.join(
        content_location, date_string + "-" + slug + ".md")

    print(f"Writing {markdown_file_location}")

    # Get thumbnail path
    thumbnail = "https://www.misantropolis.de" + \
        json_item['thumbnail'] if json_item['thumbnail'].startswith(
            "/") else json_item['thumbnail']

    # Compile .md content
    description = json_item['desc_l']

    # Replace <iframe>
    description = re.sub("<iframe(.*?)>(.*)</iframe>",
                          r"[iframe\1]", description)
    description = markdownify.markdownify(description)
    description = re.sub(
        "\[iframe(.*?)\]", r"<iframe\1></iframe>\n", description)

    # Compile YAML
    yaml_object = {
        'date': date_time,
        'artist': json_item['artist'],
        'title': json_item['title'],
        'summary': json_item['desc_s'],
        'main': json_item['main'],
        'type': json_item['type'],
        'format': json_item['format'],
        'label': json_item['label'],
        'nr': json_item['nr'],
        'raps': json_item['raps'] == True,
        'prod': json_item['prod'] == True,
        'cuts': json_item['cuts'] == True,
        'thumbnail': thumbnail,
        'download': json_item['download'],
        'stream': json_item['stream'],
        'shop': json_item['shop'],
        'lyrics': json_item['lyrics'],
        'numberOfTracks': int(json_item['numberOfTracks'] if json_item['numberOfTracks'] else 0)
    }

    content = '''---
{yaml}
---

{description}
'''.format(yaml=yaml.dump(yaml_object, allow_unicode=True, sort_keys=False), description=description.strip())

    # Write .md file
    with open(markdown_file_location, 'w+', encoding='utf-8') as markdown_file:
        markdown_file.write(content)
