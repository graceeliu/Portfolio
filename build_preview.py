#!/usr/bin/env python3
"""
build_preview.py — bundles the whole portfolio into one self-contained
preview.html so it can be viewed without a web server.

This is a PREVIEW ONLY. The real site is index.html + work/ + writing/ +
styles.css, and that's what you deploy. Nothing here needs to be committed.

Run from the portfolio/ directory:  python3 build_preview.py
"""

import re
import glob
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def route_for(path):
    """index.html -> home ; work/medcheck.html -> work/medcheck"""
    if path == "index.html":
        return "home"
    return os.path.splitext(path)[0]


def extract_main(html):
    m = re.search(r"<main>(.*?)</main>", html, re.S)
    return m.group(1) if m else ""


def extract_script(html):
    blocks = re.findall(r"<script>(.*?)</script>", html, re.S)
    return blocks[-1] if blocks else ""


def rewrite_links(body, page_dir):
    """Turn relative .html links into hash routes, and fix asset paths."""

    def sub(m):
        attr, href = m.group(1), m.group(2)
        if href.startswith(("http", "mailto:", "#/")):
            return m.group(0)

        # bare in-page anchor — leave alone
        if href.startswith("#"):
            return m.group(0)

        path, _, frag = href.partition("#")

        # stylesheet is inlined; drop the link
        if path.endswith(".css"):
            return 'href="#"'

        # assets keep a resolved path relative to the portfolio root
        if "/assets/" in path or path.startswith("assets/"):
            resolved = os.path.normpath(os.path.join(page_dir, path))
            return f'{attr}="{resolved}"'

        if path.endswith(".html"):
            resolved = os.path.normpath(os.path.join(page_dir, path))
            return f'{attr}="#/{route_for(resolved)}"'

        return m.group(0)

    return re.sub(r'(href)="([^"]+)"', sub, body)


pages = sorted(
    p for p in glob.glob("index.html")
    + glob.glob("work/*.html")
    + glob.glob("writing/*.html")
    if not p.endswith("preview.html")
)

routes = {}
home_script = ""

for p in pages:
    html = read(p)
    body = extract_main(html)
    body = rewrite_links(body, os.path.dirname(p))
    routes[route_for(p)] = body
    if p == "index.html":
        home_script = extract_script(html)

css = read("styles.css")

# The homepage grid is rendered by JS. Wrap its script in a function the
# router can call after injecting the home route's markup.
home_init = "function initHome(){\n" + home_script + "\n}"

route_js = ",\n".join(
    f"  {k!r}: {v!r}" for k, v in routes.items()
)

out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grace Liu — portfolio preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Source+Serif+4:ital,opsz,wght@0,8..60,200..700;1,8..60,200..700&display=swap" rel="stylesheet">
<style>
{css}

/* preview-only chrome */
.preview-banner {{
  background: var(--ink); color: var(--paper);
  font-family: var(--sans); font-size: .8125rem;
  padding: .5rem var(--gutter); text-align: center;
}}
.preview-banner b {{ font-weight: 620; }}
</style>
</head>
<body>

<div class="preview-banner">
  <b>Preview build</b> — all pages bundled into one file so it works without a server. PDF links won't open here.
</div>

<header class="masthead">
  <div class="masthead-inner">
    <a class="wordmark" href="#/home">Grace Liu</a>
    <nav aria-label="Primary">
      <a href="#/home">Work</a>
      <a href="#/home">About</a>
      <a href="mailto:grace20029@gmail.com">Contact</a>
    </nav>
  </div>
</header>

<main id="app"></main>

<footer class="foot">
  <div class="shell foot-inner">
    <span>Grace Liu — product &amp; UX research</span>
    <span><a href="mailto:grace20029@gmail.com">grace20029@gmail.com</a></span>
  </div>
</footer>

<script>
const ROUTES = {{
{route_js}
}};

{home_init}

function navigate() {{
  const hash = location.hash.replace(/^#\\//, "") || "home";
  const key = ROUTES[hash] !== undefined ? hash : "home";
  document.getElementById("app").innerHTML = ROUTES[key];
  if (key === "home") initHome();
  window.scrollTo(0, 0);
}}

window.addEventListener("hashchange", navigate);
navigate();
</script>

</body>
</html>
"""

with open(os.path.join(ROOT, "preview.html"), "w", encoding="utf-8") as f:
    f.write(out)

print(f"preview.html written — {len(routes)} pages bundled, {len(out)//1024} KB")
for k in routes:
    print(f"  #/{k}")
