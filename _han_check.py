# -*- coding: utf-8 -*-
# Scan foreign language packs for stray CHINESE inside value strings.
# Japanese (lang.ja.js) uses the same CJK range, so we skip it deliberately
# (its Han chars are legit Japanese kanji, not Chinese leaks).
import re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
val_re = re.compile(r'^\s*"([a-z][a-zA-Z0-9_.]*)"\s*:\s*"(.*)",?\s*$')
han_re = re.compile(r'[\u4e00-\u9fff]')          # CJK ideographs (covers CN + JP)
kana_re = re.compile(r'[\u3040-\u30ff]')          # hiragana + katakana => Japanese line

print("Scanning foreign packs (excluding lang.ja.js) for stray Chinese...")
found = False
for lf in sorted(HERE.glob("lang.*.js")):
    if lf.name in ("lang.en.js", "lang.ja.js"):
        continue
    for i, line in enumerate(lf.read_text(encoding="utf-8").splitlines(), 1):
        m = val_re.match(line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if key == "feat.i18n.what0d":   # intentional language list
            continue
        if kana_re.search(val):         # Japanese text — not a Chinese leak
            continue
        if han_re.search(val):
            found = True
            print(f"  LEAK {lf.name}:{i}  key={key}\n        val={val}")
if not found:
    print("  (none) — no stray Chinese in any non-Japanese foreign pack value ✓")
