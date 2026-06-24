import os
import re
import sys
from datetime import datetime, timedelta

# ============================================================
# YOUR AMAZON ID - LOCKED AND LOADED
# ============================================================
AMAZON_TAG = "timevalue0e2-20"

# ============================================================
# MAXIMUM VALUE CONFIG (600 PAGES - VERIFIED STABLE)
# 6 Teams (15 matchups) x 8 Cities x 5 Variants = 600 PAGES
# ============================================================
TEAMS = [
    "Portugal", "England", "Argentina", "France", "Brazil", "Germany"
]

CITIES = [
    {"name": "New-York", "tip": "Power banks are essential for long subway rides. Book hotels in Manhattan early."},
    {"name": "London", "tip": "UK plug adapters are mandatory. Use the Tube to get to Wembley."},
    {"name": "Dubai", "tip": "Handheld fans are lifesavers in the heat. Book indoor attractions."},
    {"name": "Tokyo", "tip": "Pocket Wi-Fi routers are cheaper on Amazon. Trains run until midnight."},
    {"name": "Riyadh", "tip": "Lightweight breathable jerseys sell out fast. Stay hydrated."},
    {"name": "Toronto", "tip": "Hand warmers for cold stadium nights. Book GO Train tickets early."},
    {"name": "Frankfurt", "tip": "Get a Europe-wide multi-plug adapter. ICE trains connect perfectly."},
    {"name": "Lisbon", "tip": "Comfortable insoles for walking the hilly city streets."}
]

VARIANTS = [
    "vip-suite", "last-minute-deal", "standard-resale", 
    "group-booking", "family-pack"
]

def main():
    print("🔥 Starting ULTRA-MAX Engine (600 pages)...")
    sys.stdout.flush()
    
    os.makedirs("public", exist_ok=True)
    all_urls = []
    match_count = 0

    # Generate all match combinations (6 choose 2 = 15)
    for i in range(len(TEAMS)):
        for j in range(i+1, len(TEAMS)):
            team_a = TEAMS[i]
            team_b = TEAMS[j]
            match_count += 1
            
            # Add a realistic match date (June 2026 window)
            base_date = datetime(2026, 6, 10) + timedelta(days=match_count % 30)
            display_date = base_date.strftime("%B %d, %Y")
            schema_date = base_date.strftime("%Y-%m-%d")
            
            for city in CITIES:
                for variant in VARIANTS:
                    # Create the clean URL Slug
                    raw_slug = f"{team_a}-vs-{team_b}-{variant}-{city['name']}-2026"
                    slug = re.sub(r'[^a-z0-9\-]', '', raw_slug.lower().replace(" ", "-"))
                    filename = f"{slug}.html"
                    
                    # Dynamic Pricing (makes it look realistic)
                    base_price = 150 + (hash(team_a + team_b + city['name']) % 400)
                    modifier = 2.0 if "vip" in variant else 1.5 if "last-minute" in variant else 1.0
                    min_p = base_price * modifier
                    max_p = min_p * (4.5 + (hash(city['name']) % 10) / 10)
                    
                    # ULTRA MONETIZATION: 5 AMAZON PRODUCTS PER PAGE
                    link_jersey_a = f"https://www.amazon.com/s?k={team_a}+jersey+fifa+2026&tag={AMAZON_TAG}"
                    link_jersey_b = f"https://www.amazon.com/s?k={team_b}+jersey+fifa+2026&tag={AMAZON_TAG}"
                    link_scarf = f"https://www.amazon.com/s?k=fifa+world+cup+scarf+2026&tag={AMAZON_TAG}"
                    link_power = f"https://www.amazon.com/s?k=portable+power+bank+fast+charging&tag={AMAZON_TAG}"
                    link_adapter = f"https://www.amazon.com/s?k=universal+travel+adapter+2026&tag={AMAZON_TAG}"
                    
                    # FULL HTML PAGE (Rich content for SEO)
                    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="google-site-verification" content="Id9ipBDvGsTp1XPX2F37iuV-hgFMh5yaeLNhJBqsM9o" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buy {team_a} vs {team_b} Tickets & Gear in {city['name']} | FIFA 2026</title>
    <meta name="description" content="Get {variant.replace('-', ' ')} tickets for {team_a} vs {team_b} in {city['name']}. Shop official jerseys, scarves, and travel gear on Amazon.">
    <link rel="canonical" href="https://fifa-blitz.vercel.app/{filename}">
    
    <!-- JSON-LD Structured Data (For Google Rich Snippets) -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "SportsEvent",
      "name": "{team_a} vs {team_b} - FIFA World Cup 2026",
      "startDate": "{schema_date}",
      "location": {{
        "@type": "Place",
        "name": "{city['name']} Stadium"
      }},
      "offers": {{
        "@type": "AggregateOffer",
        "lowPrice": {min_p:.2f},
        "highPrice": {max_p:.2f},
        "priceCurrency": "USD"
      }}
    }}
    </script>
    
    <style>
        *{{margin:0;padding:0;box-sizing:border-box;}}
        body{{font-family:'Segoe UI',system-ui;background:#0a0f1e;color:#f8fafc;padding:20px;line-height:1.6;}}
        .container{{max-width:850px;margin:auto;background:#1e293b;padding:40px;border-radius:30px;border:1px solid #334155;box-shadow:0 20px 40px rgba(0,0,0,0.8);}}
        .badge{{display:inline-block;background:#3b82f6;padding:4px 16px;border-radius:30px;font-size:12px;font-weight:600;letter-spacing:1px;text-transform:uppercase;}}
        h1{{font-size:2.4rem;margin:15px 0 5px 0;background:linear-gradient(135deg,#38bdf8,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
        .subtitle{{color:#94a3b8;font-size:1.1rem;border-bottom:1px solid #1e293b;padding-bottom:15px;margin-bottom:20px;}}
        .price-box{{background:#0f172a;padding:25px;border-radius:16px;margin:20px 0;border-left:6px solid #fbbf24;}}
        .price-range{{font-size:2.8rem;font-weight:800;color:#fbbf24;}}
        .grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin:15px 0;}}
        .info-card{{background:#0f172a;padding:12px 18px;border-radius:10px;}}
        .info-card label{{display:block;font-size:11px;color:#64748b;text-transform:uppercase;}}
        .info-card .value{{font-weight:600;}}
        .cta-group{{display:flex;flex-direction:column;gap:12px;margin:25px 0;}}
        .btn{{display:block;text-align:center;padding:15px;border-radius:12px;font-weight:700;text-decoration:none;transition:0.2s;font-size:1.05rem;}}
        .btn:hover{{transform:scale(1.02);filter:brightness(1.1);}}
        .btn-primary{{background:#FF9900;color:#000;}}
        .btn-secondary{{background:#232F3E;color:#fff;border:1px solid #FF9900;}}
        .btn-dark{{background:#0f172a;color:#fff;border:1px solid #334155;}}
        .tip-box{{background:#0f172a;padding:15px;border-radius:12px;margin:15px 0;border:1px dashed #4f46e5;}}
        .disclaimer{{font-size:12px;color:#94a3b8;margin-top:25px;padding-top:15px;border-top:1px solid #1e293b;}}
        @media(max-width:600px){{h1{{font-size:1.8rem;}}.grid-2{{grid-template-columns:1fr;}}}}
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">⚽ FIFA 2026 • {city['name']}</div>
        <h1>{team_a} 🆚 {team_b}</h1>
        <div class="subtitle">{variant.replace('-', ' ').title()} Experience</div>

        <div class="price-box">
            <div style="color:#94a3b8;font-size:14px;">💰 Estimated Market Value ({city['name']})</div>
            <div class="price-range">${min_p:.2f} — ${max_p:.2f} <span style="font-size:16px;font-weight:400;color:#94a3b8;">USD</span></div>
        </div>

        <div class="grid-2">
            <div class="info-card"><label>📅 Date</label><div class="value">{display_date}</div></div>
            <div class="info-card"><label>📍 Venue</label><div class="value">{city['name']} Stadium</div></div>
        </div>

        <div class="tip-box">💡 <strong>Travel Hack:</strong> {city['tip']}</div>

        <h3 style="margin:20px 0 15px 0;">🛒 Complete Fan Kit (Buy on Amazon)</h3>
        <div class="cta-group">
            <a href="{link_jersey_a}" target="_blank" rel="nofollow sponsored" class="btn btn-primary">👕 Buy {team_a} Official Jersey</a>
            <a href="{link_jersey_b}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">👕 Buy {team_b} Official Jersey</a>
            <a href="{link_scarf}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">🏴 Buy FIFA Scarf / Flag</a>
            <a href="{link_power}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">🔋 Portable Power Bank (Stadium Must-Have)</a>
            <a href="{link_adapter}" target="_blank" rel="nofollow sponsored" class="btn btn-secondary">🔌 Universal Travel Adapter</a>
        </div>

        <div class="disclaimer">
            ⚠️ <strong>Amazon Affiliate Disclaimer:</strong> As an Amazon Associate (ID: {AMAZON_TAG}), I earn from qualifying purchases. 
            We are an unofficial fan guide. Check official ticket partners for final availability.
        </div>
    </div>
</body>
</html>"""
                    
                    # Write the file
                    filepath = os.path.join("public", filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(html)
                    
                    url_path = f"/{filename}"
                    all_urls.append(url_path)
                    print(f"✅ Created: {filename}")
                    sys.stdout.flush()

    # --- BUILD MASTER INDEX PAGE ---
    print("📄 Building Master Index (index.html)...")
    sys.stdout.flush()
    
    links_html = ""
    # Show all 600 links sorted nicely
    for u in all_urls:
        title = u.replace("/", "").replace(".html", "").replace("-", " ").title()
        links_html += f'<div class="card"><a href="{u}">{title}</a></div>'
    
    index_content = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FIFA 2026 Ultimate Ticket & Gear Hub</title>
<style>
body{{background:#0a0f1e;color:#f8fafc;font-family:system-ui;padding:30px;}}
.container{{max-width:1400px;margin:auto;}}
h1{{font-size:3rem;background:linear-gradient(135deg,#38bdf8,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:15px;margin:30px 0;}}
.card{{background:#1e293b;padding:14px;border-radius:10px;border:1px solid #334155;transition:0.2s;}}
.card:hover{{border-color:#38bdf8;transform:translateY(-3px);}}
.card a{{color:#38bdf8;text-decoration:none;font-weight:500;display:block;}}
.card a:hover{{text-decoration:underline;}}
.footer{{margin-top:40px;padding-top:20px;border-top:1px solid #1e293b;color:#64748b;text-align:center;}}
</style>
</head>
<body>
<div class="container">
    <h1>🏆 FIFA 2026 World Cup</h1>
    <p><strong>{len(all_urls)}</strong> pages live. Click any match to find tickets and gear.</p>
    <div class="grid">{links_html}</div>
    <div class="footer">⚡ Powered by Amazon Associate ID: {AMAZON_TAG}</div>
</div>
</body></html>"""
    
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    # --- BUILD SITEMAP (Crucial for Google) ---
    print("📄 Building sitemap.xml...")
    sys.stdout.flush()
    sitemap = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for u in all_urls:
        sitemap += f'<url><loc>https://fifa-blitz.vercel.app{u}</loc><changefreq>daily</changefreq><priority>1.0</priority></url>'
    sitemap += '</urlset>'
    with open("public/sitemap.xml", "w") as f:
        f.write(sitemap)

    # --- ROBOTS.TXT ---
    with open("public/robots.txt", "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://fifa-blitz.vercel.app/sitemap.xml")

    print(f"🎯 ULTRA-MAX DEPLOYMENT COMPLETE! {len(all_urls)} pages generated.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
