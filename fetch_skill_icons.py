# -*- coding: utf-8 -*-
"""Fetch skill icons (64px) from the Arena of Valor Wiki into images/skills/.
Run: python3 fetch_skill_icons.py [start end]  (default = all unique skill icons)
Writes images/skills/<slug>.png and skills_iconmap.json {"icon_file": "images/skills/<slug>.png"}.
"""
import json, os, re, subprocess, sys, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 Chrome/120", "Referer": "https://arenaofvalor.fandom.com/"}
API = "https://arenaofvalor.fandom.com/api.php"

def api(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=30))

def norm(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")

def main():
    sk = json.load(open("skills.json", encoding="utf-8"))
    icons = sorted({s["icon_file"] for h in sk.values() for s in h["skills"] if s.get("icon_file")})
    args = [a for a in sys.argv[1:] if a.isdigit()]
    icons = icons[int(args[0]):int(args[1])] if len(args) == 2 else icons
    os.makedirs("images/skills", exist_ok=True)
    imap = json.load(open("skills_iconmap.json", encoding="utf-8")) if os.path.exists("skills_iconmap.json") else {}
    todo = [i for i in icons if i not in imap]

    # resolve File titles to real URLs (try .png then .jpg), batched
    def query_titles(titles):
        out = {}
        for pg in api({"action": "query", "titles": "|".join(titles),
                       "prop": "imageinfo", "iiprop": "url", "format": "json",
                       "redirects": "1"}).get("query", {}).get("pages", {}).values():
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
            except Exception:  # long-URL 400 fallback: one by one
                for t in chunk:
                    try:
                        out.update(query_titles([t]))
                    except Exception:
                        pass
        return out

    todo_q = [urllib.parse.unquote(f) for f in todo]
    urls = resolve(["File:" + f + ".png" for f in todo_q])
    urls.update(resolve(["File:" + f + ".jpg" for f in todo_q if norm(f) not in urls]))

    ok = fail = 0
    for f, fq in zip(todo, todo_q):
        u = urls.get(norm(fq))
        if not u:
            print("FAIL", f, "no image found")
            fail += 1
            continue
        u = u.replace("/revision/latest", "/revision/latest/scale-to-width-down/64")
        base = norm(f)
        ext = ".png" if ".png" in u else ".jpg"
        path = "images/skills/" + base + ext
        try:
            req = urllib.request.Request(u, headers=UA)
            data = urllib.request.urlopen(req, timeout=30).read()
        except Exception:
            data = subprocess.run(["curl", "-sf", "--max-time", "30",
                                   "-A", "Mozilla/5.0 Chrome/120", "-e", UA["Referer"], u],
                                  capture_output=True, timeout=40).stdout
        if len(data) < 200:
            print("FAIL", f, "too small")
            fail += 1
            continue
        open(path, "wb").write(data)
        imap[f] = path
        ok += 1
    json.dump(imap, open("skills_iconmap.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("skill icons done: ok=%d fail=%d mapped=%d" % (ok, fail, len(imap)))

if __name__ == "__main__":
    main()
