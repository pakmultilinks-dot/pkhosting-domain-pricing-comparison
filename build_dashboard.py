"""Generate index.html from domain_pricing.csv.

The dashboard is one self-contained page: the CSV rows are embedded as
an inline JS array, filters run in the browser, no fetch, no keys.
Run: python3 build_dashboard.py
"""
import csv, json
from collections import defaultdict

ROWS = []
with open("domain_pricing.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        ROWS.append(row)

data = []
for r in ROWS:
    data.append({
        "registrar": r["registrar"],
        "extension": r["extension"],
        "reg": float(r["registration_price"]) if r["registration_price"] else None,
        "ren": float(r["renewal_price"]) if r["renewal_price"] else None,
        "currency": r["currency"],
        "jump": float(r["renewal_jump_pct"]) if r["renewal_jump_pct"] else None,
        "source": r["source_url"],
        "notes": r["notes"],
    })

priced = [d for d in data if d["reg"] is not None]

def cheapest(key, cur):
    out = []
    exts = sorted(set(d["extension"] for d in priced if d["currency"] == cur))
    for ext in exts:
        rows = [d for d in priced if d["currency"] == cur and d["extension"] == ext]
        best = min(rows, key=lambda d: d[key])
        out.append((ext, best["registrar"], best[key]))
    return out

cheapest_reg_usd = cheapest("reg", "USD")
cheapest_ren_usd = cheapest("ren", "USD")
jumps = sorted((d for d in priced if d["jump"] is not None),
               key=lambda d: d["jump"], reverse=True)[:5]

def summary_rows(pairs, label):
    return "".join(
        f"<tr><td>{ext}</td><td>{reg}</td><td>{val:g}</td></tr>"
        for ext, reg, val in pairs)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PK Hosting Domain Pricing Comparison (2 Nov 2026)</title>
<style>
body {{ font-family: Arial, Helvetica, sans-serif; margin: 24px auto; max-width: 1060px; padding: 0 16px; color: #222; }}
h1 {{ font-size: 24px; }} h2 {{ font-size: 19px; margin-top: 28px; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
th, td {{ border: 1px solid #ccc; padding: 7px 10px; text-align: left; font-size: 14px; }}
th {{ background: #1a5c2a; color: #fff; }}
tr:nth-child(even) td {{ background: #f4f4f4; }}
select {{ padding: 6px; margin-right: 12px; font-size: 14px; }}
.note {{ color: #555; font-size: 13px; }}
.jump-high {{ color: #b00000; font-weight: bold; }}
</style>
</head>
<body>
<h1>PK Hosting Domain Pricing Comparison</h1>
<p class="note">Prices collected 2 Nov 2026 from the registrars own pages or, where those
pages block automated reads, from Nov 2, 2026 tracker snapshots (see notes per row).
USD and PKR are never converted: compare within one currency only. .pk and .com.pk
prices are per 2-year term. NOT FOUND means the registrar does not list that extension.</p>

<h2>Summary</h2>
<h3>Cheapest USD registration per extension</h3>
<table><tr><th>Extension</th><th>Registrar</th><th>Price (USD)</th></tr>
{summary_rows(cheapest_reg_usd, "reg")}</table>
<h3>Cheapest USD renewal per extension</h3>
<table><tr><th>Extension</th><th>Registrar</th><th>Price (USD)</th></tr>
{summary_rows(cheapest_ren_usd, "ren")}</table>
<p class="note">Cloudflare holds the cheapest USD renewal on all 8 USD extensions,
because it sells at registry cost with no markup.</p>
<h3>Biggest renewal jumps</h3>
<table><tr><th>Registrar</th><th>Extension</th><th>First year</th><th>Renewal</th><th>Jump</th></tr>
{"".join(f"<tr><td>{{d['registrar']}}</td><td>{{d['extension']}}</td><td>{{d['reg']:g}}</td><td>{{d['ren']:g}}</td><td>{{d['jump']:+.1f}}%</td></tr>" for d in jumps)}</table>
<h3>PK Hosting vs PK Domain (PKR, same extensions)</h3>
<table><tr><th>Extension</th><th>PK Hosting</th><th>PK Domain</th><th>Difference</th></tr>
<tr><td>.com (per year)</td><td>3,762</td><td>3,429</td><td>+333 (+9.7%)</td></tr>
<tr><td>.pk (per 2 years)</td><td>5,460</td><td>4,149</td><td>+1,311 (+31.6%)</td></tr>
<tr><td>.com.pk (per 2 years)</td><td>5,460</td><td>4,149</td><td>+1,311 (+31.6%)</td></tr>
</table>
<p class="note">PK Hosting is flat (0% jump) on .com, .net, .pk, .com.pk and .io,
but its .co renewal doubles (+100.0%) and it lists no .ai or .dev price.</p>

<h2>Full table</h2>
<label>Extension:
<select id="extFilter"><option value="all">All extensions</option>
{''.join(f'<option value="{e}">{e}</option>' for e in sorted(set(d["extension"] for d in data)))}
</select></label>
<label>Registrar:
<select id="regFilter"><option value="all">All registrars</option>
{''.join(f'<option value="{r}">{r}</option>' for r in sorted(set(d["registrar"] for d in data)))}
</select></label>
<table>
<tr><th>Registrar</th><th>Extension</th><th>Registration</th><th>Renewal</th><th>Currency</th><th>Renewal jump</th><th>Notes</th></tr>
<tbody id="tbody"></tbody>
</table>
<script>
var DATA = {json.dumps(data)};
function fmt(v) {{ return v === null ? "NOT FOUND" : v.toLocaleString("en-US", {{maximumFractionDigits: 2}}); }}
function render() {{
  var ext = document.getElementById("extFilter").value;
  var reg = document.getElementById("regFilter").value;
  var rows = DATA.filter(function(d) {{
    return (ext === "all" || d.extension === ext) && (reg === "all" || d.registrar === reg);
  }});
  var html = "";
  rows.forEach(function(d) {{
    var jump = d.jump === null ? "NOT FOUND" : (d.jump > 0 ? "+" : "") + d.jump.toFixed(1) + "%";
    var cls = (d.jump !== null && d.jump >= 100) ? ' class="jump-high"' : "";
    html += "<tr><td>" + d.registrar + "</td><td>" + d.extension + "</td><td>" + fmt(d.reg) +
      "</td><td>" + fmt(d.ren) + "</td><td>" + d.currency + "</td><td" + cls + ">" + jump +
      "</td><td>" + d.notes + "</td></tr>";
  }});
  document.getElementById("tbody").innerHTML = html;
}}
document.getElementById("extFilter").addEventListener("change", render);
document.getElementById("regFilter").addEventListener("change", render);
render();
</script>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"index.html written with {len(data)} rows")
