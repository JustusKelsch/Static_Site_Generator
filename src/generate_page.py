import os
from pathlib import Path
from block_markdown import markdown_to_blocks, markdown_to_html_node


def exctract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.count("#") == 1:
            return block[2:]
    
    raise ValueError("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as md:
        markdown = md.read()

    with open(template_path) as temp:
        template = temp.read()

    html = markdown_to_html_node(markdown).to_html()
    title = exctract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)


    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    file = open(f"{dest_path}", "w")
    file.write(template)
    file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
