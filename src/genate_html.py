import os

from block_markdown import markdown_to_html_node


def extract_title(markdown: str):
    for line in markdown.split("\n"):
        if line.startswith("#"):
            return line.lstrip("#").lstrip()

    raise ValueError("no title found")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown=markdown)
    html_content = html_node.to_html()
    title = extract_title(markdown=markdown)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for file_name in os.listdir(dir_path_content):
        file_path = f"{dir_path_content}/{file_name}"
        dest_path = f"{dest_dir_path}/{file_name.replace('.md', '.html')}"

        if os.path.isfile(file_path) and file_path.endswith(".md"):
            generate_page(from_path=file_path, template_path=template_path, dest_path=dest_path)
        elif os.path.isdir(file_path):
            generate_pages_recursive(dir_path_content=file_path, template_path=template_path, dest_dir_path=dest_path)
