# -*- coding: utf-8 -*-
import re, pathlib, glob

HERE = pathlib.Path(__file__).resolve().parent

html_files = [HERE / "index.html"] + sorted(HERE.glob("feature-*.html"))
lang_files = sorted(HERE.glob("lang.*.js"))

# 1) collect keys defined in each lang pack
pack_keys = {}
key_re = re.compile(r'"([a-z][a-zA-Z0-9_.]*)"\s*:')
for lf in lang_files:
    txt = lf.read_text(encoding="utf-8")
    keys = set(key_re.findall(txt))
    pack_keys[lf.name] = keys

# 2) collect keys used in HTML
used = set()
attr_re = re.compile(r'data-i18n-attr="([^"]+)"')
ih_re = re.compile(r'data-i18n(?:-html)?="([^"]+)"')
for hf in html_files:
    txt = hf.read_text(encoding="utf-8")
    for m in ih_re.finditer(txt):
        used.add(m.group(1))
    for m in attr_re.finditer(txt):
        for part in m.group(1).split(","):
            if ":" in part:
                used.add(part.split(":", 1)[1].strip())

print(f"HTML files scanned: {len(html_files)}")
print(f"Lang packs: {[f.name for f in lang_files]}")
print(f"Distinct i18n keys used in HTML: {len(used)}")

# 3) baseline = en pack (fallback). Anything missing in en => non-zh shows Chinese (bad)
en_keys = pack_keys.get("lang.en.js", set())
missing_en = sorted(k for k in used if k not in en_keys)
print("\n[CRITICAL] keys used in HTML but MISSING in lang.en.js (fallback):")
if missing_en:
    for k in missing_en:
        print("  -", k)
else:
    print("  (none) — all used keys have an en fallback ✓")

# 4) coverage across all 9 foreign packs (quality)
foreign = [f for f in lang_files if f.name != "lang.en.js"]
print("\n[QUALITY] keys missing in some foreign pack (will fall back to en):")
any_missing = False
for k in sorted(used):
    miss = [f.name for f in foreign if k not in pack_keys.get(f.name, set())]
    if miss:
        any_missing = True
        print(f"  - {k}: missing in {miss}")
if not any_missing:
    print("  (none) — full coverage across all 10 packs ✓")
