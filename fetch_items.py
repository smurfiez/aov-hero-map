# -*- coding: utf-8 -*-
"""Fetch the AoV item catalog (EN) from the Arena of Valor Wiki into items.json.
Run: python3 fetch_items.py
Output: items.json [{name, type, level, price, desc, icon_file}]
"""
import html, json, re, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 Chrome/120"}
API = "https://arenaofvalor.fandom.com/api.php"

def api(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=30))

def clean(s):
    s = re.sub(r"\{\{[Mm][Pp] Icon 100\|[^}]*\}\}", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"[ \t]+", " ", s).strip()

def section(wt, start, end="== Special items =="):
    i = wt.index(start)
    j = wt.find(end, i + len(start))
    return wt[i:j if j > 0 else len(wt)]

def parse(wt):
    items = []
    cur_type, type_left = "", 0
    cur_lvl, lvl_left = "", 0
    for raw in section(wt, "==List of items==").split("|-")[1:]:
        row = re.sub(r'style="[^"]*"', "", raw)
        # type / level column rows appear as: | rowspan=N | Value
        for m in re.finditer(r'rowspan="?(\d+)"?[^|]*\|\s*([^|]+)', row):
            n, val = int(m.group(1)), m.group(2).strip()
            if "Lvl" in val:
                cur_lvl, lvl_left = val, n
            elif val.replace(" ", "").isalpha() or "/" in val:
                cur_type, type_left = val, n
        icon = re.search(r"\{\{[Mm][Pp] Icon 100\|([^|}]+)\|([^}]+)\}\}", row)
        if not icon:
            if type_left:
                type_left -= 1
            if lvl_left:
                lvl_left -= 1
            continue
        cells = [clean(c) for c in row.split("|")]
        price_i = next((i for i, c in enumerate(cells)
                        if re.fullmatch(r"\d{3,4}", c)), None)
        if price_i is None:
            continue
        items.append({
            "name": icon.group(2).strip(),
            "type": cur_type,
            "level": cur_lvl,
            "price": cells[price_i],
            "desc": " ".join(c for c in cells[price_i + 1:] if c),
            "icon_file": icon.group(1).strip().replace(" ", "_"),
        })
        if type_left:
            type_left -= 1
        if lvl_left:
            lvl_left -= 1
    return items

def main():
    d = api({"action": "parse", "page": "Items", "prop": "wikitext", "format": "json"})
    items = parse(d["parse"]["wikitext"]["*"])
    json.dump(items, open("items.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print("items:", len(items))
    for k, v in Counter(x["type"] for x in items).items():
        print(" ", k, v)

if __name__ == "__main__":
    main()
