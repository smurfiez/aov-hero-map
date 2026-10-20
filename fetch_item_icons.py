# -*- coding: utf-8 -*-
"""Fetch item icons (64px) from the Arena of Valor Wiki into images/items/.
Run: python3 fetch_item_icons.py
Writes images/items/<slug>.<ext> and items_iconmap.json {icon_file: "images/items/<slug>.<ext>"}.
Idempotent — skips icons already present.
"""
import json, os, re, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 Chrome/120", "Referer": "https://arenaofvalor.fandom.com/"}
API = "https://arenaofvalor.fandom.com/api.php"

def api(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=30))

def norm(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")

def main():
    items = json.load(open("items.json", encoding="utf-8"))
    icons = sorted({x["icon_file"] for x in items if x.get("icon_file")})
    os.makedirs("images/items", exist_ok=True)
    imap = json.load(open("items_iconmap.json", encoding="utf-8")) if os.path.exists("items_iconmap.json") else {}
    todo = [i for i in icons if i not in imap]
    print("icons: %d total, %d to fetch" % (len(icons), len(todo)))

    def query_titles(titles):
        out = {}
        d = api({"action": "query", "titles": "|".join(titles),
                 "prop": "imageinfo", "iiprop": "url", "format": "json", "redirects": "1"})
        for pg in d.get("query", {}).get("pages", {}).values():
            ii = pg.get("imageinfo", [{}])[0]
            if ii.get("url"):
                t = pg["title"][5:]
                for e in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
                    if t.lower().endswith(e):
                        t = t[:-len(e)]
                out[norm(t)] = ii["url"]
        return out

    def resolve(batch):
        out = {}
        for i in range(0, len(batch), 15):
            chunk = batch[i:i + 15]
            try:
                out.update(query_titles(chunk))
            except Exception:
                for t in chunk:
                    try:
                        out.update(query_titles([t]))
                    except Exception:
                        pass
        return out

    todo_q = [urllib.parse.unquote(f) for f in todo]
    noext = lambda f: re.sub(r"\.(png|jpe?g|webp|gif)$", "", f, flags=re.I)
    urls = resolve(["File:" + f for f in todo_q])
    urls.update(resolve(["File:" + f.replace(".png", ".jpg") for f in todo_q
                         if norm(noext(f)) not in urls and f.endswith(".png")]))

    ok = fail = 0
    for f, fq in zip(todo, todo_q):
        u = urls.get(norm(noext(fq)))
        if not u:
            print("FAIL", f, "no image found")
            fail += 1
            continue
        u = u.replace("/revision/latest", "/revision/latest/scale-to-width-down/64")
        base = norm(f)
        ext = ".png" if ".png" in u else ".jpg"
        path = "images/items/" + base + ext
        try:
            req = urllib.request.Request(u, headers=UA)
            data = urllib.request.urlopen(req, timeout=30).read()
            open(path, "wb").write(data)
            imap[f] = path
            ok += 1
        except Exception as e:
            print("FAIL", f, e)
            fail += 1
        if ok % 20 == 0 and ok:
            print("  %d..." % ok)
    json.dump(imap, open("items_iconmap.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("item icons done: ok=%d fail=%d" % (ok, fail))

if __name__ == "__main__":
    main()
