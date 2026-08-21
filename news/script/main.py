import file as file_manager
import gfm
import os, glob


with open("../template/article.html", "r") as file:
    article_template = file.read()

with open("../template/main_page.html", "r") as file:
    main_page_template = file.read()

paths = os.listdir("../articles")

for t in ["html", "svg", "css", "png", "jpg", "jpeg"]: # add other file types as needed
    for f in glob.glob(f"../*.{t}"):
       os.remove(f)


index = 0
cards = ""
for file_path in paths:
    index += 1
    output = file_manager.read("../articles/" + file_path)
    markdown = output["markdown"]

    html = gfm.convert_to_html(markdown)
    page = article_template.replace("[[code]]", html)
    with open(f"../{str(index).zfill(3)}.html", "w") as file:
        file.write(page)

    for path, image in output["images"].items():
        with open("../" + path.split("/")[-1], "wb") as file:
            file.write(image)

    data = output["data"]

    template = f"""
  <div class="card">
    <a href="{str(index).zfill(3)}.html">
    <img src="{data['cover']}" class="tinyPicture">
    <h3>{data['title']}</h3>
    <p>{data['date']}</p>
    </a>
  </div>
"""
    cards += template

with open("../update.html", "w") as file:
    file.write(main_page_template.replace("[[CODE]]", cards))
