import os


def rmdir_recursive(path: str):
    if os.path.isdir(path):
        print(f"Removing folder: {path}")
        for file_name in os.listdir(path):
            file_path = f"{path}/{file_name}"
            rmdir_recursive(file_path)
        os.rmdir(path)
    elif os.path.isfile(path):
        print(f"Removing file: {path}")
        os.unlink(path)
    else:
        raise RuntimeError(f"Invalid path: {path}")


def copy_directory(source_directory: str, destination_directory: str):
    if os.path.exists(destination_directory):
        rmdir_recursive(destination_directory)

    os.mkdir(destination_directory)

    for file_name in os.listdir(source_directory):
        source_path = f"{source_directory}/{file_name}"
        destination_path = f"{destination_directory}/{file_name}"

        print(f"Copying {source_path} into {destination_path}")

        if os.path.isfile(source_path):
            with (
                open(source_path, "rb") as source_file,
                open(destination_path, "wb") as destination_file,
            ):
                destination_file.write(source_file.read())
        elif os.path.isdir(source_path):
            copy_directory(source_path, destination_path)


if __name__ == "__main__":
    copy_directory("static", "public")
