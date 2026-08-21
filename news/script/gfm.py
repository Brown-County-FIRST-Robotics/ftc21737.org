import pycmarkgfm
from bs4 import BeautifulSoup

gfm = """
# testing markdown 2.0
## subheader
### sub subheader

![](sponsors.png)

- [x] task 1
- [ ] task 2
- [x] other

you can write text and format it *like this* or __this__ or even `like this`


> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.

```
git status
git add
git commit
```

``` python
data = input("enter data:")
with open("file.txt", "w") as file:
    file.write(data)

print("File saved.")
```

1. item 1
2. item 2
3. item 3

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
"""

def convert_to_html(gfm):
    html = pycmarkgfm.gfm_to_html(gfm)

    soup = BeautifulSoup(html, "html.parser")

    for bq in soup.find_all("blockquote"):
        p = bq.find("p")
        if not p:
            continue

        text = p.get_text().strip()
        if not text.startswith("[!"):
            continue

        first_line_end = text.find("\n")
        label_line = text if first_line_end == -1 else text[:first_line_end]
        content = "" if first_line_end == -1 else text[first_line_end + 1:].strip()

        label = label_line[2:-1].lower()

        div = soup.new_tag("div", **{"class": f"callout {label}"})

        title = soup.new_tag("div", **{"class": "callout-title"})
        title.string = label.upper()

        body = soup.new_tag("div", **{"class": "callout-body"})
        body.string = content

        div.append(title)
        div.append(body)

        bq.replace_with(div)

    return str(soup)
