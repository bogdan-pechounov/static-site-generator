import os

from genate_html import generate_pages_recursive
from utils import copy_directory, rmdir_recursive


def main():
    source_directory = "./static"
    destination_directory = "./docs"

    print("Deleting public directory....")
    if os.path.exists(destination_directory):
        rmdir_recursive(destination_directory)

    print("Copying static files to public directory...")
    copy_directory(source_directory=source_directory, destination_directory=destination_directory)

    print("Generating content...")
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path=destination_directory,
    )


if __name__ == "__main__":
    main()
