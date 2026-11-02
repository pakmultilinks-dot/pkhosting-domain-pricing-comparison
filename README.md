# PK Hosting Domain Pricing Comparison

Market comparison of domain extension prices, collected 2 November 2026,
to help PK Hosting price its domain offers. Files in this folder:

- domain_pricing.csv: the dataset (70 rows, 51 priced, 19 NOT FOUND).
- index.html: the dashboard, one self-contained page, no build step.
- report.md: the one-page report with recommendations.
- analysis.py: reads the CSV and prints every summary statistic used in
  the report and dashboard. Run: python3 analysis.py
- build_csv.py, build_dashboard.py: the scripts that generated the CSV
  and the dashboard from the collected figures.

## Data sources

All prices were read on 2 Nov 2026 from the page named in each CSV row's
source_url:

- GoDaddy: Nov 2, 2026 snapshot at
  https://tldspy.com/compare/godaddy-vs-namecheap, with GoDaddy's own
  guide (https://www.godaddy.com/resources/skills/how-much-domain-name-cost,
  May 2026 standard fees) noted per row where it differs.
- Namecheap: Nov 2, 2026 snapshot at the same TLDSpy page. Namecheap's own
  pricing page blocks automated reads, so no figure was taken from it
  directly; the snapshot is dated Nov 2, 2026 and is the freshest
  available figure.
- Porkbun: own price list at https://porkbun.com/products/domains, opened
  2 Nov 2026. Its text rendering drops row labels, so each figure was
  cross-checked against the Nov 2 snapshot at
  https://tldspy.com/compare/cloudflare-vs-porkbun, which matched.
- Dynadot: own price list page at http://www.dynadot.com/domain/, read
  directly (page crawled 1 Nov 2026).
- Cloudflare Registrar: Nov 2, 2026 snapshot at
  https://tldspy.com/compare/cloudflare-vs-porkbun. Cloudflare's own
  pages block automated reads; its at-cost model (registry wholesale plus
  ICANN fee, no markup) is stated on its own product pages.
- PK Hosting: own domains page at https://www.pkhosting.com/domains/,
  fetched 2 Nov 2026. Note: these prices differ from older published
  figures (for example .com was previously listed at 3,999 PKR and is now
  3,762 PKR); the figures here are the ones live on the page on the
  collection date.
- PK Domain (PKNIC reseller, Lahore): own registration page at
  https://pkdomain.com.pk/registration.html, which lists .com, .pk,
  .com.pk and .edu.pk only.

## Assumptions

- Prices are standard, non-premium, single-name prices for one year,
  except .pk and .com.pk, which are sold per 2-year term, and .ai, which
  carries a 2-year minimum term at most registrars.
- Registration price means the first-year price shown, including a promo
  first-year price where the seller shows one. That is why renewal jumps
  look extreme on promo extensions such as .xyz.
- Taxes are not adjusted. Porkbun's list states its prices include ICANN
  and other fees. Other registrars may add tax at checkout.
- No currency conversion is done anywhere. USD rows and PKR rows are
  compared only within their own currency group.

## Cleaning steps

1. Read each source page and recorded registration and renewal prices
   exactly as listed, with the source URL and the collection date
   2026-11-02.
2. Where a registrar does not list an extension, recorded it as NOT FOUND
   with empty price cells, never filled from another registrar.
3. Computed renewal_jump_pct as (renewal minus registration) divided by
   registration, times 100, rounded to one decimal, only where both
   prices exist.
4. Kept .ai term quirks visible instead of smoothing them: Cloudflare's
   160.00 registration figure is a 2-year total, so its computed jump is
   -50.0 percent; the CSV note explains this.
5. Checked for the em-dash character in all output files and removed any
   occurrence; plain hyphens and commas are used instead.

## Method

Manual collection from public pricing pages on one date, recorded in a
flat CSV, with a script (analysis.py) that recomputes every summary
statistic from that CSV. The dashboard (index.html) embeds the same CSV
rows as an inline data array, so the page, the report and the analysis
cannot drift apart.

## Limitations

- Prices move often. GoDaddy's own May 2026 guide already differs from
  the Nov 2 snapshot, and Namecheap's .com renewal was reported at
  different values across Oct 20, Nov 1 and Nov 2 snapshots. Re-check at
  checkout before acting on any single figure.
- Tracker-sourced rows (Namecheap, Cloudflare, and Porkbun's .org row)
  are snapshots of the registrars' list prices, not the registrars' own
  pages, because those pages block automated reads or drop row labels.
  Each such row says so in its notes.
- .pk pricing runs through PKNIC channels and is not comparable to USD
  pricing without a stated exchange rate; none is used here.
- Bundle pricing (domain free with hosting), transfer pricing, premium
  names, and taxes are out of scope.
- No real customer data was used at any step. All figures are public
  list prices.

## How to run the dashboard

Open index.html in any browser. No server, no build step, no network
fetch at runtime. Use the extension and registrar dropdowns to filter
the full table. To recompute the summary numbers, run:
python3 analysis.py
