from datetime import datetime
from datetime import timedelta
import json
import markdown
import os
from pathlib import Path
import re
import yaml

type = "releases" # (This part differs from posts)

# Get base directory
base_dir = Path(__file__).parent.parent.absolute()

# Get location of .md files
markdown_directory_location = os.path.join(base_dir, "content", type)

# Get location of .json file
json_location = os.path.join(base_dir, "feeds", f"{type}.json")

# Initialize JSON
json_data = list()

# Go through all .md files and convert them into JSON
for markdown_file in sorted(Path(markdown_directory_location).glob("*.md"), reverse=True):
    print(f"Reading {markdown_file.absolute()}")

    # Get date from filename
    identifier = markdown_file.stem.split('-')
    
    # Get slug from filename
    slug = "-".join(identifier[3:])
    
    # Read and parse .md content
    with open(markdown_file, 'r', encoding='utf-8') as md_file:
        markdown_file_content = md_file.read()
    parsed_content = re.match("(?sm)^---(.*?)---(.+)", markdown_file_content)
    yaml_content = yaml.safe_load(parsed_content.group(1))

    # Append JSON object
    # (This part differs from posts)
    json_data.append({
        'date': datetime.strftime(yaml_content['date'], "%Y-%m-%dT%H:%M:%SZ"),
        'artist': yaml_content['artist'],
        'title': yaml_content['title'],
        'slug': slug,
        'desc_s': yaml_content['summary'],
        'desc_l': markdown.markdown(parsed_content.group(2)),
        'main': yaml_content['main'],
        'type': yaml_content['type'],
        'format': yaml_content['format'],
        'label': yaml_content['label'],
        'nr': yaml_content['nr'],
        'raps': yaml_content['raps'],
        'prod': yaml_content['prod'],
        'cuts': yaml_content['cuts'],
        'thumbnail': yaml_content['thumbnail'],
        'download': yaml_content['download'],
        'stream': yaml_content['stream'],
        'shop': yaml_content['shop'],
        'lyrics': yaml_content['lyrics'],
        'numberOfTracks': yaml_content['numberOfTracks']
    })

# Write .json
print(f"Dumping JSON to {json_location}")
json.dump(json_data, open(json_location, 'w+', encoding='utf-8'), indent=4)