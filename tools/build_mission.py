"""Mission-control set of animated SVGs for the profile README (matches aliazamkazmi.vercel.app).
Run: python3 tools/build_mission.py  -> assets/mc-*.svg
Plain SVG + SMIL so it animates inside GitHub's <img> sandbox (no JS, no web fonts).
"""
import math, os, random, html

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
SANS = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
TEAL, CYAN, AMBER, PINK, VIOLET = "#3EE6B4", "#70C1FF", "#FFB547", "#FF6FD8", "#9B7BFF"
BG0, BG1, LINE, DIM = "#040908", "#08120f", "#14302a", "#5f8f84"
random.seed(11)
esc = html.escape


def write(name, svg):
    p = os.path.join(OUT, name)
    open(p, "w", encoding="utf-8").write(svg)
    print("wrote", name, f"{len(svg)//1024}KB")


def glow(id_="gl", s=3):
    return f'<filter id="{id_}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{s}" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'


def corners(x, y, w, h, c=TEAL, L=18, op=0.8):
    p = [f"M{x} {y+L} V{y} H{x+L}", f"M{x+w-L} {y} H{x+w} V{y+L}", f"M{x+w} {y+h-L} V{y+h} H{x+w-L}", f"M{x+L} {y+h} H{x} V{y+h-L}"]
    return "".join(f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity="{op}" stroke-width="2"/>' for d in p)


def blink(dur=1.2, begin=0):
    return f'<animate attributeName="opacity" values="1;0.15;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'


def dust(W, H, n):
    s = ""
    for _ in range(n):
        x, y, r = random.uniform(0, W), random.uniform(0, H), random.choice([0.5, 0.7, 1, 1.3])
        d, b = random.uniform(2, 6), random.uniform(-6, 0)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#cffff0"><animate attributeName="opacity" values="0.1;0.9;0.1" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>'
    return s


# ============================================================ HERO: launch pad
def hero():
    W, H = 1200, 520
    cx, cy = 900, 330  # launch pad centre (ellipse = 3D disc)
    rings = ""
    for i, (rx, op) in enumerate([(250, .25), (190, .35), (130, .55), (70, .8)]):
        rings += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.32:.0f}" fill="none" stroke="{TEAL}" stroke-opacity="{op}" stroke-width="{2 if i==2 else 1}"/>'
    # radar sweep on the disc (rotating wedge squashed into perspective)
    sweep = (f'<g transform="translate({cx} {cy}) scale(1 0.32)"><g>'
             f'<path d="M0 0 L250 0 A250 250 0 0 0 216.5 -125 Z" fill="url(#sw)"/>'
             f'<animateTransform attributeName="transform" type="rotate" values="0;-360" dur="5s" repeatCount="indefinite"/></g></g>')
    # tick marks around rim
    ticks = "".join(
        f'<line x1="{cx+260*math.cos(a):.1f}" y1="{cy+260*math.sin(a)*0.32:.1f}" x2="{cx+272*math.cos(a):.1f}" y2="{cy+272*math.sin(a)*0.32:.1f}" stroke="{TEAL}" stroke-opacity="0.5"/>'
        for a in [i * math.pi / 24 for i in range(48)])
    # blips appearing on the radar (fleet)
    blips = ""
    for i in range(7):
        a, r = random.uniform(0, 2 * math.pi), random.uniform(60, 230)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a) * 0.32
        blips += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="{AMBER if i%3==0 else TEAL}" opacity="0">'
                  f'<animate attributeName="opacity" values="0;1;0" dur="5s" begin="{i*0.7:.1f}s" repeatCount="indefinite"/></circle>')
    # low-poly craft hovering above the pad (wireframe, bobbing)
    craft = f'''<g filter="url(#gl)"><g>
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -14;0 0" dur="4s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>
      <path d="M{cx} {cy-210} L{cx+28} {cy-120} L{cx} {cy-100} L{cx-28} {cy-120} Z" fill="#0d2a24" stroke="{TEAL}" stroke-width="1.5"/>
      <path d="M{cx-28} {cy-120} L{cx-150} {cy-92} L{cx-120} {cy-82} L{cx} {cy-100} Z" fill="#0b2420" stroke="{TEAL}" stroke-width="1.2"/>
      <path d="M{cx+28} {cy-120} L{cx+150} {cy-92} L{cx+120} {cy-82} L{cx} {cy-100} Z" fill="#081c19" stroke="{TEAL}" stroke-width="1.2"/>
      <path d="M{cx} {cy-210} L{cx} {cy-100}" stroke="{TEAL}" stroke-opacity="0.6"/>
      <path d="M{cx-10} {cy-160} L{cx} {cy-175} L{cx+10} {cy-160} Z" fill="{TEAL}" fill-opacity="0.8"/>
      <path d="M{cx-12} {cy-100} L{cx} {cy-62} L{cx+12} {cy-100} Z" fill="{AMBER}"><animate attributeName="opacity" values="0.4;1;0.4" dur="0.35s" repeatCount="indefinite"/></path>
    </g></g>
    <ellipse cx="{cx}" cy="{cy}" rx="70" ry="16" fill="{TEAL}" fill-opacity="0.18"><animate attributeName="rx" values="60;84;60" dur="4s" repeatCount="indefinite"/></ellipse>'''
    vy, fy = 300, H - 22
    floor = "".join(f'<line x1="{cx+(x-cx)*0.05:.0f}" y1="{vy}" x2="{x}" y2="{fy}" stroke="{TEAL}" stroke-opacity=".12"/>' for x in range(-600, 2400, 90))
    floor += "".join(f'<line x1="640" x2="{W-22}" y1="{vy}" y2="{vy}" stroke="{TEAL}" stroke-opacity=".0"><animate attributeName="y1" values="{vy};{fy}" dur="5s" begin="{-i*0.83:.2f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".6 0 1 1"/><animate attributeName="y2" values="{vy};{fy}" dur="5s" begin="{-i*0.83:.2f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".6 0 1 1"/><animate attributeName="stroke-opacity" values="0;.35" dur="5s" begin="{-i*0.83:.2f}s" repeatCount="indefinite"/></line>' for i in range(6))
    floor = f'<g clip-path="url(#fl)">{floor}</g>'
    # HUD telemetry readouts that tick
    hud = ""
    for j, (lab, vals) in enumerate([("ALT", ["0.0", "1.2", "2.9", "4.4", "6.1"]), ("VEL", ["000", "120", "260", "410", "580"]), ("SYS", ["NOMINAL"] * 5)]):
        y = 140 + j * 34
        hud += f'<text x="1140" y="{y}" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{DIM}">{lab}</text>'
        for k, v in enumerate(vals):
            hud += (f'<text x="1140" y="{y+16}" text-anchor="end" font-family="{MONO}" font-size="14" fill="#d9fff3" opacity="0">{v}'
                    f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{k/5:.2f};{k/5+.01:.2f};{(k+1)/5-.01:.2f};{(k+1)/5:.2f};1" dur="4s" repeatCount="indefinite"/></text>')
    stats = [("31", "PROJECTS"), ("14", "PRODUCTS BUILT"), ("16", "DESIGN PROJECTS"), ("200,000+", "USERS · LARGEST PLATFORM")]
    st = ""
    x = 60
    for i, (n, l) in enumerate(stats):
        w = [110, 160, 170, 230][i]
        st += (f'<g><text x="{x}" y="418" font-family="{SANS}" font-size="30" font-weight="700" fill="{TEAL}">{n}</text>'
               f'<text x="{x}" y="440" font-family="{MONO}" font-size="10.5" letter-spacing="1.5" fill="{DIM}">{l}</text></g>')
        if i < 3:
            st += f'<line x1="{x+w-14}" y1="392" x2="{x+w-14}" y2="444" stroke="{LINE}"/>'
        x += w
    # countdown T-03 → T-00 → LIFTOFF loop
    cd = ""
    seq = ["T-03", "T-02", "T-01", "T-00"]
    n = len(seq)
    for i, s in enumerate(seq):
        a, b = i / n, (i + 1) / n
        cd += (f'<text x="1140" y="78" text-anchor="end" font-family="{MONO}" font-size="30" font-weight="700" fill="{TEAL}" opacity="0">{s}'
               f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{a:.3f};{a+.01:.3f};{b-.01:.3f};{b:.3f};1" dur="4s" repeatCount="indefinite"/></text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Ali Azam Kazmi — Product Engineer moving into Technical PM. Mission-control launch pad with a hovering craft and radar.">
<title>Ali Azam Kazmi — Product Engineer · Space OS</title>
<defs>{glow()}
<radialGradient id="bg" cx="75%" cy="65%" r="85%"><stop offset="0" stop-color="#0c2a23"/><stop offset=".5" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></radialGradient>
<radialGradient id="sw" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="scale(250)"><stop offset="0" stop-color="{TEAL}" stop-opacity=".0"/><stop offset="1" stop-color="{TEAL}" stop-opacity=".35"/></radialGradient>
<linearGradient id="nm" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#d9fff3"/><stop offset=".62" stop-color="{TEAL}"/><stop offset=".74" stop-color="#fff"/><stop offset="1" stop-color="#fff"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/></linearGradient>
<clipPath id="fl"><rect x="730" y="300" width="450" height="200"/></clipPath><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{LINE}" stroke-opacity=".55"/></pattern>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)" opacity=".5"/>
{dust(W, H, 70)}
{floor}{rings}{ticks}{sweep}{blips}{craft}
<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="{LINE}"/>
{corners(20, 20, W-40, H-40)}
<circle cx="52" cy="58" r="5" fill="{TEAL}">{blink()}</circle>
<text x="66" y="63" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{DIM}">PAD 01 · CLEARED FOR LAUNCH</text>
<text x="1140" y="44" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{DIM}">SPACE OS · NEW DELHI 28.61°N 77.21°E</text>
{cd}
<line x1="1020" y1="90" x2="1140" y2="90" stroke="{TEAL}" stroke-width="2"/>
{hud}
<text x="60" y="150" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{TEAL}">● PORTFOLIO · PRODUCT ENGINEER → TECHNICAL PM</text>
<text x="56" y="222" font-family="{SANS}" font-size="70" font-weight="800" letter-spacing="-1.5" fill="url(#nm)">Ali Azam Kazmi</text>
<text x="60" y="268" font-family="{SANS}" font-size="20" fill="#cfe9e1">Give me a problem. I’ll figure out what to do next.</text>
<text x="60" y="300" font-family="{SANS}" font-size="15" fill="{DIM}">Fleet &amp; geospatial products at MapmyIndia · Founder &amp; CPO, DumbMoney · Smaak.ux studio</text>
<line x1="60" y1="370" x2="610" y2="370" stroke="{LINE}"/>
{st}
<text x="60" y="482" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{DIM}">HOLD TO LAUNCH ▸ aliazamkazmi.vercel.app</text>
<rect x="56" y="490" width="0" height="2" fill="{TEAL}"><animate attributeName="width" values="0;330;330;0" keyTimes="0;.7;.9;1" dur="4s" repeatCount="indefinite"/></rect>
</svg>'''


# ============================================================ connect tiles
def tile(kind, label, sub, c):
    W, H = 280, 120
    logo = ""
    lx, ly = 52, 60
    if kind == "linkedin":
        logo = (f'<rect x="{lx-24}" y="{ly-24}" width="48" height="48" rx="9" fill="{c}"/>'
                f'<text x="{lx}" y="{ly+12}" text-anchor="middle" font-family="{SANS}" font-size="31" font-weight="800" fill="#fff">in</text>')
    elif kind == "behance":
        logo = (f'<rect x="{lx-24}" y="{ly-24}" width="48" height="48" rx="24" fill="{c}"/>'
                f'<text x="{lx}" y="{ly+9}" text-anchor="middle" font-family="{SANS}" font-size="23" font-weight="800" fill="#fff">Bē</text>')
    elif kind == "figma":
        r = 8
        cols = ["#F24E1E", "#FF7262", "#A259FF", "#1ABCFE", "#0ACF83"]
        logo = (f'<g transform="translate({lx-8} {ly-24})">'
                f'<path d="M0 0h8a8 8 0 0 1 0 16H0z" transform="translate(8 0)" fill="{cols[1]}"/><path d="M8 0H0a8 8 0 0 0 0 16h8z" transform="translate(8 0) translate(-8 0)" fill="{cols[0]}"/>'
                f'<path d="M8 16H0a8 8 0 0 0 0 16h8z" fill="{cols[2]}"/><circle cx="16" cy="24" r="8" fill="{cols[3]}"/>'
                f'<path d="M8 32H0a8 8 0 1 0 8 8z" fill="{cols[4]}"/></g>')
    elif kind == "portfolio":
        logo = (f'<circle cx="{lx}" cy="{ly}" r="20" fill="none" stroke="{c}" stroke-width="2"/>'
                f'<ellipse cx="{lx}" cy="{ly}" rx="34" ry="9" fill="none" stroke="{c}" stroke-opacity=".7" transform="rotate(-20 {lx} {ly})"/>'
                f'<circle r="4" fill="#fff"><animateMotion dur="2.6s" repeatCount="indefinite" path="M{lx+32} {ly-11} A34 9 -20 1 1 {lx-32} {ly+11} A34 9 -20 1 1 {lx+32} {ly-11}"/></circle>')
    elif kind == "resume":
        logo = (f'<rect x="{lx-17}" y="{ly-23}" width="34" height="46" rx="4" fill="none" stroke="{c}" stroke-width="2"/>'
                + "".join(f'<rect x="{lx-10}" y="{ly-13+i*8}" width="{20 if i%2==0 else 14}" height="2.5" rx="1" fill="{c}"><animate attributeName="width" values="0;{20 if i%2==0 else 14}" dur="1.2s" begin="{i*0.2}s" fill="freeze"/></rect>' for i in range(4)))
    elif kind == "mail":
        logo = (f'<rect x="{lx-24}" y="{ly-17}" width="48" height="34" rx="5" fill="none" stroke="{c}" stroke-width="2"/>'
                f'<path d="M{lx-24} {ly-15} L{lx} {ly+3} L{lx+24} {ly-15}" fill="none" stroke="{c}" stroke-width="2"/>')
    elif kind == "medium":
        logo = (f'<circle cx="{lx-12}" cy="{ly}" r="13" fill="#fff"/><ellipse cx="{lx+10}" cy="{ly}" rx="6" ry="12" fill="#fff"/><ellipse cx="{lx+22}" cy="{ly}" rx="2.5" ry="11" fill="#fff"/>')
    elif kind == "dumbmoney":
        logo = (f'<rect x="{lx-24}" y="{ly-24}" width="48" height="48" rx="12" fill="{c}" fill-opacity=".15" stroke="{c}"/>'
                f'<text x="{lx}" y="{ly+10}" text-anchor="middle" font-family="{SANS}" font-size="27" font-weight="800" fill="{c}">₹</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)} — {esc(sub)}">
<title>{esc(label)}</title>
<defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}"/><stop offset=".45" stop-color="{c}" stop-opacity=".08"/><stop offset="1" stop-color="{c}"/>
<animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="5s" repeatCount="indefinite"/></linearGradient>
<radialGradient id="g" cx="15%" cy="50%" r="70%"><stop offset="0" stop-color="{c}" stop-opacity=".22"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="#07110f" stroke="url(#b)" stroke-width="2"/>
<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="url(#g)"/>
{logo}
<text x="100" y="58" font-family="{SANS}" font-size="20" font-weight="700" fill="#fff">{esc(label)}</text>
<text x="100" y="80" font-family="{MONO}" font-size="11.5" fill="{DIM}">{esc(sub)}</text>
<text x="{W-20}" y="{H-16}" text-anchor="end" font-family="{MONO}" font-size="16" fill="{c}">↗<animate attributeName="opacity" values=".4;1;.4" dur="1.8s" repeatCount="indefinite"/></text>
</svg>'''


# ============================================================ systems (product flight log)
SYSTEMS = [
    ("SYS-01", "Technician App", "Field ops run on people who are never at a desk.", "React Native · offline-first · PRD owner", "IN BUILD", AMBER),
    ("SYS-02", "Mappls Shop · Auto Billing", "Billing was done by hand. Found every hidden human decision.", "Angular · Razorpay · Odoo", "4× COLLECTIONS · −80% OPS", TEAL),
    ("SYS-03", "IOCL GeoRTD Pipeline", "30,000 routes: a pipeline you have to trust every run.", "Geospatial data · AWS S3", "30,000+ ROUTES", CYAN),
    ("SYS-04", "Vahan Shakti", "Keep the map useful when thousands of vehicles move at once.", "React · Mappls SDK · clustering", "200,000+ USERS", TEAL),
    ("SYS-05", "Intouch · Driver Safety", "Built for 10k vehicles, architected for 50k.", "DMS · ADAS · scorecards · PRD v1.0", "10,000+ VEHICLES", VIOLET),
]


def systems():
    W, rowH, top = 1200, 92, 70
    H = top + rowH * len(SYSTEMS) + 30
    rows = ""
    for i, (code, name, line, stack, res, c) in enumerate(SYSTEMS):
        y = top + i * rowH
        rows += f'''<g>
<animate attributeName="opacity" values="0.55;1;0.55" dur="{len(SYSTEMS)*1.6}s" begin="{i*1.6}s" repeatCount="indefinite" keyTimes="0;.1;1"/>
<rect x="40" y="{y}" width="{W-80}" height="{rowH-14}" rx="10" fill="#08120f" stroke="{LINE}"/>
<rect x="40" y="{y}" width="4" height="{rowH-14}" rx="2" fill="{c}"/>
<text x="66" y="{y+33}" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{c}">{code}</text>
<text x="160" y="{y+33}" font-family="{SANS}" font-size="20" font-weight="700" fill="#fff">{esc(name)}</text>
<text x="160" y="{y+58}" font-family="{SANS}" font-size="14" fill="#a9c9bf">{esc(line)}</text>
<text x="700" y="{y+33}" font-family="{MONO}" font-size="11.5" fill="{DIM}">{esc(stack)}</text>
<rect x="{W-330}" y="{y+42}" width="250" height="24" rx="12" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-opacity=".5"/>
<text x="{W-205}" y="{y+58}" text-anchor="middle" font-family="{MONO}" font-size="11.5" font-weight="700" fill="{c}">{esc(res)}</text>
<text x="{W-62}" y="{y+40}" text-anchor="end" font-family="{SANS}" font-size="18" fill="{c}">›</text>
</g>'''
    # scanning cursor that walks the list
    scan = f'<rect x="40" y="{top}" width="{W-80}" height="{rowH-14}" rx="10" fill="none" stroke="{TEAL}" stroke-width="1.5"><animate attributeName="y" values="{";".join(str(top+i*rowH) for i in range(len(SYSTEMS)))};{top}" dur="{len(SYSTEMS)*1.6}s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Five products I've shipped at MapmyIndia: Technician App, Mappls Shop automated billing (4x collections, 80% less ops work), IOCL GeoRTD pipeline (30,000+ routes), Vahan Shakti (200,000+ users), Intouch driver safety (10,000+ vehicles)">
<title>Systems on the route</title>
<rect width="{W}" height="{H}" rx="16" fill="{BG0}"/>
{corners(14, 14, W-28, H-28, op=.6)}
<text x="40" y="44" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">SYSTEMS · 05 ON THE ROUTE · ONE WORLD AT A TIME</text>
<circle cx="{W-52}" cy="40" r="5" fill="{TEAL}">{blink()}</circle>
<text x="{W-64}" y="44" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{TEAL}">LIVE</text>
{rows}{scan}
</svg>'''


# ============================================================ results in orbit ("every result has mass")
def orbit():
    W, H = 1200, 470
    cx, cy = 640, 285
    results = [("200,000+", "users", 230, 26, 40, TEAL), ("30,000+", "routes injected", 175, 19, 28, CYAN),
               ("20,000+", "vehicles monitored", 125, 16, 22, VIOLET), ("10,000+", "active vehicles", 300, 14, 52, AMBER),
               ("4×", "collections", 370, 12, 64, PINK)]
    s = ""
    for i, (n, l, r, size, dur, c) in enumerate(results):
        ry = r * 0.36
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry:.0f}" fill="none" stroke="{c}" stroke-opacity=".25" stroke-dasharray="3 6"/>'
        path = f"M{cx+r} {cy} A{r} {ry:.0f} 0 1 1 {cx-r} {cy} A{r} {ry:.0f} 0 1 1 {cx+r} {cy}"
        b = -i * dur / 5
        s += (f'<g><animateMotion dur="{dur}s" begin="{b:.1f}s" repeatCount="indefinite" path="{path}"/>'
              f'<circle r="{size}" fill="{c}" fill-opacity=".18" stroke="{c}"/><circle r="{size*0.45:.0f}" fill="{c}"/>'
              f'<text y="{-size-10}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="#fff">{n}</text>'
              f'<text y="{size+18}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{c}">{esc(l)}</text></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Results in orbit: 200,000+ users, 30,000+ routes injected, 20,000+ vehicles monitored, 10,000+ active vehicles, 4x collections">
<title>Every result has mass</title>
<defs>{glow("g2", 6)}<radialGradient id="core"><stop offset="0" stop-color="#fff"/><stop offset=".3" stop-color="{TEAL}"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient></defs>
<rect width="{W}" height="{H}" rx="16" fill="{BG0}"/>
{dust(W, H, 60)}
{corners(14, 14, W-28, H-28, op=.6)}
<text x="40" y="48" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">RESULTS · IN ORBIT</text>
<text x="40" y="82" font-family="{SANS}" font-size="28" font-weight="800" fill="#fff">Every result has mass.</text>
<text x="40" y="106" font-family="{SANS}" font-size="14" fill="{DIM}">What was measured, in orbit. Everything else curves toward it.</text>
<circle cx="{cx}" cy="{cy}" r="46" fill="url(#core)" filter="url(#g2)"><animate attributeName="r" values="40;50;40" dur="3s" repeatCount="indefinite"/></circle>
<text x="{cx}" y="{cy+5}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="{BG0}">PRODUCT</text>
{s}
</svg>'''


# ============================================================ product loop
def loop():
    W, H = 1200, 170
    steps = ["PROBLEM", "UNDERSTAND", "STRATEGY", "UX", "TECH", "BUILD", "SHIP", "LEARN"]
    n = len(steps)
    x0, x1, y = 80, 1120, 92
    gap = (x1 - x0) / (n - 1)
    s = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{LINE}" stroke-width="2"/>'
    s += f'<path d="M{x1} {y} C{x1+50} {y} {x1+50} {y+55} {x1-40} {y+55} L{x0+40} {y+55} C{x0-50} {y+55} {x0-50} {y} {x0} {y}" fill="none" stroke="{LINE}" stroke-dasharray="4 6"/>'
    dur = 8
    for i, t in enumerate(steps):
        x = x0 + i * gap
        b = i * dur / n * 0.82
        s += (f'<circle cx="{x:.0f}" cy="{y}" r="9" fill="{BG1}" stroke="{TEAL}" stroke-width="2"/>'
              f'<circle cx="{x:.0f}" cy="{y}" r="4" fill="{TEAL}" opacity=".25"><animate attributeName="opacity" values=".25;1;.25;.25" keyTimes="0;.05;.2;1" dur="{dur}s" begin="{b:.2f}s" repeatCount="indefinite"/></circle>'
              f'<text x="{x:.0f}" y="{y-24}" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="#cfe9e1">{t}</text>')
    path = f"M{x0} {y} L{x1} {y} C{x1+50} {y} {x1+50} {y+55} {x1-40} {y+55} L{x0+40} {y+55} C{x0-50} {y+55} {x0-50} {y} {x0} {y}"
    s += f'<g filter="url(#g3)"><circle r="6" fill="#fff"/><circle r="12" fill="{TEAL}" fill-opacity=".35"/><animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}" keyPoints="0;0.62;1" keyTimes="0;0.82;1" calcMode="linear"/></g>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="How I work: problem, understand, strategy, UX, technology, build, ship, learn — then the next problem">
<title>The loop I run</title>
<defs>{glow("g3", 4)}</defs>
<rect width="{W}" height="{H}" rx="16" fill="{BG0}"/>
<text x="40" y="36" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">FLIGHT RULES · THE LOOP I RUN ON EVERY PRODUCT</text>
<text x="{W/2:.0f}" y="{y+60}" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{DIM}">↺ NEXT PROBLEM</text>
{s}
</svg>'''


def label(text, w=1200):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="46" viewBox="0 0 {w} 46" role="img" aria-label="{esc(text)}">
<line x1="0" y1="23" x2="{w}" y2="23" stroke="{LINE}"/>
<rect y="21" width="160" height="4" rx="2" fill="{TEAL}" opacity=".9"><animate attributeName="x" values="-160;{w}" dur="5s" repeatCount="indefinite"/></rect>
<rect x="0" y="8" width="{len(text)*11+44:.0f}" height="30" fill="{BG0}"/>
<circle cx="10" cy="23" r="4" fill="{TEAL}">{blink()}</circle>
<text x="24" y="28" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{TEAL}">{esc(text)}</text>
</svg>'''


# ============================================================ terminal (whoami)
def terminal():
    W, H = 1200, 330
    lines = [
        ("$", "whoami", TEAL),
        (">", "Ali Azam Kazmi · product engineer → technical PM · New Delhi", "#d9fff3"),
        ("$", "cat philosophy.txt", TEAL),
        (">", "Ship the decision, not just the feature. Find the human hiding in the process.", "#d9fff3"),
        ("$", "ls ~/currently", TEAL),
        (">", "mapmyindia/  dumbmoney/  watchsense/  smaak.ux/  space-os/", AMBER),
        ("$", "./launch --next-problem", TEAL),
        (">", "▲ cleared for launch. open to PM / TPM roles.", PINK),
    ]
    T = 14.0
    body, defs = "", ""
    t = 0.4
    for i, (pr, txt, c) in enumerate(lines):
        y = 92 + i * 28
        wtxt = 24 + len(txt) * 8.45
        typing = pr == "$"
        d = max(0.5, len(txt) * 0.06) if typing else 0.15
        a, b = t / T, (t + d) / T
        defs += (f'<clipPath id="c{i}"><rect x="40" y="{y-18}" height="26" width="0">'
                 f'<animate attributeName="width" values="0;0;{wtxt:.0f};{wtxt:.0f};0" keyTimes="0;{a:.3f};{b:.3f};0.97;1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        col = TEAL if typing else DIM
        body += (f'<g clip-path="url(#c{i})"><text x="44" y="{y}" font-family="{MONO}" font-size="14" fill="{col}">{pr}</text>'
                 f'<text x="66" y="{y}" font-family="{MONO}" font-size="14" fill="{c}">{esc(txt)}</text></g>')
        t += d + (0.5 if typing else 0.9)
    cur_y = 92 + len(lines) * 28
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: whoami — Ali Azam Kazmi, product engineer moving into technical PM. Philosophy: ship the decision, not just the feature. Currently: MapmyIndia, DumbMoney, WatchSense, Smaak.ux, Space OS. Open to PM and TPM roles.">
<title>ali@space-os: whoami</title>
<defs>{defs}<linearGradient id="tb" x1="0" x2="1"><stop offset="0" stop-color="#0c1d19"/><stop offset="1" stop-color="#08120f"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="16" fill="{BG0}" stroke="{LINE}"/>
<rect width="{W}" height="44" rx="16" fill="url(#tb)"/><rect y="28" width="{W}" height="16" fill="#08120f"/>
<circle cx="30" cy="22" r="6" fill="#FF5F57"/><circle cx="50" cy="22" r="6" fill="#FEBC2E"/><circle cx="70" cy="22" r="6" fill="#28C840"/>
<text x="{W/2:.0f}" y="27" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{DIM}">ali@space-os: ~</text>
{body}
<rect x="44" y="{cur_y-14}" width="9" height="17" fill="{TEAL}">{blink(1)}</rect>
</svg>"""


# ============================================================ isometric skills city
def skills():
    W, H = 1200, 400
    data = [("TypeScript", 10, TEAL), ("UI/UX", 7, PINK), ("React", 7, CYAN), ("Mappls SDK", 4, AMBER), ("PRDs", 3, VIOLET)]
    ox, oy, cw = 790, 330, 64
    c30, s30 = math.cos(math.radians(30)), 0.5

    def P(x, y, z):
        return (ox + (x - y) * c30, oy + (x + y) * s30 - z)

    def pts(*ps):
        return " ".join(f"{a:.1f},{b:.1f}" for a, b in ps)

    floor = ""
    for i in range(-3, 4):
        a, b = P(i * cw - cw / 2, -3.5 * cw, 0), P(i * cw - cw / 2, 3.5 * cw, 0)
        floor += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{LINE}"/>'
        a, b = P(-3.5 * cw, i * cw - cw / 2, 0), P(3.5 * cw, i * cw - cw / 2, 0)
        floor += f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{LINE}"/>'
    blds, labels = "", ""
    pos = [(-2, -1), (-1, 0), (0, 1), (1, 2), (2, 3)]
    pos = [(-2.4, 0.6), (-1.2, 0.6), (0, 0.6), (1.2, 0.6), (2.4, 0.6)]
    for i, (name, n, c) in enumerate(data):
        gx, gy = pos[i][0] * cw * 1.05, -pos[i][0] * cw * 0.0 + (i - 2) * cw * 1.05
        gx, gy = (i - 2) * cw * 1.45, -(i - 2) * cw * 1.15
        h = 17 * n
        w = cw * 0.38
        x0, x1, y0, y1 = gx - w, gx + w, gy - w, gy + w

        def faces(hh):
            top = pts(P(x0, y0, hh), P(x1, y0, hh), P(x1, y1, hh), P(x0, y1, hh))
            left = pts(P(x0, y1, 0), P(x1, y1, 0), P(x1, y1, hh), P(x0, y1, hh))
            right = pts(P(x1, y0, 0), P(x1, y1, 0), P(x1, y1, hh), P(x1, y0, hh))
            return top, left, right
        t0, l0, r0 = faces(2)
        t1, l1, r1 = faces(h)
        dur, beg = 12, i * 0.3
        kt = "0;0.12;0.94;1"
        def anim(a, b):
            return f'<animate attributeName="points" values="{a};{b};{b};{a}" keyTimes="{kt}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite" calcMode="spline" keySplines=".2 .8 .2 1;0 0 1 1;.6 0 .8 .2"/>'
        lx, ly = P(gx, gy, h + 26)
        blds += (f'<polygon points="{l1}" fill="{c}" fill-opacity=".55">{anim(l0, l1)}</polygon>'
                 f'<polygon points="{r1}" fill="{c}" fill-opacity=".28">{anim(r0, r1)}</polygon>'
                 f'<polygon points="{t1}" fill="{c}" stroke="#ffffff" stroke-opacity=".35">{anim(t0, t1)}</polygon>')
        labels += (f'<g><animateTransform attributeName="transform" type="translate" values="0 {h-2};0 0;0 0;0 {h-2}" keyTimes="{kt}" dur="{dur}s" begin="{beg}s" repeatCount="indefinite" calcMode="spline" keySplines=".2 .8 .2 1;0 0 1 1;.6 0 .8 .2"/>'
                 f'<text x="{lx:.0f}" y="{ly-16:.0f}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="800" fill="#fff">{n}</text>'
                 f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{c}">{esc(name.upper())}</text></g>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Skills installed, as a 3D isometric city sized by number of projects: TypeScript 10, UI/UX 7, React 7, Mappls SDK 4, PRDs 3">
<title>Skills installed</title>
<rect width="{W}" height="{H}" rx="16" fill="{BG0}"/>
{dust(W, H, 40)}
{corners(14, 14, W-28, H-28, op=.6)}
<text x="40" y="48" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{DIM}">SKILLS INSTALLED · 5/5</text>
<text x="40" y="80" font-family="{SANS}" font-size="26" font-weight="800" fill="#fff">Built from what I actually ship.</text>
<text x="40" y="104" font-family="{SANS}" font-size="14" fill="{DIM}">Building height = number of projects that used it.</text>
{floor}{blds}{labels}
</svg>"""


# ============================================================ mission-style code cards
CODE = [
    ("sapceos", "BLD-01", "SPACE OS", "3D portfolio: a Three.js flight through my work", ["Next.js 16", "R3F", "GSAP"], TEAL),
    ("D3-Advance-Visuals", "BLD-02", "D3 Advanced Visuals", "D3 + Next.js engine for ops dashboards", ["D3.js", "TypeScript", "Zustand"], CYAN),
    ("sundar", "BLD-03", "Sunder Masala", "Heritage spice rebrand: 32 SKUs, SSG pages", ["Next.js 16", "Tailwind v4"], AMBER),
    ("casa", "BLD-04", "Wolf Casa", "Interiors showroom with 3D curated rooms", ["R3F", "Rapier", "GSAP"], TEAL),
    ("react-tech-loaders", "BLD-05", "React Tech Loaders", "Hacker-terminal, pixel & neon loaders", ["React", "TypeScript"], PINK),
    ("Honeypot-ssh", "BLD-06", "SSH Honeypot", "Fake shell that logs attacker commands", ["Python", "Paramiko", "Docker"], VIOLET),
]


def code_card(repo, code, title, desc, tags, c):
    W, H = 580, 170
    chips, x = "", 32
    for t in tags:
        w = 16 + len(t) * 7.4
        chips += (f'<rect x="{x}" y="118" width="{w:.0f}" height="24" rx="4" fill="{c}" fill-opacity=".08" stroke="{c}" stroke-opacity=".45"/>'
                  f'<text x="{x + w/2:.0f}" y="134" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{c}">{esc(t)}</text>')
        x += w + 8
    bars = "".join(f'<rect x="{W-150+k*14}" y="40" width="8" height="40" fill="{c}" opacity=".15"><animate attributeName="opacity" values=".15;.9;.15" dur="1.6s" begin="{k*0.15:.2f}s" repeatCount="indefinite"/></rect>' for k in range(8))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)} — {esc(desc)}">
<title>{esc(title)}</title>
<defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}"/><stop offset=".5" stop-color="{c}" stop-opacity=".05"/><stop offset="1" stop-color="{c}"/>
<animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="6s" repeatCount="indefinite"/></linearGradient></defs>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="#07110f" stroke="url(#b)" stroke-width="2"/>
{corners(10, 10, W-20, H-20, c=c, L=12, op=.5)}
<text x="32" y="44" font-family="{MONO}" font-size="11.5" letter-spacing="2.5" fill="{c}">{code} · {esc(repo)}</text>
<text x="32" y="78" font-family="{SANS}" font-size="24" font-weight="800" fill="#fff">{esc(title)}</text>
<text x="32" y="102" font-family="{SANS}" font-size="14" fill="#a9c9bf">{esc(desc)}</text>
{chips}
<text x="{W-28}" y="{H-26}" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{c}">OPEN ↗<animate attributeName="opacity" values=".4;1;.4" dur="1.8s" repeatCount="indefinite"/></text>
</svg>"""


write("mc-hero.svg", hero())
write("mc-terminal.svg", terminal())
write("mc-skills.svg", skills())
for r in CODE:
    write(f"mc-code-{r[0].lower()}.svg", code_card(*r))
write("mc-systems.svg", systems())
write("mc-orbit.svg", orbit())
write("mc-loop.svg", loop())
for slug, text in [("connect", "00 / OPEN CHANNEL"), ("systems", "01 / SYSTEMS I'VE SHIPPED"), ("results", "02 / RESULTS"),
                   ("loop", "03 / HOW I WORK"), ("ventures", "04 / VENTURES & STUDIO"), ("code", "05 / OPEN-SOURCE BUILDS"),
                   ("telemetry", "06 / TELEMETRY")]:
    write(f"mc-label-{slug}.svg", label(text))
for kind, lab, sub, c in [
    ("portfolio", "Space OS", "aliazamkazmi.vercel.app", TEAL),
    ("linkedin", "LinkedIn", "in/ali-azam-kazmi", "#0A66C2"),
    ("behance", "Behance", "behance.net/aliak8", "#1769FF"),
    ("figma", "Figma", "figma.com/@aliak", "#A259FF"),
    ("resume", "Résumé", "PDF · 1 page", AMBER),
    ("mail", "Email", "say hello", PINK),
    ("medium", "Medium", "@aliazamkazmi1291", "#cccccc"),
    ("dumbmoney", "DumbMoney", "Founder & CPO", TEAL),
]:
    write(f"mc-tile-{kind}.svg", tile(kind, lab, sub, c))
