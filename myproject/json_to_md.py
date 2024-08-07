import json
import os

def json_to_markdown(json_file, markdown_file):
    # استفاده از مسیر مطلق برای فایل JSON
    json_path = os.path.abspath(json_file)
    
    with open(json_path, 'r') as f:
        data = json.load(f)

    markdown_content = f"# {data[0]['title']}\n\n"
    for section in data[0]['content']:
        markdown_content += f"## {section['section']}\n\n{section['content']}\n\n"

    with open(markdown_file, 'w') as f:
        f.write(markdown_content)

json_to_markdown('output.json', 'output.md')

print(f"Markdown file has been created: {os.path.abspath('output.md')}")