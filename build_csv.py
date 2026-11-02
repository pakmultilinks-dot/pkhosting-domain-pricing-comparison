"""Build domain_pricing.csv from the collected 2 Nov 2026 figures.

Every figure below was read from the page named in its source_url on
2 Nov 2026. NOT FOUND means the registrar does not list that extension
on its published price list (international registrars do not sell .pk
names; PK Hosting lists no .ai or .dev price; PK Domain publishes only
.com, .pk, .com.pk and .edu.pk prices).
No figure is guessed, converted, or carried from another registrar.
"""
import csv, json

DATE = "2026-11-02"
GD = "https://tldspy.com/compare/godaddy-vs-namecheap"
GD_OWN = "https://www.godaddy.com/resources/skills/how-much-domain-name-cost"
NC = "https://tldspy.com/compare/godaddy-vs-namecheap"
PB = "https://porkbun.com/products/domains"
PB_X = "https://tldspy.com/compare/cloudflare-vs-porkbun"
DY = "http://www.dynadot.com/domain/"
CF = "https://tldspy.com/compare/cloudflare-vs-porkbun"
PKH = "https://www.pkhosting.com/domains/"
PKD = "https://pkdomain.com.pk/registration.html"

# (registrar, extension, reg, renew, currency, source, notes)
# Prices are None for NOT FOUND. PKR .pk/.com.pk prices are per 2-year term.
ROWS = [
    # GoDaddy, USD. Nov 2 snapshot; own guide (May 2026) lists standard
    # annual fees .com 22.99, .net 24.99, .org 23.99, .co 51.99, .xyz 23.99.
    ("GoDaddy", ".com", 13.39, 23.19, "USD", GD, "Own guide lists a 0.01 first-year promo (3-year purchase required) and 22.99 renewal; Nov 2 snapshot shows 13.39/23.19."),
    ("GoDaddy", ".net", 15.19, 25.19, "USD", GD, "Own guide lists 24.99 renewal; Nov 2 snapshot shows 25.19."),
    ("GoDaddy", ".org", 10.19, 24.19, "USD", GD, "Own guide lists 9.99 first year and 23.99 renewal; Nov 2 snapshot shows 10.19/24.19."),
    ("GoDaddy", ".co", 59.99, 59.99, "USD", GD, "Own guide lists a 51.99 standard annual fee (May 2026); Nov 2 snapshot shows 59.99."),
    ("GoDaddy", ".io", 59.99, 89.99, "USD", GD, ""),
    ("GoDaddy", ".ai", 104.99, 159.99, "USD", GD, ""),
    ("GoDaddy", ".dev", 16.19, 24.19, "USD", GD, ""),
    ("GoDaddy", ".xyz", 2.19, 26.19, "USD", GD, "Own guide lists a 23.99 standard annual fee; Nov 2 snapshot shows 2.19 first year and 26.19 renewal."),
    ("GoDaddy", ".pk", None, None, "USD", GD, "NOT FOUND: GoDaddy does not sell .pk names."),
    ("GoDaddy", ".com.pk", None, None, "USD", GD, "NOT FOUND: GoDaddy does not sell .com.pk names."),
    # Namecheap, USD. Own page blocks automated reads; Nov 2 snapshot used.
    ("Namecheap", ".com", 12.08, 19.98, "USD", NC, "Own page blocks automated reads; figure from Nov 2 snapshot. Another tracker showed 18.68 renewal on Oct 20 rising to 20.18 on Nov 1; verify at checkout."),
    ("Namecheap", ".net", 12.48, 18.58, "USD", NC, "Own page blocks automated reads; figure from Nov 2 snapshot."),
    ("Namecheap", ".org", 8.48, 18.98, "USD", NC, "Own page blocks automated reads; figure from Nov 2 snapshot."),
    ("Namecheap", ".co", 19.98, 45.48, "USD", NC, "Own page blocks automated reads; figure from Nov 2 snapshot."),
    ("Namecheap", ".io", 29.98, 75.98, "USD", NC, "Own page blocks automated reads; figure from Nov 2 snapshot."),
    ("Namecheap", ".ai", 89.98, 114.98, "USD", NC, "Own page blocks automated reads; figure from Nov 2 snapshot. 2-year minimum term applies."),
    ("Namecheap", ".dev", 10.98, 20.98, "USD", NC, "Own page blocks automated reads; figure from Nov 2 snapshot."),
    ("Namecheap", ".xyz", 2.00, 21.48, "USD", NC, "Own page blocks automated reads; figure from Nov 2 snapshot."),
    ("Namecheap", ".pk", None, None, "USD", NC, "NOT FOUND: Namecheap does not sell .pk names."),
    ("Namecheap", ".com.pk", None, None, "USD", NC, "NOT FOUND: Namecheap does not sell .com.pk names."),
    # Porkbun, USD. Own price list opened 2 Nov 2026; text rendering drops
    # row labels, so each figure was cross-checked against the Nov 2 snapshot.
    ("Porkbun", ".com", 11.81, 11.81, "USD", PB, "Own price list; figure cross-checked against Nov 2 snapshot (match)."),
    ("Porkbun", ".net", 12.52, 12.52, "USD", PB, "Own price list; figure cross-checked against Nov 2 snapshot (match)."),
    ("Porkbun", ".org", 7.98, 11.84, "USD", PB_X, "Own price list shows a short-term 6.98 first-year sale; 7.98 standard first year and 11.84 renewal from Nov 2 snapshot."),
    ("Porkbun", ".co", 15.76, 31.20, "USD", PB, "Own price list; figure cross-checked against Nov 2 snapshot (match)."),
    ("Porkbun", ".io", 28.12, 51.80, "USD", PB, "Own price list; figure cross-checked against Nov 2 snapshot (match)."),
    ("Porkbun", ".ai", 82.70, 82.70, "USD", PB, "Own price list; figure cross-checked against Nov 2 snapshot (match). 2-year minimum term applies."),
    ("Porkbun", ".dev", 8.75, 12.87, "USD", PB, "Own price list; figure cross-checked against Nov 2 snapshot (match)."),
    ("Porkbun", ".xyz", 2.04, 14.21, "USD", PB, "Own price list; figure cross-checked against Nov 2 snapshot (match)."),
    ("Porkbun", ".pk", None, None, "USD", PB, "NOT FOUND: Porkbun does not sell .pk names."),
    ("Porkbun", ".com.pk", None, None, "USD", PB, "NOT FOUND: Porkbun does not sell .com.pk names."),
    # Dynadot, USD. Own price list page, read directly.
    ("Dynadot", ".com", 11.62, 11.62, "USD", DY, "Own price list page."),
    ("Dynadot", ".net", 12.52, 12.52, "USD", DY, "Own price list page."),
    ("Dynadot", ".org", 7.99, 11.64, "USD", DY, "Own price list page."),
    ("Dynadot", ".co", 15.50, 31.20, "USD", DY, "Own price list page."),
    ("Dynadot", ".io", 28.89, 53.50, "USD", DY, "Own price list page."),
    ("Dynadot", ".ai", 85.60, 85.60, "USD", DY, "Own price list page. 2-year minimum term applies."),
    ("Dynadot", ".dev", 8.00, 12.50, "USD", DY, "Own price list page."),
    ("Dynadot", ".xyz", 1.99, 14.45, "USD", DY, "Own price list page."),
    ("Dynadot", ".pk", None, None, "USD", DY, "NOT FOUND: Dynadot does not sell .pk names."),
    ("Dynadot", ".com.pk", None, None, "USD", DY, "NOT FOUND: Dynadot does not sell .com.pk names."),
    # Cloudflare Registrar, USD. At-cost model; own pages block automated
    # reads, so Nov 2 snapshot used. Registration and renewal are equal
    # except .org, .io, .ai, .dev, .xyz (registry promo pass-through).
    ("Cloudflare", ".com", 11.17, 11.17, "USD", CF, "At-cost pricing (registry wholesale plus ICANN fee, no markup). Own pages block automated reads; figure from Nov 2 snapshot."),
    ("Cloudflare", ".net", 11.86, 11.86, "USD", CF, "At-cost pricing. Own pages block automated reads; figure from Nov 2 snapshot."),
    ("Cloudflare", ".org", 8.50, 11.20, "USD", CF, "At-cost pricing; first year reflects a registry promotion passed through. Own pages block automated reads; figure from Nov 2 snapshot."),
    ("Cloudflare", ".co", 30.00, 30.00, "USD", CF, "At-cost pricing. Own pages block automated reads; figure from Nov 2 snapshot."),
    ("Cloudflare", ".io", 32.00, 50.00, "USD", CF, "At-cost pricing. Own pages block automated reads; figure from Nov 2 snapshot."),
    ("Cloudflare", ".ai", 160.00, 80.00, "USD", CF, "Registration figure is the 2-year minimum term total (80.00 per year); renewal is 80.00 per year. Jump computed on listed figures is -50.0 percent and is an artifact of the 2-year term, not a price cut."),
    ("Cloudflare", ".dev", 8.20, 12.20, "USD", CF, "At-cost pricing. Own pages block automated reads; figure from Nov 2 snapshot."),
    ("Cloudflare", ".xyz", 12.30, 11.20, "USD", CF, "At-cost pricing; renewal below first year because registry promotions pass through. Own pages block automated reads; figure from Nov 2 snapshot."),
    ("Cloudflare", ".pk", None, None, "USD", CF, "NOT FOUND: Cloudflare does not sell .pk names."),
    ("Cloudflare", ".com.pk", None, None, "USD", CF, "NOT FOUND: Cloudflare does not sell .com.pk names."),
    # PK Hosting, PKR. Own domains page, fetched 2 Nov 2026.
    ("PK Hosting", ".com", 3762, 3762, "PKR", PKH, "Own domains page. Flat price, no renewal jump."),
    ("PK Hosting", ".net", 4265, 4265, "PKR", PKH, "Own domains page. Flat price, no renewal jump."),
    ("PK Hosting", ".org", 3956, 4028, "PKR", PKH, "Own domains page."),
    ("PK Hosting", ".pk", 5460, 5460, "PKR", PKH, "Own domains page. Price is for a 2-year term. Flat price, no renewal jump."),
    ("PK Hosting", ".com.pk", 5460, 5460, "PKR", PKH, "Own domains page. Price is for a 2-year term. Flat price, no renewal jump."),
    ("PK Hosting", ".io", 17981, 17981, "PKR", PKH, "Own domains page. Flat price, no renewal jump."),
    ("PK Hosting", ".co", 5394, 10788, "PKR", PKH, "Own domains page. Renewal is double the first-year price."),
    ("PK Hosting", ".xyz", 4783, 4855, "PKR", PKH, "Own domains page."),
    ("PK Hosting", ".ai", None, None, "PKR", PKH, "NOT FOUND: no .ai price shown in PK Hosting published price lists fetched 2 Nov 2026."),
    ("PK Hosting", ".dev", None, None, "PKR", PKH, "NOT FOUND: no .dev price shown in PK Hosting published price lists fetched 2 Nov 2026."),
    # PK Domain (PKNIC reseller, Lahore), PKR. Own registration page.
    ("PK Domain", ".com", 3429, 3429, "PKR", PKD, "Own registration page. Same price at renewal (site states cheap renewal, same price)."),
    ("PK Domain", ".pk", 4149, 4149, "PKR", PKD, "Own registration page. Price is for a 2-year term. Same price at renewal."),
    ("PK Domain", ".com.pk", 4149, 4149, "PKR", PKD, "Own registration page. Price is for a 2-year term. Same price at renewal."),
    ("PK Domain", ".net", None, None, "PKR", PKD, "NOT FOUND: not in PK Domain published price list."),
    ("PK Domain", ".org", None, None, "PKR", PKD, "NOT FOUND: not in PK Domain published price list."),
    ("PK Domain", ".io", None, None, "PKR", PKD, "NOT FOUND: not in PK Domain published price list."),
    ("PK Domain", ".co", None, None, "PKR", PKD, "NOT FOUND: not in PK Domain published price list."),
    ("PK Domain", ".ai", None, None, "PKR", PKD, "NOT FOUND: not in PK Domain published price list."),
    ("PK Domain", ".dev", None, None, "PKR", PKD, "NOT FOUND: not in PK Domain published price list."),
    ("PK Domain", ".xyz", None, None, "PKR", PKD, "NOT FOUND: not in PK Domain published price list."),
]

def jump(reg, ren):
    if reg is None or ren is None or reg == 0:
        return ""
    return round((ren - reg) / reg * 100, 1)

out = "domain_pricing.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["registrar", "extension", "registration_price", "renewal_price",
                "currency", "renewal_jump_pct", "source_url", "collection_date", "notes"])
    for reg_name, ext, r, n, cur, src, note in ROWS:
        w.writerow([reg_name, ext,
                    "" if r is None else r,
                    "" if n is None else n,
                    cur, jump(r, n), src, DATE, note])

priced = sum(1 for row in ROWS if row[2] is not None)
print(f"rows: {len(ROWS)}, priced: {priced}, not found: {len(ROWS) - priced}")
print(f"registrars: {sorted(set(r[0] for r in ROWS))}")
print(f"extensions: {sorted(set(r[1] for r in ROWS))}")
