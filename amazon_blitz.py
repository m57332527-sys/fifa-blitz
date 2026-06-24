import os, re, itertools, random
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# ============================================================
# YOUR AMAZON ID IS ALREADY LOCKED (DO NOT CHANGE)
# ============================================================
AMAZON_TAG = "timevalue0e2-20"

# ============================================================
# ULTRA EXPANSION: 64 TEAMS (Full FIFA + Qualifiers + Knockouts)
# ============================================================
TEAMS = [
    # Group Stage Favorites
    "Portugal", "England", "Argentina", "France", "Brazil", "Germany", "Spain", "Netherlands",
    "Uzbekistan", "Ghana", "Nigeria", "Senegal", "Cameroon", "Morocco", "Egypt", "Algeria",
    "USA", "Mexico", "Canada", "Japan", "South-Korea", "Australia", "Saudi-Arabia", "Iran",
    "Italy", "Belgium", "Croatia", "Denmark", "Switzerland", "Sweden", "Poland", "Ukraine",
    # Extra Knockout/Underdogs (Adds 32 more = 64 total)
    "Ecuador", "Uruguay", "Colombia", "Peru", "Chile", "Paraguay", "Venezuela", "Bolivia",
    "Scotland", "Wales", "Turkey", "Russia", "Serbia", "Austria", "Greece", "Czech-Republic",
    "Norway", "Hungary", "Romania", "Slovakia", "Slovenia", "Bosnia", "Iceland", "Finland",
    "Guinea", "Mali", "Burkina-Faso", "Zambia", "Congo", "Uganda", "Angola", "Togo"
]

CITIES = [
    {"name": "New-York", "tip": "Buy portable power banks; subway rides are long."},
    {"name": "London", "tip": "UK plug adapter is mandatory."},
    {"name": "Dubai", "tip": "Handheld fans are a lifesaver in the heat."},
    {"name": "Tokyo", "tip": "Pocket Wi-Fi is cheaper on Amazon."},
    {"name": "Riyadh", "tip": "Lightweight, breathable jerseys sell out fast."},
    {"name": "Toronto", "tip": "Hand warmers for the cold nights."},
    {"name": "Frankfurt", "tip": "Get a Europe-wide multi-plug adapter."},
    {"name": "Lisbon", "tip": "Comfortable insoles for walking all day."},
    {"name": "Miami", "tip": "Rain poncho is essential for sudden showers."},
    {"name": "Sydney", "tip": "Sunscreen and UV-protection sleeves."}
]

VARIANTS = ["vip-suite", "last-minute", "standard-resale", "group-booking", "family-pack", "ultimate-fan-experience"]

def generate_pages():
    tasks = []
    # Generate ALL possible match combinations (2,016 matches from 64 teams)
    # We take the first 400 to reach 400 * 10 * 6 = 24,000 pages
    match_pairs = list(itertools.combinations(TEAMS, 2))[:400] 
    
    for team_a, team_b in match_pairs:
        # Generate a realistic match date (between June 1 - July 20, 2026)
        random.seed(hash(team_a + team_b))
        days_offset = random.randint(1, 50)
        match_date = datetime(2026, 6, 1) + timedelta(days=days_offset)
        display_date = match_date.strftime("%B %d, %Y")
        schema_date = match_date.strftime("%Y-%m-%d")
        
        for city in CITIES:
            for variant in VARIANTS:
                base = 150 + (hash(team_a + team_b + city['name']) % 500)
                modifier = 2.0 if "vip" in variant else 1.2 if "ultimate" in variant else 1.0
                min_p = base * modifier
                max_p = min_p * 6.0
                
                slug = f"{team_a}-vs-{team_b}-{variant}-{city['name']}-2026".lower()
                slug = re.sub(r'[^a-z0-9\-]', '', slug)[:90]
                
                tasks.append({
                    "slug": slug, "team_a": team_a, "team_b": team_b,
                    "city": city["name"], "city_tip": city["tip"],
                    "variant": variant.replace("-", " ").title(),
                    "date": display_date, "schema_date": schema_date,
                    "min": f"${min_p:,.2f}", "max": f"${max_p:,.2f}",
                    "tag": AMAZON_TAG
                })
    return tasks

def write_page(p):
    os.makedirs("public", exist_ok=True)
    
    # ULTRA MONETIZATION: 7 Amazon Links (Jersey A, Jersey B, Scarf, Flag, Power Bank, Adapter, Fan Kit)
    link_a = f"https://www.amazon.com/s?k={p['team_a']}+jersey+fifa+2026&tag={p['tag']}"
    link_b = f"https://www.amazon.com/s?k={p['team_b']}+jersey+fifa+2026&tag={p['tag']}"
    link_scarf = f"https://www.amazon.com/s?k=fifa+2026+scarf+flag&tag={p['tag']}"
    link_power = f"https://www.amazon.com/s?k=power+bank+fast+charging&tag={p['tag']}"
    link_adapter = f"https://www.amazon.com/s?k=universal+travel+adapter+2026&tag={p['tag']}"
    link_kit = f"https://www.amazon.com/s?k=fan+kit+face+paint+whistle&tag={p['tag']}"
    link_ticket = f"https://www.stubhub.com/search?q={p['team_a']}+{p['team_b']}+tickets"  # Extra ticket link
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>{p['team_a']} vs {p['team_b']} Tickets & Gear {p['city']} 2026</title>
<meta name="description" content="Ultimate {p['variant']} guide for {p['team_a']} vs {p['team_b']} in {p['city']}. Shop jerseys, travel gear, and last-minute tickets.">
<link rel="canonical" href="https://fifa-blitz.vercel.app/{p['slug']}.html">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SportsEvent","startDate":"{p['schema_date']}","offers":{{"@type":"AggregateOffer","lowPrice":"{p['min']}","highPrice":"{p['max']}","priceCurrency":"USD"}}}}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Segoe UI',system-ui;background:#0a0f1e;color:#f8fafc;padding:20px;}}
.container{{max-width:850px;margin:auto;background:#1e293b;padding:40px;border-radius:30px;border:1px solid #334155;}}
h1{{font-size:2.4rem;background:linear-gradient(135deg,#38bdf8,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.price-tag{{background:#0f172a;padding:25px;border-radius:16px;margin:20px 0;border-left:6px solid #fbbf24;}}
.price-range{{font-size:2.8rem;font-weight:800;color:#fbbf24;}}
.btn{{display:block;text-align:center;padding:15px;border-radius:12px;font-weight:700;text-decoration:none;margin:10px 0;transition:0.2s;}}
.btn:hover{{transform:scale(1.03);filter:brightness(1.1);}}
.btn-amazon{{background:#FF9900;color:#000;}}
.btn-stubhub{{background:#0054a6;color:#fff;}}
.btn-secondary{{background:#232F3E;color:#fff;border:1px solid #FF9900;}}
.tip-box{{background:#0f172a;padding:15px;border-radius:12px;margin:15px 0;border:1px dashed #4f46e5;}}
.countdown{{background:#dc2626;padding:12px;border-radius:30px;text-align:center;font-weight:700;margin:15px 0;}}
.disclaimer{{font-size:12px;color:#94a3b8;margin-top:25px;padding-top:15px;border-top:1px solid #334155;}}
</style>
</head>
<body>
<div class="container">
    <div class="countdown">⚡ MATCH DAY: {p['date']} ⚡ (FIFA 2026 - Peak Demand)</div>
    <h1>⚽ {p['team_a']} 🆚 {p['team_b']}</h1>
    <p style="color:#94a3b8;font-size:1.2rem;">{p['variant']} • {p['city']} • World Cup 2026</p>
    
    <div class="price-tag">
        <div style="color:#94a3b8;">💰 Estimated Fan Resale Value</div>
        <div class="price-range">{p['min']} — {p['max']} USD</div>
    </div>

    <div class="tip-box">💡 <strong>Ultra Travel Hack:</strong> {p['city_tip']} (Buy now, prices spike closer to match).</div>

    <h3 style="margin:20px 0 15px 0;">🛒 ULTRA FAN KIT (Buy Everything Here)</h3>
    
    <a href="{link_a}" target="_blank" rel="nofollow sponsored" class="btn btn-amazon">👕 Buy {p['team_a']} Official Jersey (Amazon)</a>
    <a href="{link_b}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">👕 Buy {p['team_b']} Official Jersey (Amazon)</a>
    <a href="{link_scarf}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">🏴 Buy FIFA Scarf + Flag (Amazon)</a>
    <a href="{link_power}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">🔋 Power Bank (Stadium Must-Have)</a>
    <a href="{link_adapter}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">🔌 Universal Travel Adapter</a>
    <a href="{link_kit}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">🎉 Face Paint + Fan Kit (Amazon)</a>
    
    <h3 style="margin:20px 0 10px 0;">🎟️ TICKETS (External Partner)</h3>
    <a href="{link_ticket}" target="_blank" rel="nofollow sponsored" class="btn btn-stubhub">🎟️ Check Live Resale Tickets (StubHub)</a>

    <div class="disclaimer">
        ⚠️ <strong>Amazon Affiliate:</strong> I earn commissions (ID: {p['tag']}) from Amazon purchases. 
        Ticket links are referrals. We are an unofficial fan guide.
    </div>
</div>
</body>
</html>"""
    
    with open(f"public/{p['slug']}.html", "w", encoding="utf-8") as f:
        f.write(html)
    return f"https://fifa-blitz.vercel.app/{p['slug']}.html"

if __name__ == "__main__":
    print("🔥 ULTRA MODE: Building 25,000+ pages for timevalue0e2-20...")
    tasks = generate_pages()
    with ThreadPoolExecutor(max_workers=30) as ex:
        urls = list(ex.map(write_page, tasks))
    
    # Sitemap with 25,000 URLs
    # 1. Build Sitemap
with open("public/sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        f.write(f'<url><loc>{u}</loc><changefreq>daily</changefreq><priority>1.0</priority></url>')
    f.write('</urlset>')

# 2. Build INDEX.HTML (This fixes the 404)
index_html_content = f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FIFA 2026 Ultimate Ticket & Gear Hub</title>
<style>
body{{background:#0a0f1e;color:#f8fafc;font-family:system-ui;padding:40px;}}
.container{{max-width:1200px;margin:auto;}}
h1{{font-size:3rem;background:linear-gradient(135deg,#38bdf8,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:15px;margin:30px 0;}}
.card{{background:#1e293b;padding:18px;border-radius:12px;border:1px solid #334155;}}
.card a{{color:#38bdf8;text-decoration:none;font-weight:600;}}
.card a:hover{{text-decoration:underline;}}
.footer{{margin-top:40px;color:#64748b;border-top:1px solid #1e293b;padding-top:20px;text-align:center;}}
</style>
</head>
<body>
<div class="container">
    <h1>🏆 FIFA 2026 World Cup</h1>
    <p>Find tickets, jerseys, and travel gear for every match. <strong>{len(urls)}</strong> pages indexed.</p>
    <div class="grid">
'''
# Add first 200 pages as clickable links (to keep the page fast)
for u in urls[:200]:
    title = u.split('/')[-1].replace('.html', '').replace('-', ' ').title()
    index_html_content += f'<div class="card"><a href="{u}">{title}</a></div>'

index_html_content += f'''
    </div>
    <div class="footer">⚡ All 25,000+ matches covered. Amazon Associate ID: {AMAZON_TAG}</div>
</div>
</body>
</html>'''

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(index_html_content)
    
    with open("public/robots.txt", "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://fifa-blitz.vercel.app/sitemap.xml")
    
    print(f"✅ ULTRA DEPLOYMENT COMPLETE! {len(urls)} pages built.")
