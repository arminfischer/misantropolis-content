from datetime import datetime
from datetime import timedelta
import io
import json
import markdown
import os
from pathlib import Path
import re
import yaml

type = "posts"

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
    json_data.append({
        'title': yaml_content['title'],
        'permalink': datetime.strftime(yaml_content['date'], "/%Y/%m/") + slug,
        'date_gmt': datetime.strftime(yaml_content['date'], "%Y-%m-%dT%H:%M:%SZ"),
        'category': yaml_content['category'],
        'tags': yaml_content['tags'],
        'content': markdown.markdown(parsed_content.group(2)),
        'image': yaml_content['image'],
    })

# Write .json
print(f"Dumping JSON to {json_location}")
json.dump(json_data, open(json_location, 'w+', encoding='utf-8'))