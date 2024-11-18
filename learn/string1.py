urls = [
    "/truyen/abc11",
    "/truyen/abc12",
    "/truyen/abc13",
    "http://truyen/abc14",
    "/truyen/abc15",
    "http://truyen/abc16"
]

for index, url in enumerate(urls):
    if "http" not in url:
        url = "https://truyenwikidich.net" + url
    print(f"{url}: {index+1}/{len(urls)}({(index+1)*100/len(urls):.2f}%)")