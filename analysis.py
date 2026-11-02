"""Analysis for the PK Hosting domain pricing comparison.

Reads domain_pricing.csv and prints every summary statistic used in
report.md and index.html, so all report numbers are reproducible from
the CSV. No currency conversion is done: USD and PKR rows are compared
only within their own currency group. .pk and .com.pk prices are per
2-year term and are compared only against other .pk/.com.pk prices.
Run: python3 analysis.py
"""
import csv
from collections import defaultdict

ROWS = []
with open("domain_pricing.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        for k in ("registration_price", "renewal_price", "renewal_jump_pct"):
            row[k] = float(row[k]) if row[k] not in ("", None) else None
        ROWS.append(row)

priced = [r for r in ROWS if r["registration_price"] is not None]
print(f"Total rows: {len(ROWS)}")
print(f"Priced rows: {len(priced)}")
print(f"NOT FOUND rows: {len(ROWS) - len(priced)}")
print(f"Registrars: {len(set(r['registrar'] for r in ROWS))}")
print(f"Extensions: {len(set(r['extension'] for r in ROWS))}")
print()

print("Cheapest registration and renewal per extension (within currency):")
by_ext_cur = defaultdict(list)
for r in priced:
    by_ext_cur[(r["extension"], r["currency"])].append(r)
for (ext, cur), rows in sorted(by_ext_cur.items()):
    cheapest_reg = min(rows, key=lambda r: r["registration_price"])
    cheapest_ren = min(rows, key=lambda r: r["renewal_price"])
    print(f"  {ext} [{cur}]: cheapest registration: {cheapest_reg['registrar']} "
          f"{cheapest_reg['registration_price']}; cheapest renewal: "
          f"{cheapest_ren['registrar']} {cheapest_ren['renewal_price']}")
print()

print("Biggest renewal jumps (percent, priced rows only):")
jumps = sorted(
    (r for r in priced if r["renewal_jump_pct"] is not None),
    key=lambda r: r["renewal_jump_pct"], reverse=True)
for r in jumps[:10]:
    print(f"  {r['registrar']} {r['extension']}: "
          f"{r['registration_price']} -> {r['renewal_price']} "
          f"({r['renewal_jump_pct']:+.1f}%)")
print()

print("Flat or falling renewals (jump <= 0 percent, excluding the Cloudflare")
print(".ai 2-year term artifact):")
for r in priced:
    if r["renewal_jump_pct"] is not None and r["renewal_jump_pct"] <= 0:
        if r["registrar"] == "Cloudflare" and r["extension"] == ".ai":
            continue
        print(f"  {r['registrar']} {r['extension']}: "
              f"{r['registration_price']} -> {r['renewal_price']} "
              f"({r['renewal_jump_pct']:+.1f}%)")
print()

print("PK Hosting vs PK Domain (PKR, same extensions):")
for ext in (".com", ".pk", ".com.pk"):
    ph = next(r for r in priced if r["registrar"] == "PK Hosting" and r["extension"] == ext)
    pd = next(r for r in priced if r["registrar"] == "PK Domain" and r["extension"] == ext)
    diff = ph["registration_price"] - pd["registration_price"]
    pct = diff / pd["registration_price"] * 100
    print(f"  {ext}: PK Hosting {ph['registration_price']} vs PK Domain "
          f"{pd['registration_price']} (difference {diff:+.0f}, {pct:+.1f}%)")
print()

print("PK Hosting renewal jumps:")
for r in priced:
    if r["registrar"] == "PK Hosting":
        print(f"  {r['extension']}: {r['registration_price']} -> "
              f"{r['renewal_price']} ({r['renewal_jump_pct']:+.1f}%)")
print()

print("Cloudflare renewal rank (USD extensions):")
for ext in sorted(set(r["extension"] for r in priced if r["currency"] == "USD")):
    rows = [r for r in priced if r["currency"] == "USD" and r["extension"] == ext]
    rows_sorted = sorted(rows, key=lambda r: r["renewal_price"])
    cf = next((r for r in rows_sorted if r["registrar"] == "Cloudflare"), None)
    if cf:
        rank = rows_sorted.index(cf) + 1
        print(f"  {ext}: Cloudflare renewal {cf['renewal_price']} is rank "
              f"{rank} of {len(rows_sorted)}")
