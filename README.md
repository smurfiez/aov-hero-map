# AoV ↔ 王者荣耀 Hero Map

A static site for a **王者荣耀 (Wangzhe Rongyao) player crossing over to Arena of Valor / 传说对决**.
Search any hero by AoV name or WZRY name, filter by role, see the counterpart + mapping type + tier.

## Files
- `index.html` — the site
- `tiers.html` — tier list with per-hero tier reasons
- `items.html` — full AoV item catalog (95 items) mapped to closest 王者荣耀 item
- `heroes.js` — the full roster (121 heroes): AoV name, 中文名, WZRY counterpart, role, lane, mapping type, note, tier, icon path
- `items.js` — the item catalog (generated): AoV name, stats, price, WZRY item, mapping type, reason, icon
- `images/` — drop portrait PNGs here (see below)

## Mapping types
- `direct` — same kit, renamed model (Violet→孙尚香, Hayate→马可波罗)
- `old` — matches a pre-rework WZRY hero (Lu Bu→曹操, Zanis→典韦, Taara→程咬金)
- `loose` — similar vibe, not a clone (Kil'Groth→老夫子-ish, Lindis→成吉思汗-ish)
- `original` — AoV / 传说对决-only, no WZRY equivalent (Teeri, Slimz, Florentino, Liliana…)

52 of 121 heroes are originals — that's why the site labels them clearly.

## Icons
`images/` ships with in-game hero portraits (120×120, from the official Garena AoV site) for most heroes,
plus splash art from the [Arena of Valor Wiki](https://arenaofvalor.fandom.com) for a few (Batman, Brunhilda,
Payna, Riktor, The Joker). `Vei` has no freely fetchable source and falls back to a letter placeholder.
Re-download or top up with: `python3 fetch_icons.py` (idempotent, skips files already present).
Cards show the hero's AoV name, 中文名 with pinyin underneath, and the WZRY counterpart.

## Skills (in the detail popup)
Clicking a card opens a detail modal that also shows the hero's 4 skills
(name, passive tag, mana, cooldown, type tags, description) from the
[Arena of Valor Wiki](https://arenaofvalor.fandom.com), plus 64px skill icons in `images/skills/`.
Data lives in `skills.js` (generated). Reproduce/refresh:

```
python3 fetch_skills.py        # wikitext → skills.json (121 heroes; Vei has no wiki page)
python3 fetch_skill_icons.py   # 64px icons → images/skills/ + skills_iconmap.json
python3 -c "import json; sk=json.load(open('skills.json')); imap=json.load(open('skills_iconmap.json')); \
  open('skills.js','w',encoding='utf-8').write('const SKILLS = ' + json.dumps({k:{'title':v['title'],'skills':[dict(s, icon=imap.get(s['icon_file'],'')) for s in v['skills']]} for k,v in sk.items()}, ensure_ascii=False) + ';\n')"
```

`fetch_skills.py` handles the wiki's several table formats (rowspan wikitables, gallery
tables, plain/`||`-separated cells, webp icons, `==Abilities==` headings). ~10 heroes have
template-only or prose wiki pages (Astrid, Lu Bu, Skud, Y'bneth, Heino, Dyadia, Zata, Marja,
Aya, Vei) — their popups simply show no skills.

## Items
`items.html` lists the full AoV item catalog (Beta 47.0, from the wiki's Items table) with the
closest 王者荣耀 item per entry. The WZRY mapping + one-line EN reason live in `ITEMS_MAP` in
`build.py`. Reproduce/refresh:

```
python3 fetch_items.py        # wiki Items table -> items.json (95 items)
python3 fetch_item_icons.py   # 64px icons -> images/items/ + items_iconmap.json
python3 build.py              # regenerates heroes.js + items.js (mapping + icons merged)
```

## Copyright note
This is a personal fan tool. Do NOT hotlink Tencent / 传说对决 / Honor of Kings official splash arts — those are copyrighted.
Use only art you have rights to (your own screenshots, officially released promo art, or keep the placeholders).

## Running it
Just open `index.html` in a browser. No server needed.
For best results serve the folder: `python -m http.server` then visit http://localhost:8000
