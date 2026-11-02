# PK Hosting Domain Pricing Comparison: Report

Date: 2 November 2026. Scope: 10 extensions (.com, .net, .org, .pk, .com.pk,
.io, .co, .ai, .dev, .xyz) across 7 sellers (GoDaddy, Namecheap, Porkbun,
Dynadot, Cloudflare Registrar, PK Hosting, PK Domain). 70 registrar-extension
cells, 51 priced, 19 marked NOT FOUND. Full data: domain_pricing.csv.
Dashboard: index.html. Reproducible summary: analysis.py.

## Method in brief

Each registrar's own public price page was opened first. Dynadot's own page
gave a full 8-extension table. PK Hosting's own domains page was fetched the
same day and gave 8 priced extensions. PK Domain's own registration page gave
.com, .pk and .com.pk. Where a registrar's own page blocks automated reads
(Cloudflare, Namecheap) or its text rendering drops row labels (Porkbun),
figures were taken from Nov 2, 2026 tracker snapshots that republish the
registrar's list prices, and cross-checked against a second tracker where
possible. GoDaddy figures are the Nov 2 snapshot, with GoDaddy's own guide
(May 2026) standard fees noted per row. No price was guessed or carried from
another registrar. USD and PKR are never converted; comparisons run within
one currency. .pk and .com.pk prices are per 2-year term.

## Key findings

1. Renewal is the real price, and .xyz is the trap. The biggest renewal
jumps in the set are all .xyz: GoDaddy 2.19 to 26.19 USD (+1,095.9%),
Namecheap 2.00 to 21.48 (+974.0%), Dynadot 1.99 to 14.45 (+626.1%), Porkbun
2.04 to 14.21 (+596.6%). Cheap first-year .xyz pricing is a loss leader
everywhere except at PK Hosting, where .xyz renews at 4,855 PKR against
4,783 first year (+1.5%).
2. Cloudflare is the renewal floor. Its at-cost model (registry wholesale
plus ICANN fee, no markup) gives it the cheapest USD renewal on all 8 USD
extensions: .com 11.17, .net 11.86, .org 11.20, .co 30.00, .io 50.00,
.ai 80.00 per year, .dev 12.20, .xyz 11.20. No retail registrar beats it on
any renewal.
3. First-year leaders differ by extension. Cheapest USD first year:
.com Cloudflare 11.17, .net Cloudflare 11.86, .org Porkbun 7.98, .co
Dynadot 15.50, .io Porkbun 28.12, .ai Porkbun 82.70, .dev Dynadot 8.00,
.xyz Dynadot 1.99. GoDaddy is the most expensive renewal on .com (23.19),
.net (25.19), .org (24.19) and .ai (159.99).
4. PK Hosting is dearer than the local .pk reseller on every shared
extension. PK Hosting .com is 3,762 PKR vs PK Domain 3,429 (+333, +9.7%).
PK Hosting .pk and .com.pk are 5,460 per 2 years vs PK Domain 4,149
(+1,311, +31.6%). A Pakistani customer comparing two local sellers sees
PK Hosting as the expensive option on exactly the extensions that matter
most locally.
5. PK Hosting's real strength is flat pricing. It charges the same at
renewal as at registration on .com, .net, .pk, .com.pk and .io (0% jump),
against GoDaddy .org +137.4% and Namecheap .io +153.4%. Its one trap is
.co: 5,394 first year doubling to 10,788 at renewal (+100.0%), the same
pattern as Dynadot .co (+101.3%) and Porkbun .co (+98.0%).
6. Two gaps in PK Hosting's catalogue. It publishes no .ai or .dev price,
while international .ai renewals run 80.00 to 159.99 USD and .dev renewals
12.20 to 24.19 USD. International registrars publish no .pk or .com.pk
price at all, so the .pk market is a local-only contest between PK Hosting
and PK Domain.

## Recommendations for PK Hosting

1. Cut .pk and .com.pk toward 4,149 per 2 years, or bundle them with a
hosting plan at the current price. At +31.6% over PK Domain, the current
5,460 price loses the local comparison before any other feature is
considered.
2. Cut .com toward 3,429 to 3,500 PKR, or justify the 333 premium in the
same line: free migration, free SSL, local support. Do not leave the
premium unexplained.
3. Sell flat renewals as the headline promise. "The price you see is the
price you renew at" is true for PK Hosting on .com, .net, .pk, .com.pk
and .io, and it is the exact opposite of the market's biggest complaint.
Publish the renewal price next to every first-year price on the domains
page.
4. Fix .co before promoting it. Either raise the 5,394 first-year price
toward the 10,788 renewal or cut the renewal; a doubling renewal is the
pattern customers punish.
5. Promote .xyz honestly as the exception: 4,783 first year, 4,855
renewal. Every international registrar's .xyz renewal jumps 6 to 11
times; PK Hosting's does not.
6. Add .dev to the catalogue. It is a cheap, developer-facing extension
(12.20 to 24.19 USD renewals internationally) that fits PK Hosting's
hosting customer base. Treat .ai as a separate, high-ticket decision:
its 2-year minimum terms and 80.00 to 159.99 USD renewals need a margin
calculation first, not a copy of the .com price.

## Limitations

Prices change, and promos expire: GoDaddy's own guide figures (May 2026)
already differ from the Nov 2 snapshot, and Namecheap's .com renewal was
reported at 18.68 on Oct 20, rising to 20.18 on Nov 1, against 19.98 in the
Nov 2 snapshot. Tracker-sourced rows must be re-checked at checkout.
.pk pricing runs through PKNIC channels, not the international market, so
USD and PKR rows are not comparable without a stated exchange rate, and
none is used here. .ai figures carry 2-year minimum terms: Cloudflare's
160.00 registration figure is a 2-year total (80.00 per year), which is
why its computed jump shows -50.0%. Taxes, ICANN fees already included
in Porkbun's list, and bundle discounts are not adjusted for.
