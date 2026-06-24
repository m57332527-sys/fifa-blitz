import os
import re
import sys

# ============================================================
# YOUR AMAZON ID IS LOCKED (DO NOT CHANGE)
# ============================================================
AMAZON_TAG = "timevalue0e2-20"

# ============================================================
# TEST MODE: ONLY 3 MATCHES, 4 CITIES, 4 VARIANTS = 48 PAGES
# THIS WILL BUILD IN UNDER 5 SECONDS ON VERCEL
# ============================================================
TEAMS = ["Portugal", "England", "Argentina"]
CITIES = [
    {"name": "New-York", "tip": "Power banks are essential."},
    {"name": "London", "tip": "UK plug adapter is mandatory."},
    {"name": "Dubai", "tip": "Handheld fans are lifesavers."},
    {"name": "Tokyo", "tip": "Pocket Wi-Fi is cheaper on Amazon."}
]
VARIANTS = ["vip-suite", "last-minute", "standard-resale", "family-pack"]

def main():
    print("🔥 Starting TEST build (48 pages)...")
    sys.stdout.flush()  # Force Vercel to show this log immediately
    
    os.makedirs("public", exist_ok=True)
    generated_urls = []
    
    # Generate pages (NO THREADING, NO COMPLEX LOGIC)
    for team_a in TEAMS:
        for team_b in TEAMS:
            if team_a == team_b:
                continue  # Skip same-team matches
            for city in CITIES:
                for variant in VARIANTS:
                    # Create slug
                    raw_slug = f"{team_a}-vs-{team_b}-{variant}-{city['name']}-2026"
                    slug = re.sub(r'[^a-z0-9\-]', '', raw_slug.lower().replace(" ", "-"))
                    filename = f"{slug}.html"
                    
                    # Dummy price
                    min_p = 150.00
                    max_p = 850.00
                    
                    # Amazon links
                    link_a = f"https://www.amazon.com/s?k={team_a}+jersey+fifa+2026&tag={AMAZON_TAG}"
                    link_b = f"https://www.amazon.com/s?k={team_b}+jersey+fifa+2026&tag={AMAZON_TAG}"
                    
                    # HTML Content (Short and sweet)
                    html = f"""<!DOCTYPE html>
<html>
<head><title>{team_a} vs {team_b} Tickets {city['name']} 2026</title>
<meta name="description" content="Buy {team_a} vs {team_b} tickets and gear in {city['name']}.">
<link rel="canonical" href="https://fifa-blitz.vercel.app/{filename}">
</head>
<body style="font-family:system-ui;background:#0a0f1e;color:#fff;padding:40px;">
<div style="max-width:800px;margin:auto;background:#1e293b;padding:40px;border-radius:30px;">
<h1>⚽ {team_a} vs {team_b}</h1>
<p>{city['name']} • FIFA 2026</p>
<p>💰 Estimated: ${min_p:.2f} - ${max_p:.2f}</p>
<p>💡 {city['tip']}</p>
<a href="{link_a}" style="display:block;background:#FF9900;color:#000;padding:15px;text-align:center;border-radius:12px;text-decoration:none;margin:10px 0;">👕 Buy {team_a} Jersey</a>
<a href="{link_b}" style="display:block;background:#232F3E;color:#fff;padding:15px;text-align:center;border-radius:12px;text-decoration:none;margin:10px 0;">👕 Buy {team_b} Jersey</a>
<p style="font-size:12px;color:#94a3b8;">Amazon ID: {AMAZON_TAG}</p>
</div>
</body></html>"""
                    
                    # Write the file
                    filepath = os.path.join("public", filename)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(html)
                    
                    url = f"/{filename}"
                    generated_urls.append(url)
                    print(f"✅ Created: {filename}")
                    sys.stdout.flush()
    
    # --- Build Index.html (The Fix for 404) ---
    print("📄 Building index.html...")
    sys.stdout.flush()
    
    links_html = ""
    for u in generated_urls:
        title = u.replace("/", "").replace(".html", "").replace("-", " ").title()
        links_html += f'<div style="background:#1e293b;padding:10px;border-radius:8px;margin:5px 0;"><a href="{u}" style="color:#38bdf8;text-decoration:none;">{title}</a></div>'
    
    index_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>FIFA 2026 Hub</title>
<style>body{{background:#0a0f1e;color:#fff;font-family:system-ui;padding:40px;}}
.container{{max-width:800px;margin:auto;}}
h1{{font-size:2.5rem;background:linear-gradient(135deg,#38bdf8,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
</style>
</head>
<body>
<div class="container">
<h1>🏆 FIFA 2026</h1>
<p><strong>{len(generated_urls)}</strong> pages live. Click any link below.</p>
{links_html}
<p style="margin-top:30px;color:#64748b;">Amazon ID: {AMAZON_TAG}</p>
</div>
</body></html>"""
    
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    # Build sitemap
    print("📄 Building sitemap.xml...")
    sys.stdout.flush()
    sitemap = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    for u in generated_urls:
        sitemap += f'<url><loc>https://fifa-blitz.vercel.app{u}</loc><priority>1.0</priority></url>'
    sitemap += '</urlset>'
    with open("public/sitemap.xml", "w") as f:
        f.write(sitemap)
    
    # Robots
    with open("public/robots.txt", "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://fifa-blitz.vercel.app/sitemap.xml")
    
    print(f"🎯 DEPLOYMENT COMPLETE! {len(generated_urls)} pages generated.")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
