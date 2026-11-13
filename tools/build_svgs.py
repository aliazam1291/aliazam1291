"""Generates the animated SVGs used in the profile README.
Run: python3 tools/build_svgs.py   (writes into assets/)
Everything is plain SVG + SMIL/CSS so it animates inside GitHub's <img> sandbox.
"""
import math, random, os, html

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
SANS = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
CYAN, VIOLET, PINK = "#70C1FF", "#9B7BFF", "#FF6FD8"
random.seed(7)


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name, len(svg) // 1024, "KB")


def stars(w, h, n, ymax=None):
    out = []
    for i in range(n):
        x, y = random.uniform(0, w), random.uniform(0, ymax or h)
        r = random.choice([0.6, 0.8, 1, 1.2, 1.6])
        d = random.uniform(2, 6)
        b = random.uniform(-6, 0)
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff">'
            f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(out)


# ---------------------------------------------------------------- header
def header():
    W, H = 1200, 420
    gx, gy, R = 905, 190, 118
    # rotating wireframe globe: meridians whose rx follows |cos|
    steps = 24
    vals = ";".join(f"{abs(math.cos(math.pi * i / steps)) * R:.1f}" for i in range(steps + 1))
    meridians = "".join(
        f'<ellipse cx="{gx}" cy="{gy}" rx="{R}" ry="{R}" fill="none" stroke="{CYAN}" stroke-opacity="0.55" stroke-width="1">'
        f'<animate attributeName="rx" values="{vals}" dur="12s" begin="{-k * 2:.1f}s" repeatCount="indefinite"/></ellipse>'
        for k in range(6)
    )
    lats = "".join(
        f'<ellipse cx="{gx}" cy="{gy + R * math.sin(a):.1f}" rx="{R * math.cos(a):.1f}" ry="{R * math.cos(a) * 0.18:.1f}" '
        f'fill="none" stroke="{CYAN}" stroke-opacity="0.35" stroke-width="1"/>'
        for a in [math.radians(d) for d in (-60, -30, 0, 30, 60)]
    )
    # pins pulsing on the globe surface (fleet locations)
    pins = ""
    for i, (px, py) in enumerate([(-40, -35), (25, 10), (60, -55), (-70, 30), (10, 70), (-15, -80)]):
        x, y = gx + px, gy + py
        pins += (
            f'<circle cx="{x}" cy="{y}" r="3" fill="{PINK}"/>'
            f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke="{PINK}" stroke-width="1.5">'
            f'<animate attributeName="r" values="3;14" dur="2.4s" begin="{i * 0.4}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.9;0" dur="2.4s" begin="{i * 0.4}s" repeatCount="indefinite"/></circle>'
        )
    # synthwave perspective floor
    vx, vy, fy = 600, 300, 420
    vlines = "".join(
        f'<line x1="{vx + (x - vx) * 0.04:.1f}" y1="{vy}" x2="{x}" y2="{fy}" stroke="{VIOLET}" stroke-opacity="0.45" stroke-width="1"/>'
        for x in range(-1200, 2401, 100)
    )
    hlines = "".join(
        f'<line x1="0" x2="{W}" y1="{vy}" y2="{vy}" stroke="{VIOLET}" stroke-width="1">'
        f'<animate attributeName="y1" values="{vy};{fy}" dur="4s" begin="{-i * 0.5}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines="0.6 0 1 1"/>'
        f'<animate attributeName="y2" values="{vy};{fy}" dur="4s" begin="{-i * 0.5}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines="0.6 0 1 1"/>'
        f'<animate attributeName="stroke-opacity" values="0;0.7" dur="4s" begin="{-i * 0.5}s" repeatCount="indefinite"/></line>'
        for i in range(8)
    )
    roles = ["Product Engineer", "Fleet & Telematics Platforms", "Geospatial UX · Mappls", "PRD → Figma → Code → Ship", "Moving into Technical PM"]
    n, per = len(roles), 3
    role_txt = ""
    for i, r in enumerate(roles):
        t0, t1 = i / n, (i + 1) / n
        kt = f"0;{t0:.3f};{t0 + 0.02:.3f};{t1 - 0.02:.3f};{t1:.3f};1"
        role_txt += (
            f'<text x="70" y="232" font-family="{MONO}" font-size="22" fill="{CYAN}" opacity="0">&gt; {html.escape(r)}'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{n * per}s" repeatCount="indefinite"/></text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ali Azam Kazmi — Product Engineer, fleet, telematics and geospatial products">
<title>Ali Azam Kazmi — Product Engineer</title>
<defs>
  <radialGradient id="bg" cx="70%" cy="40%" r="90%"><stop offset="0" stop-color="#16244a"/><stop offset="0.55" stop-color="#0a1022"/><stop offset="1" stop-color="#05070f"/></radialGradient>
  <radialGradient id="planet" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#2b5c9e"/><stop offset="0.6" stop-color="#0f2448"/><stop offset="1" stop-color="#060c1c"/></radialGradient>
  <radialGradient id="halo" r="50%"><stop offset="0.6" stop-color="{CYAN}" stop-opacity="0.35"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="0.45" stop-color="{CYAN}"/><stop offset="0.7" stop-color="{VIOLET}"/><stop offset="1" stop-color="#ffffff"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/></linearGradient>
  <linearGradient id="floorfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070f" stop-opacity="1"/><stop offset="0.35" stop-color="#05070f" stop-opacity="0"/></linearGradient>
  <clipPath id="globe"><circle cx="{gx}" cy="{gy}" r="{R}"/></clipPath>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g>{stars(W, H, 110, 300)}</g>
<g>{vlines}{hlines}</g>
<rect y="300" width="{W}" height="120" fill="url(#floorfade)"/>
<line x1="0" x2="{W}" y1="300" y2="300" stroke="{PINK}" stroke-opacity="0.6"/>
<circle cx="{gx}" cy="{gy}" r="{R + 40}" fill="url(#halo)"/>
<circle cx="{gx}" cy="{gy}" r="{R}" fill="url(#planet)"/>
<g clip-path="url(#globe)" filter="url(#glow)">{lats}{meridians}</g>
<circle cx="{gx}" cy="{gy}" r="{R}" fill="none" stroke="{CYAN}" stroke-opacity="0.8" stroke-width="1.5"/>
{pins}
<g transform="rotate(-18 {gx} {gy})">
  <ellipse cx="{gx}" cy="{gy}" rx="205" ry="48" fill="none" stroke="{VIOLET}" stroke-opacity="0.7" stroke-dasharray="4 6">
    <animate attributeName="stroke-dashoffset" values="0;-100" dur="4s" repeatCount="indefinite"/></ellipse>
  <g filter="url(#glow)"><rect x="-9" y="-4" width="18" height="8" rx="2" fill="#fff"/><rect x="-22" y="-3" width="10" height="6" fill="{CYAN}"/><rect x="12" y="-3" width="10" height="6" fill="{CYAN}"/>
    <animateMotion dur="9s" repeatCount="indefinite" path="M {gx + 205} {gy} A 205 48 0 1 1 {gx - 205} {gy} A 205 48 0 1 1 {gx + 205} {gy}"/></g>
</g>
<text x="70" y="120" font-family="{SANS}" font-size="20" letter-spacing="6" fill="#8aa4c8">HELLO, I'M</text>
<text x="66" y="185" font-family="{SANS}" font-size="64" font-weight="800" fill="url(#name)" filter="url(#glow)">Ali Azam Kazmi</text>
{role_txt}
<rect x="70" y="250" width="12" height="3" fill="{CYAN}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
<text x="70" y="285" font-family="{SANS}" font-size="15" fill="#8aa4c8">MapmyIndia (Mappls) · Founder &amp; CPO, DumbMoney · New Delhi, India</text>
</svg>'''


# ---------------------------------------------------------------- live fleet panel
def fleet():
    W, H = 1200, 340
    routes = [
        ("M 60 260 C 200 240 260 120 420 130 S 640 220 760 160", CYAN, 11),
        ("M 80 70 C 220 90 300 200 470 210 S 700 90 780 60", PINK, 14),
        ("M 40 180 L 200 180 C 300 180 330 280 500 280 S 700 260 790 280", VIOLET, 9),
    ]
    grid = "".join(f'<line x1="{x}" y1="20" x2="{x}" y2="320" stroke="#1b2a4a"/>' for x in range(20, 820, 40))
    grid += "".join(f'<line x1="20" y1="{y}" x2="820" y2="{y}" stroke="#1b2a4a"/>' for y in range(20, 330, 40))
    road = ""
    for i, (d, c, dur) in enumerate(routes):
        road += (
            f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity="0.18" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="6 10">'
            f'<animate attributeName="stroke-dashoffset" values="0;-160" dur="3s" repeatCount="indefinite"/></path>'
            f'<g filter="url(#g)"><path d="M -9 -6 L 11 0 L -9 6 L -5 0 Z" fill="{c}"/>'
            f'<animateMotion dur="{dur}s" repeatCount="indefinite" rotate="auto" path="{d}"/></g>'
        )
    hud = [("200,000+", "users on Vahan Shakti"), ("20,000+", "vehicles on Locate"), ("10,000+", "active vehicles on Intouch"), ("4×", "collections with Mappls Shop")]
    hud_svg = ""
    for i, (big, small) in enumerate(hud):
        y = 70 + i * 66
        hud_svg += (
            f'<g>'
            f'<rect x="860" y="{y - 38}" width="300" height="56" rx="10" fill="#0d1730" stroke="#22365e"/>'
            f'<text x="880" y="{y - 4}" font-family="{SANS}" font-size="26" font-weight="800" fill="#fff">{big}</text>'
            f'<text x="880" y="{y + 12}" font-family="{SANS}" font-size="12" fill="#8aa4c8">{html.escape(small)}</text></g>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated live fleet-tracking map with vehicles moving on routes, a geofence, and platform scale numbers">
<title>Live fleet telemetry — the kind of products I build</title>
<defs><filter id="g" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0.25"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="16" fill="#070c1a"/>
<rect x="20" y="20" width="800" height="300" rx="10" fill="#0a1226"/>
{grid}
<circle cx="470" cy="205" r="46" fill="{PINK}" fill-opacity="0.06" stroke="{PINK}" stroke-dasharray="5 5"><animate attributeName="r" values="40;52;40" dur="3s" repeatCount="indefinite"/></circle>
<text x="438" y="268" font-family="{MONO}" font-size="11" fill="{PINK}">GEOFENCE</text>
{road}
<rect x="20" y="20" width="120" height="300" fill="url(#scan)"><animate attributeName="x" values="20;700;20" dur="8s" repeatCount="indefinite"/></rect>
<rect x="36" y="34" width="150" height="26" rx="13" fill="#0d1730" stroke="#22365e"/>
<circle cx="52" cy="47" r="5" fill="#2EE59D"><animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/></circle>
<text x="64" y="52" font-family="{MONO}" font-size="12" fill="#cfe3ff">LIVE · TRACKING</text>
<text x="860" y="15" font-family="{MONO}" font-size="11" fill="#5d7aa6" dy="8">// PLATFORMS I'VE BUILT</text>
{hud_svg}
</svg>'''


# ---------------------------------------------------------------- project cards
CARDS = [
    ("sapceos", "SPACE OS", "3D portfolio — a Three.js flight through my work", ["Next.js 16", "R3F", "GSAP"], CYAN, "orbit"),
    ("D3-Advance-Visuals", "D3 Advanced Visuals", "D3 + Next.js engine for analytics dashboards", ["D3.js", "TypeScript", "Zustand"], VIOLET, "chart"),
    ("sundar", "Sunder Masala", "Rebrand site for a heritage spice brand, 32 SKUs", ["Next.js 16", "Tailwind v4", "SSG"], "#FFB547", "grid"),
    ("casa", "Wolf Casa", "Interiors showroom with 3D curated rooms", ["R3F", "Rapier", "GSAP"], "#2EE59D", "cube"),
    ("react-tech-loaders", "React Tech Loaders", "Hacker-terminal, pixel & neon loaders", ["React", "TypeScript"], PINK, "ring"),
    ("Honeypot-ssh", "SSH Honeypot", "Fake shell that logs attacker commands", ["Python", "Paramiko", "Docker"], "#FF5C5C", "shield"),
]


def glyph(kind, c):
    cx, cy = 340, 62
    if kind == "orbit":
        return (f'<circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="{c}" stroke-width="2"/>'
                f'<ellipse cx="{cx}" cy="{cy}" rx="32" ry="9" fill="none" stroke="{c}" stroke-opacity="0.6" transform="rotate(-20 {cx} {cy})"/>'
                f'<circle r="4" fill="#fff"><animateMotion dur="3s" repeatCount="indefinite" path="M {cx + 30} {cy - 11} A 32 9 -20 1 1 {cx - 30} {cy + 11} A 32 9 -20 1 1 {cx + 30} {cy - 11}"/></circle>')
    if kind == "chart":
        bars = ""
        for i, h in enumerate([18, 30, 22, 40, 28]):
            bars += (f'<rect x="{cx - 30 + i * 13}" y="{cy + 20 - h}" width="9" height="{h}" rx="2" fill="{c}">'
                     f'<animate attributeName="height" values="{h};{h * 0.4:.0f};{h}" dur="{1.6 + i * 0.3:.1f}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="y" values="{cy + 20 - h};{cy + 20 - h * 0.4:.0f};{cy + 20 - h}" dur="{1.6 + i * 0.3:.1f}s" repeatCount="indefinite"/></rect>')
        return bars
    if kind == "grid":
        out = ""
        for i in range(3):
            for j in range(3):
                out += (f'<rect x="{cx - 24 + i * 17}" y="{cy - 24 + j * 17}" width="13" height="13" rx="3" fill="{c}">'
                        f'<animate attributeName="opacity" values="0.25;1;0.25" dur="2.4s" begin="{(i + j) * 0.2:.1f}s" repeatCount="indefinite"/></rect>')
        return out
    if kind == "cube":  # isometric cube that "breathes"
        return (f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="translate" values="0 3;0 -4;0 3" dur="3s" repeatCount="indefinite"/>'
                f'<path d="M 0 -26 L 24 -13 L 0 0 L -24 -13 Z" fill="{c}"/>'
                f'<path d="M -24 -13 L 0 0 L 0 26 L -24 13 Z" fill="{c}" fill-opacity="0.55"/>'
                f'<path d="M 24 -13 L 0 0 L 0 26 L 24 13 Z" fill="{c}" fill-opacity="0.3"/></g></g>')
    if kind == "ring":
        return (f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="#24365a" stroke-width="5"/>'
                f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{c}" stroke-width="5" stroke-linecap="round" stroke-dasharray="40 100">'
                f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="1.4s" repeatCount="indefinite"/></circle>')
    if kind == "shield":
        return (f'<path d="M {cx} {cy - 26} L {cx + 22} {cy - 16} L {cx + 22} {cy + 2} C {cx + 22} {cy + 16} {cx} {cy + 26} {cx} {cy + 26} C {cx} {cy + 26} {cx - 22} {cy + 16} {cx - 22} {cy + 2} L {cx - 22} {cy - 16} Z" fill="none" stroke="{c}" stroke-width="2.5"/>'
                f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{c}">$_'
                f'<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></text>')
    return ""


def card(repo, title, desc, tags, c, kind):
    W, H = 400, 190
    chips, x = "", 24
    for t in tags:
        w = 14 + len(t) * 7.2
        chips += (f'<rect x="{x}" y="138" width="{w:.0f}" height="24" rx="12" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-opacity="0.45"/>'
                  f'<text x="{x + w / 2:.0f}" y="154" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{c}">{html.escape(t)}</text>')
        x += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)} — {html.escape(desc)}">
<title>{html.escape(title)}</title>
<defs>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}"/><stop offset="0.5" stop-color="{c}" stop-opacity="0.05"/><stop offset="1" stop-color="{c}"/>
    <animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="6s" repeatCount="indefinite"/></linearGradient>
  <radialGradient id="gl" cx="85%" cy="20%" r="70%"><stop offset="0" stop-color="{c}" stop-opacity="0.22"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>
</defs>
<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="16" fill="#0b1224" stroke="url(#bd)" stroke-width="2"/>
<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="16" fill="url(#gl)"/>
{glyph(kind, c)}
<text x="24" y="52" font-family="{SANS}" font-size="23" font-weight="800" fill="#fff">{html.escape(title)}</text>
<text x="24" y="76" font-family="{MONO}" font-size="11.5" fill="#5d7aa6">aliazam1291/{html.escape(repo)}</text>
<text x="24" y="112" font-family="{SANS}" font-size="14" fill="#b9cbe6">{html.escape(desc)}</text>
{chips}
<text x="{W - 24}" y="{H - 22}" text-anchor="end" font-family="{SANS}" font-size="13" font-weight="700" fill="{c}">open →<animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/></text>
</svg>'''


# ---------------------------------------------------------------- divider
def divider():
    W = 1200
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="24" viewBox="0 0 {W} 24" role="img" aria-label="section divider">
<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>
<filter id="g"><feGaussianBlur stdDeviation="2"/></filter></defs>
<line x1="0" x2="{W}" y1="12" y2="12" stroke="#1d2b4a"/>
<rect y="10" width="260" height="4" rx="2" fill="url(#d)" filter="url(#g)"><animate attributeName="x" values="-260;{W}" dur="4s" repeatCount="indefinite"/></rect>
<rect y="11" width="260" height="2" rx="1" fill="url(#d)"><animate attributeName="x" values="-260;{W}" dur="4s" repeatCount="indefinite"/></rect>
</svg>'''


# header/fleet/divider retired; only the project cards are still used


for c in CARDS:
    write(f"card-{c[0].lower()}.svg", card(*c))
