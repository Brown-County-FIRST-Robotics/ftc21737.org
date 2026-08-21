import file

# this is for making news articles

markdown = input("markdown: ")
title = input("title: ")
cover = input("cover: ")
date = input("date: ")

images = []
while True:
    image = input("enter image or 'stop': ")
    if image == "stop":
        break
    else:
        images.append(image)


file.write(f"{title}.page", title, date, cover, markdown, images)
