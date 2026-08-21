import zipfile
import json
import io


def read(file_path):
    output = {"images": {}}
    with zipfile.ZipFile(file_path, "r") as zfile:
        with zfile.open("page.md", "r") as file:
            output["markdown"] = file.read().decode()

        with zfile.open("data.json", "r") as file:
            output["data"] = json.load(file)

        for path in zfile.namelist():
            if path.startswith("images/"):
                with zfile.open(path, "r") as file:
                    output["images"][path] = file.read()

    return output


def write(file_path, title, date, cover, markdown_file, images_paths):
    with zipfile.ZipFile(file_path, "w") as zfile:
        with open(markdown_file, "r") as file:
            zfile.writestr("page.md", file.read())

        for image in images_paths:
            with open(f"{image}", "rb") as file:
                zfile.writestr(image, file.read())

        with open(cover, "rb") as file:
            zfile.writestr(f"images/{cover}", file.read())

        data = {
            "title": title,
            "date": date,
            "cover": cover,
        }
        string_file = io.StringIO()
        json.dump(data, string_file, indent=4)
        json_string = string_file.getvalue()
        zfile.writestr("data.json", json_string)
