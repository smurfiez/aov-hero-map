# -*- coding: utf-8 -*-
"""Fetch AoV hero skills (EN) from the Arena of Valor Wiki into skills.json.
Run: python3 fetch_skills.py [start end]  (default = all 121 heroes)
Output: skills.json {slug: {title, skills:[{name, passive, icon_file, desc, mana, types, cd}]}}
"""
import html, json, os, re, sys, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 Chrome/120"}
API = "https://arenaofvalor.fandom.com/api.php"
TITLES = {"Diao Chan": "Diaochan"}  # wiki page titles that differ from the hero name

def api(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=30))

def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

def skills_table(wt):
    m = re.search(r"^==\s*(?:Skills|Skillss|Abilities(?:\s*&\s*Stats)?)\s*==", wt, re.I | re.M)
    if not m:
        return ""
    nxt = re.search(r"^==\s", wt[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(wt)
    t = wt.find("{|", m.end(), end)
    if t < 0:
        return ""
    depth, j = 0, t
    while j < len(wt):
        if wt[j:j+2] == "{|":
            depth += 1
        elif wt[j:j+2] == "|}":
            depth -= 1
            if depth == 0:
                return wt[t:j+2]
        j += 1
    return wt[t:]

def parse_new_row(row):
    """New format: |<gallery>File:x.png</gallery>|Name\ndesc\nMana cost: N\n\nCooldown: C|Type"""
    gi = row.find("</gallery>")
    if gi < 0:
        return None
    icon_m = re.search(r"File:([^\n|]+?)(?:\.png|\.jpg|\.jpeg|\.webp|\.gif)", row[:gi])
    cells = row.split("|")
    try:
        gi_cell = next(i for i, c in enumerate(cells) if "</gallery>" in c)
        rest = [c for c in cells[gi_cell+1:] if c.strip()]
        name = clean(rest[0]).strip("*'")
    except (StopIteration, IndexError):
        return None
    body, mana, cd, typ = "", "", "", ""
    for c in rest[1:]:
        if "mana cost" in c.lower() and not body:
            body = c
        elif clean(c) and not typ and clean(c).replace(" ", "").isalpha():
            typ = clean(c)
    m = re.search(r"[Mm]ana cost:\s*(\d+)", body)
    if m:
        mana = m.group(1)
        body = body.replace(m.group(0), " ")
    m = re.search(r"C[oO]oldown:\s*([\d.]+)", body)
    if m:
        cd = m.group(1)
        body = body.replace(m.group(0), " ")
    return {"name": name, "passive": typ.lower() == "passive" or mana == "0",
            "icon_file": icon_m.group(1).strip() if icon_m else "",
            "desc": clean(body), "mana": mana,
            "types": [typ] if typ else [], "cd": cd}

BAD_NAMES = {"icon", "name", "description", "statistics", "cooldown", "damage",
             "base damage", "true damage", "magic damage", "physical damage",
             "attribute", "shield points", "armor increase", "attack damage increase",
             "mana cost", "energy cost", "lvl 1", "level", "current hp",
             "movement speed bonus", "damage bonus", "movement speed",
             "atk speed increase", "speed up", "atk increase", "shield"}
TYPE_LABELS = {"passive", "ultimate", "active", "skill 1", "skill 2", "skill 3"}

def parse_plain_row(row):
    """Formats C/D/E: plain cells, optional type column, [[File:x.png|...]] icon,
    cd/mana as plain cells or 'Cooldown: 6s' text. No ''' bold, no 'Mana cost:' line."""
    if row.strip().startswith("{|"):
        return None
    p = re.sub(r"\[\[([^\]]*)\]\]", lambda m: "[[" + m.group(1).replace("|", "\x01") + "]]", row)
    cells = [clean(c.replace("\x01", "|")) for c in p.split("|")]
    ico_i, icon = None, ""
    for i, c in enumerate(cells):
        m = re.search(r"File:([^\]|]+?)(?:\.png|\.jpg|\.jpeg|\.webp|\.gif)", c)
        if m:
            ico_i, icon = i, m.group(1).strip()
            break
    pre = row[:row.find("{")] if "{" in row else row
    if ico_i is None and len(re.findall(r"(?:\A|[\n|])\s*!", pre)) >= 2:
        return None  # header row
    typ = ""
    if ico_i is None:
        cands = [i for i, c in enumerate(cells)
                 if re.search(r"[A-Za-z]", c) and '"' not in c
                 and "colspan" not in c
                 and not c.strip().startswith(("{", "!", "}"))]
        if not cands:
            return None
        start = cands[0]
        first = cells[start].strip()
        if first.lower() in TYPE_LABELS:
            typ = first
            start = cands[1] if len(cands) > 1 else start + 1
    else:
        for c in cells[:ico_i]:
            t = c.strip()
            if t and t.replace(" ", "").isalpha() and '"' not in t:
                typ = t
                break
        ml = re.search(r"\]\]\s*([A-Za-z][A-Za-z ]{2,20})\s*$", cells[ico_i])
        if ml and not typ:
            typ = ml.group(1)
        start = ico_i + 1
        ico_extra = re.sub(r"\[\[File:[^\]]*\]\]", " ", cells[ico_i])
        mn = re.search(r"\[\[([^\]|]*)(?:\|([^\]|]*))?\]\]", ico_extra)
        inline_name = (mn.group(2) or mn.group(1)).strip() if mn else ""
    rest = []
    for c in cells[start:]:
        cs = c.strip()
        if not cs or cs[0] in "{}" or '"' in c:
            continue
        c = re.sub(r"\[\[File:[^\]]*\]\]", " ", c)
        m = re.search(r"\[\[([^\]|]*)(?:\|([^\]|]*))?\]\]", c)
        if m:
            c = m.group(2) or m.group(1)
        c = clean(c).strip("*'")
        if c:
            rest.append(c)
    if ico_i is not None and inline_name:
        rest.insert(0, inline_name)
    if not rest:
        return None
    name = rest[0]
    if (not re.search(r"[A-Za-z]", name) or name.lower() in BAD_NAMES
            or re.fullmatch(r"lvl \d+", name.lower()) or "://" in name):
        return None
    if rest[1:] and all(re.fullmatch(r"[\d.]+|Lvl \d+", c, re.I) for c in rest[1:]):
        return None  # stat row (damage/cooldown numbers), not a skill
    desc, cd, mana = "", "", ""
    for c in rest[1:]:
        if c.upper() in ("N/A", "N/A."):
            continue
        if re.fullmatch(r"[\d.]+", c):
            if not cd:
                cd = c
            elif not mana:
                mana = c
            continue
        m = re.fullmatch(r"([\d.]+)\s*(?:s|sec|seconds|seconds?)\b", c, re.I)
        if m:
            cd = m.group(1)
            continue
        cm = re.search(r"[Cc]ooldown:\s*([\d.]+)", c)
        if cm:
            cd = cm.group(1)
            continue
        if not desc and (len(c) >= 25 or c.endswith(".")):
            desc = c
        elif len(c) < 15 and c.replace(" ", "").isalpha():
            if c != typ:
                typ = (typ + " " + c).strip()
    desc = re.sub(r"'{2,}", " ", desc).strip()
    passive = typ.lower().startswith("passive") or (typ == "" and not cd and not mana and "{|" not in row)
    return {"name": name, "passive": passive, "icon_file": icon, "desc": desc,
            "mana": mana, "types": [typ] if typ else [], "cd": cd}

def parse_skills(wt):
    skills = []
    cur = None
    for row in skills_table(wt).split("|-"):
        if "mana cost" in row.lower():
            s = parse_new_row(row)
            if s and s["name"]:
                skills.append(s)
            continue
        nm1 = re.search(r"\[\[([^\]|]+)\|'''([^\']+?)'''\]\]", row)
        nm2 = re.search(r"\[\[File:[^\]]*\]\]\s*\|+\s*\[\[([^\]|]+?)\]\]", row)
        nm3 = re.search(r"'''(?:\[\[)?([^\]|'<>]+?)(?:\]\])?'''", row)
        icon_m = re.search(r"\[\[File:([^\]|]+?)(?:\.png|\.jpg|\.jpeg|\.webp|\.gif)(?:\|frameless)?", row)
        name = (nm1.group(2) if nm1 else nm2.group(1) if nm2 else nm3.group(1) if nm3 else "").strip()
        good = (bool(re.search(r"[A-Za-z]", name)) and name.lower() not in BAD_NAMES
                and not re.fullmatch(r"lvl?\.?\s*\d+", name.lower()) and "://" not in name)
        if good and icon_m and not row.strip().startswith("!"):
            icon = icon_m.group(1).strip() if icon_m else ""
            passive = ("50x50px" in row) and ("rowspan" not in row)
            cur = {"name": name, "passive": passive, "icon_file": icon,
                   "desc": "", "mana": "", "types": [], "cd": ""}
            skills.append(cur)
            tstart = 0
            d = re.search(r'colspan="[78]" \|(.+?)(?:\|<span style|\| rowspan|\|<br|\Z)', row, re.S)
            if d:
                cur["desc"] = clean(d.group(1))
                tstart = d.end()
            m = re.search(r"rowspan=\"4\" \|(\d+)", row)
            if m:
                cur["mana"] = m.group(1)
                tstart = max(tstart, m.end())
            for t in re.findall(r'<span style="color:#[0-9a-fA-F]+">([^<]+)</span>', row[tstart:]):
                t = clean(t)
                if t and t not in cur["types"]:
                    cur["types"].append(t)
            if "rowspan" not in row:
                for c in row.split("|"):
                    c = c.strip()
                    if re.fullmatch(r"[\d.]+", c):
                        if not cur["cd"]:
                            cur["cd"] = c
                        elif not cur["mana"]:
                            cur["mana"] = c
        else:
            s = parse_plain_row(row)
            if s:
                skills.append(s)
                cur = s
            elif cur is not None and "Cooldown" in row:
                nums = re.findall(r"\|(\d+(?:\.\d+)?)", row)
                if nums:
                    cur["cd"] = nums[0]
    return [s for s in skills if s["name"] or s["desc"]]

def slugify(name):
    return name.lower().replace("'", "").replace(" ", "")

def main():
    js = open("heroes.js", encoding="utf-8").read()
    heroes, _ = json.JSONDecoder().raw_decode(js[js.index("["):])
    a = sys.argv[1:]
    outpath = "skills.json"
    if "--out" in a:
        i = a.index("--out")
        outpath = a[i + 1]
        a = a[:i] + a[i + 2:]
    args = [x for x in a if x.isdigit()]
    heroes = heroes[int(args[0]):int(args[1])] if len(args) == 2 else heroes
    out = json.load(open(outpath, encoding="utf-8")) if os.path.exists(outpath) else {}
    ok = fail = 0
    fails = []
    for h in heroes:
        slug = slugify(h["aov_name"])
        force = "--force" in sys.argv[1:]
        if slug in out and out[slug].get("skills") and not force:
            ok += 1
            continue
        try:
            d = api({"action": "parse", "page": TITLES.get(h["aov_name"], h["aov_name"]),
                     "prop": "wikitext", "redirects": "1", "format": "json"})
            pg = d.get("parse")
            if not pg:
                raise RuntimeError("no wiki page")
            wt = pg["wikitext"]["*"]
            skills = parse_skills(wt)
            out[slug] = {"title": pg.get("title", h["aov_name"]), "skills": skills}
            ok += 1
        except Exception as e:
            fail += 1
            fails.append((h["aov_name"], str(e)))
    json.dump(out, open(outpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for f in fails:
        print("FAIL", f[0], f[1])
    print("skills done: ok=%d fail=%d out=%s" % (ok, fail, outpath))

if __name__ == "__main__":
    main()
