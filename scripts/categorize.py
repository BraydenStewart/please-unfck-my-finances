"""Fill the category column of ledger CSVs using config/categories.json. Usage: categorize.py file.csv [--report]"""
import csv, json, re, sys, collections

path = sys.argv[1]
rules = [(r["c"], re.compile(r["re"], re.I), r.get("sign")) for r in json.load(open("config/categories.json"))["rules"]]
rows = list(csv.DictReader(open(path, encoding="utf-8")))
tot = collections.defaultdict(lambda: [0, 0.0]); unc = collections.Counter()
for r in rows:
    amt = float(r["amount"]); sign = "in" if amt > 0 else "out"; r["category"] = "uncategorized"
    for c, rx, s in rules:
        if (s is None or s == sign) and rx.search(r["description"]):
            r["category"] = c; break
    t = tot[r["category"]]; t[0] += 1; t[1] += amt
    if r["category"] == "uncategorized": unc[re.sub(r"[\d#*].*$", "", r["description"]).strip()[:30]] += 1
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["date", "account", "description", "amount", "category"]); w.writeheader(); w.writerows(rows)
for c, (n, a) in sorted(tot.items(), key=lambda x: x[1][1]): print(f"{c:22s}{n:5d} {a:11.2f}")
print("top uncategorized:", unc.most_common(25))
