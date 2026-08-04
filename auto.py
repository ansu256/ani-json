import json
import requests
from pathlib import Path

urls = [
    "https://raw.githubusercontent.com/MajoSissi/animeko-source/main/dist/all.json",
    "https://raw.githubusercontent.com/Nier4ever/ani-sub/main/css.json",
    "https://raw.githubusercontent.com/cxay666/ani-yuan/main/ani-yuan.json",
    "https://raw.githubusercontent.com/ashurajo/Animeko/refs/heads/main/css1.json",
    "https://sub.creamycake.org/v1/css1.json",
    "https://masofod.github.io/anibt.json",
    "https://sub.creamycake.org/v1/bt1.json",
]


all_sources = []

for url in urls:
    try:
        print("读取:", url)

        r = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        r.raise_for_status()
        data = r.json()

        if "exportedMediaSourceDataList" in data:
            sources = data["exportedMediaSourceDataList"]["mediaSources"]

        elif "mediaSources" in data:
            sources = data["mediaSources"]

        else:
            print("未知格式:", url)
            continue

        all_sources.extend(sources)

    except Exception as e:
        print("失败:", url, e)


original = len(all_sources)


seen = set()
unique = []

for item in all_sources:

    key = json.dumps(
        item,
        ensure_ascii=False,
        sort_keys=True
    )

    if key not in seen:
        seen.add(key)
        unique.append(item)



output = {
    "exportedMediaSourceDataList": {
        "mediaSources": unique
    }
}


Path("animeko-merged.json").write_text(
    json.dumps(
        output,
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)


print("================")
print("原始:", original)
print("去重:", len(unique))
print("重复:", original-len(unique))