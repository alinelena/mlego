# /// script
# dependencies = [
#     "pyyaml>=6.0",
#     "markdown>=3.6",
# ]
# ///
from pathlib import Path
import re
import yaml
import markdown

ROOT_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT_DIR / "notes"
NEWSITE_DIR = ROOT_DIR / "newsite"
DATA_DIR = NEWSITE_DIR / "data"

# YAML multiline string representation
def str_presenter(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

LINK_REPLACEMENTS = [
    ("m66.md", "m66.html"), ("m65.md", "m65.html"), ("m60.md", "m60.html"),
    ("m60_split.md", "m60_split.html"), ("m48.md", "m48.html"), ("m20.md", "m20.html"),
    ("m8.md", "m8.html"), ("m4.md", "m4.html"), ("tipro8x16.md", "tipro8x16.html"),
    ("tipro8x12.md", "tipro8x12.html"), ("tipro8x4.md", "tipro8x4.html"),
    ("tiproansi-ortho.md", "tiproansi-ortho.html"), ("tiproortho-ansi.md", "tiproortho-ansi.html"),
    ("prime.md", "prime.html"), ("assembly.md", "assembly.html"),
    ("notenoughpins.md", "notenoughpins.html"), ("how_matrix_works_extra.md", "how_matrix_works_extra.html"),
    ("hand5x5.md", "hand5x5.html"),
    ("keyboards/index.md", "keyboards.html"), ("converted/index.md", "converted.html"),
    ("mice/index.md", "mice.html"), ("extra/index.md", "guides.html"),
    ("index.md", "index.html"),
    ("https://mlego.elena.space/tipro8x16/", "tipro8x16.html"),
    ("https://mlego.elena.re/keyboards/", "keyboards.html"),
]

def clean_markdown_for_web(text: str) -> str:
    """Normalize image paths, links, and mkdocs syntax"""
    text = re.sub(r'\{:\s*[^}]+\}', '', text)
    text = re.sub(r'\{[.#][^}]+\}', '', text)
    text = re.sub(r'\((\.\./)+pics/', '(pics/', text)
    text = re.sub(r'\(\./pics/', '(pics/', text)
    for old, new in LINK_REPLACEMENTS:
        text = re.sub(rf'\]\((?:\.\./)?(?:keyboards/|converted/|mice/|extra/)?{re.escape(old)}\)', f']({new})', text)
        text = re.sub(rf'\]\({re.escape(old)}\)', f']({new})', text)
    text = re.sub(r':(?:material|octicons|fontawesome)-[a-z0-9-]+:', '', text)
    text = re.sub(r'^!!!\s+([a-zA-Z0-9_-]+)(?:\s+"([^"]+)")?', r'> **\2**\n>', text, flags=re.MULTILINE)
    return text.strip() + "\n"

def read_note(filename: str) -> str:
    file_path = NOTES_DIR / filename
    if file_path.exists():
        return clean_markdown_for_web(file_path.read_text(encoding="utf-8"))
    return ""

def md_to_html(md_text: str) -> str:
    """Convert cleaned markdown to semantic HTML"""
    return markdown.markdown(
        md_text,
        extensions=['extra', 'tables', 'fenced_code', 'toc', 'sane_lists']
    )

def render_head(title: str, description: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — mlego</title>
  <meta name="description" content="{description}">
  <meta name="author" content="Alin M. Elena">

  <!-- Favicons -->
  <link rel="shortcut icon" href="images/favicon.webp" type="image/webp">
  <link rel="icon" href="images/favicon.webp" type="image/webp">

  <!-- Google Fonts matching alin.elena.re -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anaheim&family=Cabin+Sketch:wght@700&family=Caveat:wght@500;600;700&family=JetBrains+Mono:wght@400;600&family=Kalam:wght@400;700&family=Permanent+Marker&family=Quattrocento+Sans:ital,wght@0,400;0,700;1,400&family=Rock+Salt&display=swap" rel="stylesheet">

  <!-- Bootstrap 5.3 CSS & Bootstrap Icons -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">

  <!-- Custom Dark Theme Styles matching alin.elena.re -->
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
"""

def render_corner_nav(active_id: str = "") -> str:
    def act(page_id: str) -> str:
        return " active" if active_id == page_id else ""
    def exp(group_id: str) -> str:
        return ' aria-expanded="true"' if active_id.startswith(group_id) else ' aria-expanded="false"'
    def show(group_id: str) -> str:
        return " show" if active_id.startswith(group_id) else ""

    return f"""
  <!-- Floating Corner Navigation Menu matching alin.elena.re -->
  <nav class="corner-nav-wrapper" aria-label="Site navigation">
    <button
      type="button"
      id="corner-menu-toggle"
      class="corner-menu-btn"
      aria-expanded="false"
      aria-controls="corner-menu-panel"
      aria-label="Toggle navigation menu"
    >
      <img id="corner-btn-logo" src="images/logo.webp" alt="mlego" class="brand-avatar">
      <span id="corner-current-section">Menu</span>
      <span class="menu-icon-bars" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
      </span>
    </button>

    <div id="corner-menu-panel" class="corner-menu-panel" role="menu">
      <div class="d-flex align-items-center justify-content-between px-2 pb-2 mb-2 border-bottom border-secondary border-opacity-25">
        <span class="fw-bold text-white small text-uppercase" style="letter-spacing: 0.06em;">mlego Navigation</span>
        <span class="badge bg-dark text-info border border-info border-opacity-25">mlego.elena.re</span>
      </div>
      <ul id="corner-nav-list" class="corner-nav-list">
        <li>
          <a href="index.html" class="corner-nav-link{act('home')}" style="--nav-item-color: #57cbcc;">
            <i class="bi bi-house-door"></i> Home
          </a>
        </li>
        <li>
          <a href="about.html" class="corner-nav-link{act('about')}" style="--nav-item-color: #2dd4bf;">
            <i class="bi bi-info-circle"></i> About
          </a>
        </li>

        <!-- Keyboards Submenu -->
        <li>
          <button type="button" class="corner-nav-link corner-nav-group-toggle"{exp('keyboard')} style="--nav-item-color: #6cb670;">
            <i class="bi bi-keyboard"></i> Keyboards <i class="bi bi-chevron-down chevron-icon"></i>
          </button>
          <ul class="corner-subnav-list{show('keyboard')}">
            <li><a href="keyboards.html" class="corner-nav-link{act('keyboards')}">All Keyboards</a></li>
            <li><a href="m66.html" class="corner-nav-link{act('m66')}">m66 (5×14)</a></li>
            <li><a href="m65.html" class="corner-nav-link{act('m65')}">m65 (5×13)</a></li>
            <li><a href="m60.html" class="corner-nav-link{act('m60')}">m60 (5×12)</a></li>
            <li><a href="m60_split.html" class="corner-nav-link{act('m60_split')}">m60 Split</a></li>
            <li><a href="m48.html" class="corner-nav-link{act('m48')}">m48 (4×12)</a></li>
            <li><a href="m20.html" class="corner-nav-link{act('m20')}">m20 (5×4)</a></li>
            <li><a href="m8.html" class="corner-nav-link{act('m8')}">m8 (2×4)</a></li>
            <li><a href="m4.html" class="corner-nav-link{act('m4')}">m4 (2×2)</a></li>
          </ul>
        </li>

        <!-- POS Conversions Submenu -->
        <li>
          <button type="button" class="corner-nav-link corner-nav-group-toggle"{exp('converted')} style="--nav-item-color: #fbbf24;">
            <i class="bi bi-cpu"></i> POS Conversions <i class="bi bi-chevron-down chevron-icon"></i>
          </button>
          <ul class="corner-subnav-list{show('converted')}">
            <li><a href="converted.html" class="corner-nav-link{act('converted')}">All Conversions</a></li>
            <li><a href="tipro8x16.html" class="corner-nav-link{act('tipro8x16')}">Tipro 8×16</a></li>
            <li><a href="tipro8x12.html" class="corner-nav-link{act('tipro8x12')}">Tipro 8×12</a></li>
            <li><a href="tipro8x4.html" class="corner-nav-link{act('tipro8x4')}">Tipro 8×4</a></li>
            <li><a href="tiproansi-ortho.html" class="corner-nav-link{act('tiproansi-ortho')}">Tipro ANSI-Ortho</a></li>
            <li><a href="tiproortho-ansi.html" class="corner-nav-link{act('tiproortho-ansi')}">Tipro Ortho-ANSI</a></li>
          </ul>
        </li>

        <!-- Mice Submenu -->
        <li>
          <button type="button" class="corner-nav-link corner-nav-group-toggle"{exp('mice')} style="--nav-item-color: #818cf8;">
            <i class="bi bi-mouse"></i> QMK Mice <i class="bi bi-chevron-down chevron-icon"></i>
          </button>
          <ul class="corner-subnav-list{show('mice')}">
            <li><a href="mice.html" class="corner-nav-link{act('mice')}">All Mice</a></li>
            <li><a href="prime.html" class="corner-nav-link{act('prime')}">SteelSeries Prime</a></li>
          </ul>
        </li>

        <!-- Guides Submenu -->
        <li>
          <button type="button" class="corner-nav-link corner-nav-group-toggle"{exp('guide')} style="--nav-item-color: #f472b6;">
            <i class="bi bi-journal-code"></i> Build Guides <i class="bi bi-chevron-down chevron-icon"></i>
          </button>
          <ul class="corner-subnav-list{show('guide')}">
            <li><a href="guides.html" class="corner-nav-link{act('guides')}">All Guides</a></li>
            <li><a href="assembly.html" class="corner-nav-link{act('assembly')}">Assembly Guide</a></li>
            <li><a href="notenoughpins.html" class="corner-nav-link{act('notenoughpins')}">Not Enough Pins</a></li>
            <li><a href="how_matrix_works_extra.html" class="corner-nav-link{act('how_matrix_works_extra')}">How Matrix Works</a></li>
            <li><a href="hand5x5.html" class="corner-nav-link{act('hand5x5')}">Handwire Helpers</a></li>
          </ul>
        </li>

        <li>
          <a href="specs.html" class="corner-nav-link{act('specs')}" style="--nav-item-color: #fb923c;">
            <i class="bi bi-table"></i> Lineup Specs
          </a>
        </li>

        <li class="border-top border-secondary border-opacity-25 pt-2 mt-1">
          <a href="https://alin.elena.re" target="_blank" rel="noopener" class="corner-nav-link" style="--nav-item-color: #57cbcc;">
            <i class="bi bi-globe2"></i> Alin's Main Site
          </a>
        </li>
      </ul>
    </div>
  </nav>
"""

def render_footer() -> str:
    return """
  <!-- Footer matching alin.elena.re -->
  <footer class="py-5 border-top border-secondary border-opacity-25 text-center mt-5" style="background-color: #0b0e12;">
    <div class="container">
      <div class="d-flex align-items-center justify-content-center gap-2 mb-3">
        <img src="images/logo.webp" alt="mlego" style="width: 32px; height: 32px; border-radius: 50%;">
        <span class="fw-bold text-white fs-5" style="font-family: 'Anaheim', sans-serif;">mlego notes</span>
      </div>
      <p class="text-secondary small mb-3">
        Modular LEGO-mounted ortholinear keyboards, QMK/ZMK firmware, POS conversions, and hardware build notes.
      </p>
      <div class="d-flex justify-content-center gap-3 mb-4">
        <a href="https://gitlab.com/m-lego" target="_blank" rel="noopener" class="text-secondary hover-white fs-5"><i class="bi bi-git"></i></a>
        <a href="https://github.com/alinelena" target="_blank" rel="noopener" class="text-secondary hover-white fs-5"><i class="bi bi-github"></i></a>
        <a href="https://alin.elena.re" target="_blank" rel="noopener" class="text-secondary hover-white fs-5"><i class="bi bi-globe"></i></a>
        <a href="https://ddmms.elena.re" target="_blank" rel="noopener" class="text-secondary hover-white fs-5"><i class="bi bi-building"></i></a>
      </div>
      <div class="text-muted small">
        Copyright &copy; 2017&ndash;2026 <a href="https://alin.elena.re" class="text-info">Alin M. Elena</a>. All rights reserved.
      </div>
    </div>
  </footer>

  <!-- Lightbox Overlay for Image Zoom -->
  <div id="lightbox-overlay" class="lightbox-overlay" role="dialog" aria-modal="true" aria-label="Image Preview">
    <img id="lightbox-img" class="lightbox-img" src="" alt="Hardware Preview">
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script src="assets/js/app.js"></script>
</body>
</html>
"""

def generate_detail_page(item: dict, parent_title: str, parent_url: str, active_nav: str):
    html_content = md_to_html(item.get("content", ""))
    page_title = item.get("title", "")
    page_id = item.get("id", "")
    badge = item.get("badge", "")
    keys = item.get("keys", "")
    mcu = item.get("mcu", "")
    fw = item.get("firmware", "")
    image = item.get("image", "pics/mlego.webp")
    summary = item.get("summary", "")

    page_html = render_head(page_title, summary)
    page_html += render_corner_nav(active_nav)
    page_html += f"""
  <!-- Subpage Header -->
  <header class="py-5 border-bottom border-secondary border-opacity-25" style="background: linear-gradient(180deg, #161c24 0%, #0f1318 100%);">
    <div class="container pt-4">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb mb-2 small">
          <li class="breadcrumb-item"><a href="index.html" class="text-decoration-none text-info">Home</a></li>
          <li class="breadcrumb-item"><a href="{parent_url}" class="text-decoration-none text-info">{parent_title}</a></li>
          <li class="breadcrumb-item active text-secondary" aria-current="page">{page_title}</li>
        </ol>
      </nav>
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mt-2">
        <div>
          <h1 class="h2 text-white fw-bold mb-2" style="font-family: 'Anaheim', sans-serif;">{page_title}</h1>
          <div class="d-flex flex-wrap gap-2 align-items-center">
            {f'<span class="mlego-badge">{badge}</span>' if badge else ''}
            {f'<span class="badge bg-dark text-secondary border border-secondary border-opacity-25">{keys} Keys</span>' if keys else ''}
            {f'<span class="badge bg-dark text-info border border-info border-opacity-25"><i class="bi bi-cpu me-1"></i>{mcu}</span>' if mcu else ''}
            {f'<span class="badge bg-dark text-success border border-success border-opacity-25"><i class="bi bi-code-slash me-1"></i>{fw}</span>' if fw else ''}
          </div>
        </div>
        <div>
          <a href="{parent_url}" class="btn btn-sm btn-ddmms-outline">
            <i class="bi bi-arrow-left me-1"></i> All {parent_title}
          </a>
        </div>
      </div>
    </div>
  </header>

  <main class="py-5">
    <div class="container">
      <div class="row g-4">
        <div class="col-lg-8">
          <div class="surface-card p-4 p-md-5">
            <div class="modal-article-body">
              {html_content}
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="sticky-top" style="top: 2rem;">
            <div class="surface-card p-4 mb-4">
              <div class="hardware-card-thumb-wrap mb-3 rounded" style="height: 200px;">
                <img src="{image}" alt="{page_title}" class="hardware-card-thumb" style="cursor: zoom-in;" onclick="openLightbox('{image}')">
              </div>
              <h3 class="h5 text-white mb-3" style="font-family: 'Anaheim', sans-serif;">Quick Specs</h3>
              <ul class="list-unstyled small text-secondary mb-3" style="line-height: 2;">
                {f'<li><strong class="text-white">Layout:</strong> {badge}</li>' if badge else ''}
                {f'<li><strong class="text-white">Keys:</strong> {keys}</li>' if keys else ''}
                {f'<li><strong class="text-white">MCU:</strong> {mcu}</li>' if mcu else ''}
                {f'<li><strong class="text-white">Firmware:</strong> {fw}</li>' if fw else ''}
              </ul>
              {f'<p class="small text-secondary mb-3">{summary}</p>' if summary else ''}
              <div class="d-grid gap-2">
                <a href="https://gitlab.com/m-lego" target="_blank" rel="noopener" class="btn btn-sm btn-ddmms-primary text-center">
                  <i class="bi bi-git me-1"></i> View Hardware Repo
                </a>
                <a href="{parent_url}" class="btn btn-sm btn-ddmms-outline text-center">
                  <i class="bi bi-grid me-1"></i> Browse More {parent_title}
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
"""
    page_html += render_footer()
    (NEWSITE_DIR / f"{page_id}.html").write_text(page_html, encoding="utf-8")

def generate_catalog_page(category_id: str, title: str, subtitle: str, items: list, accent_color: str):
    page_html = render_head(title, subtitle)
    page_html += render_corner_nav(category_id)
    page_html += f"""
  <!-- Catalog Header -->
  <header class="py-5 border-bottom border-secondary border-opacity-25" style="background: linear-gradient(180deg, #161c24 0%, #0f1318 100%);">
    <div class="container pt-4">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb mb-2 small">
          <li class="breadcrumb-item"><a href="index.html" class="text-decoration-none text-info">Home</a></li>
          <li class="breadcrumb-item active text-secondary" aria-current="page">{title}</li>
        </ol>
      </nav>
      <div class="section-header text-start mb-0" style="--section-accent: {accent_color};">
        <h1 class="h2 text-white fw-bold mb-2" style="font-family: 'Anaheim', sans-serif;">
          <span style="color: {accent_color};">{title.split()[0]}</span> {' '.join(title.split()[1:])}
        </h1>
        <p class="text-secondary mb-0">{subtitle}</p>
      </div>
    </div>
  </header>

  <main class="py-5">
    <div class="container">
      <!-- Search Filter Box -->
      <div class="search-filter-box mb-4">
        <div class="search-input-group">
          <i class="bi bi-search"></i>
          <input type="text" id="search-input" class="search-input" placeholder="Filter by name, layout, MCU platform, or keyword...">
        </div>
      </div>

      <div class="row" id="catalog-grid">
"""
    for item in items:
        badge = item.get("badge", "")
        keys = item.get("keys", "")
        mcu = item.get("mcu", "")
        fw = item.get("firmware", "")
        item_id = item.get("id", "")
        item_title = item.get("title", "")
        summary = item.get("summary", "")
        image = item.get("image", "pics/mlego.webp")

        page_html += f"""
        <div class="col-lg-4 col-md-6 mb-4 card-item" data-search="{(item_title + ' ' + (mcu or '') + ' ' + (badge or '') + ' ' + (summary or '')).lower()}">
          <div class="hardware-card">
            <div class="hardware-card-thumb-wrap">
              <a href="{item_id}.html">
                <img src="{image}" alt="{item_title}" class="hardware-card-thumb" loading="lazy">
              </a>
            </div>
            <div class="hardware-card-body">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <span class="mlego-badge" style="color: {accent_color}; border-color: {accent_color}55;">{badge}</span>
                {f'<span class="badge bg-dark text-secondary border border-secondary border-opacity-25">{keys} Keys</span>' if keys else ''}
              </div>
              <h2 class="h5 hardware-card-title mb-2">
                <a href="{item_id}.html" class="text-white text-decoration-none">{item_title}</a>
              </h2>
              <div class="hardware-card-specs mb-2">
                {f'<span class="badge bg-dark text-info border border-info border-opacity-25"><i class="bi bi-cpu me-1"></i>{mcu}</span>' if mcu else ''}
                {f'<span class="badge bg-dark text-success border border-success border-opacity-25"><i class="bi bi-code-slash me-1"></i>{fw}</span>' if fw else ''}
              </div>
              <p class="hardware-card-desc">{summary}</p>
              <div class="mt-auto pt-2 border-top border-secondary border-opacity-25 d-flex align-items-center justify-content-between">
                <a href="{item_id}.html" class="btn btn-sm btn-ddmms-primary text-decoration-none">
                  <i class="bi bi-book me-1"></i> View Documentation
                </a>
                <button type="button" class="btn btn-sm btn-outline-secondary" onclick="openLightbox('{image}')">
                  <i class="bi bi-zoom-in"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
"""
    page_html += """
      </div>
    </div>
  </main>
"""
    page_html += render_footer()
    (NEWSITE_DIR / f"{category_id}.html").write_text(page_html, encoding="utf-8")

def generate_about_page(about_data: dict):
    html_content = md_to_html(about_data.get("content", ""))
    page_html = render_head("About Project & Manifesto", "Project overview, philosophy, and history of mlego keyboards")
    page_html += render_corner_nav("about")
    page_html += f"""
  <header class="py-5 border-bottom border-secondary border-opacity-25" style="background: linear-gradient(180deg, #161c24 0%, #0f1318 100%);">
    <div class="container pt-4">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb mb-2 small">
          <li class="breadcrumb-item"><a href="index.html" class="text-decoration-none text-info">Home</a></li>
          <li class="breadcrumb-item active text-secondary" aria-current="page">About Project</li>
        </ol>
      </nav>
      <div class="section-header text-start mb-0" style="--section-accent: #2dd4bf;">
        <h1 class="h2 text-white fw-bold mb-2" style="font-family: 'Anaheim', sans-serif;">
          <span style="color: #2dd4bf;">Project</span> Overview &amp; Manifesto
        </h1>
        <p class="text-secondary mb-0">Open-source modular hardware, KiCad engineering, and QMK/ZMK firmware playground</p>
      </div>
    </div>
  </header>

  <main class="py-5">
    <div class="container">
      <div class="row g-4 mb-5">
"""
    for s in about_data.get("stats", []):
        page_html += f"""
        <div class="col-6 col-lg-3">
          <div class="stat-card">
            <i class="bi {s['icon']} stat-icon" style="color: {s['color']};"></i>
            <div class="stat-count">{s['count']}</div>
            <div class="stat-label">{s['label']}</div>
          </div>
        </div>
"""
    page_html += f"""
      </div>

      <div class="surface-card p-4 p-md-5">
        <div class="modal-article-body">
          {html_content}
        </div>
      </div>
    </div>
  </main>
"""
    page_html += render_footer()
    (NEWSITE_DIR / "about.html").write_text(page_html, encoding="utf-8")

def generate_specs_page(specs_data: dict):
    page_html = render_head("Hardware Comparison Lineup", "Full side-by-side specifications for all mlego keyboards and conversions")
    page_html += render_corner_nav("specs")
    page_html += """
  <header class="py-5 border-bottom border-secondary border-opacity-25" style="background: linear-gradient(180deg, #161c24 0%, #0f1318 100%);">
    <div class="container pt-4">
      <nav aria-label="breadcrumb">
        <ol class="breadcrumb mb-2 small">
          <li class="breadcrumb-item"><a href="index.html" class="text-decoration-none text-info">Home</a></li>
          <li class="breadcrumb-item active text-secondary" aria-current="page">Lineup Specs</li>
        </ol>
      </nav>
      <div class="section-header text-start mb-0" style="--section-accent: #fb923c;">
        <h1 class="h2 text-white fw-bold mb-2" style="font-family: 'Anaheim', sans-serif;">
          <span style="color: #fb923c;">Hardware</span> Comparison Lineup
        </h1>
        <p class="text-secondary mb-0">Comprehensive specifications for all mlego keyboards, macropads, and converted terminals</p>
      </div>
    </div>
  </header>

  <main class="py-5">
    <div class="container">
      <div class="specs-table-wrapper table-responsive">
        <table class="specs-table">
          <thead>
            <tr>
              <th>Model</th>
              <th>Layout</th>
              <th>Keys</th>
              <th>MCU Platform</th>
              <th>Key Features &amp; Peripherals</th>
              <th>Firmware</th>
              <th>Documentation</th>
            </tr>
          </thead>
          <tbody>
"""
    for row in specs_data.get("items", []):
        page_html += f"""
            <tr>
              <td class="fw-bold text-white"><a href="{row['id']}.html" class="text-info text-decoration-none">{row['name']}</a></td>
              <td><span class="mlego-badge">{row['layout']}</span></td>
              <td><span class="badge bg-dark text-light border border-secondary border-opacity-25">{row['keys']}</span></td>
              <td class="small text-secondary">{row['mcu']}</td>
              <td class="small text-light">{row['features']}</td>
              <td><span class="badge bg-dark text-success border border-success border-opacity-25">{row['firmware']}</span></td>
              <td>
                <a href="{row['id']}.html" class="btn btn-sm btn-ddmms-outline py-1 px-2 text-decoration-none">
                  <i class="bi bi-file-text me-1"></i> View Page
                </a>
              </td>
            </tr>
"""
    page_html += """
          </tbody>
        </table>
      </div>
    </div>
  </main>
"""
    page_html += render_footer()
    (NEWSITE_DIR / "specs.html").write_text(page_html, encoding="utf-8")

def generate_landing_page(keyboards_data, converted_data, mice_data, guides_data, specs_data):
    page_html = render_head("Modular LEGO Ortholinear Keyboards & Hardware Notes", "Custom ISO-friendly ortholinear mechanical keyboards, macropads, vintage POS terminal conversions, and QMK/ZMK firmware — all mounted in modular LEGO cases.")
    page_html += render_corner_nav("home")
    page_html += """
  <!-- Hero / Landing Section -->
  <header>
    <section id="hero" class="hero-section parallax-window" data-parallax-speed="0.42">
      <div class="parallax-bg" id="hero-parallax-bg" style="background-image: url('images/backgrounds/exterior-stone-wall.webp');"></div>
      <div id="hero-content" class="hero-content container">
        <div class="hero-pulse-badge">
          <img src="images/logo.webp" alt="mlego logo">
        </div>
        <h1 class="hero-title">mlego notes</h1>
        <p class="hero-subtitle">Modular LEGO Ortholinear Keyboards <span class="hero-bullet">•</span> Hardware &amp; QMK/ZMK Firmware</p>
        
        <p class="text-secondary mt-3 mb-4 mx-auto" style="max-width: 680px; font-size: 1.05rem;">
          Custom ISO-friendly ortholinear mechanical keyboards, macropads, vintage POS terminal conversions, and firmware experiments — all mounted in modular LEGO cases.
        </p>

        <!-- CTAs & Social Links -->
        <div class="d-flex flex-wrap justify-content-center align-items-center gap-2 mb-4">
          <a href="keyboards.html" class="btn-ddmms-primary text-decoration-none">
            <i class="bi bi-keyboard"></i> Explore Keyboards
          </a>
          <a href="guides.html" class="btn-ddmms-outline text-decoration-none">
            <i class="bi bi-tools"></i> Build Guides
          </a>
          <a href="https://gitlab.com/m-lego/m65" target="_blank" rel="noopener" class="btn-social-pill" style="--pill-color: #fc6d26;">
            <i class="bi bi-git"></i> GitLab
          </a>
          <a href="https://github.com/alinelena" target="_blank" rel="noopener" class="btn-social-pill" style="--pill-color: #c9d1d9;">
            <i class="bi bi-github"></i> GitHub
          </a>
          <a href="https://alin.elena.re" target="_blank" rel="noopener" class="btn-social-pill" style="--pill-color: #57cbcc;">
            <i class="bi bi-globe"></i> alin.elena.re
          </a>
        </div>

        <div class="mt-4">
          <a href="#about-overview" class="scroll-down-btn text-decoration-none">
            <span>Discover</span>
            <i class="bi bi-chevron-down"></i>
          </a>
        </div>
      </div>
    </section>
  </header>

  <main>
    <!-- About Overview -->
    <section id="about-overview" class="section-block reveal-section">
      <div class="container">
        <div class="section-header" style="--section-accent: #2dd4bf;">
          <h2 class="section-title">
            <span class="section-title-highlight" style="color: #2dd4bf;">Project</span> <span class="text-white">Overview</span>
          </h2>
          <p class="text-secondary mb-2">Fun, modular, open-source electronics &amp; mechanical keyboard playground</p>
          <div class="section-divider"></div>
        </div>

        <div class="row g-4 mb-5">
          <div class="col-6 col-lg-3">
            <div class="stat-card">
              <i class="bi bi-keyboard stat-icon"></i>
              <div class="stat-count">8</div>
              <div class="stat-label">Keyboards Designed</div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card">
              <i class="bi bi-clock-history stat-icon" style="color: #6cb670;"></i>
              <div class="stat-count">11</div>
              <div class="stat-label">m65 Hardware Revisions</div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card">
              <i class="bi bi-cpu stat-icon" style="color: #fbbf24;"></i>
              <div class="stat-count">5</div>
              <div class="stat-label">POS Terminals Converted</div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="stat-card">
              <i class="bi bi-code-slash stat-icon" style="color: #818cf8;"></i>
              <div class="stat-count">100%</div>
              <div class="stat-label">Open Source HW &amp; FW</div>
            </div>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-lg-6">
            <div class="surface-card">
              <div class="card-icon-badge" style="background: rgba(108, 182, 112, 0.12); color: #6cb670; border-color: rgba(108, 182, 112, 0.3);">
                <i class="bi bi-check-circle"></i>
              </div>
              <h3 class="h4 text-white mb-3">What This Project Is</h3>
              <ul class="text-secondary ps-3 mb-0" style="line-height: 1.8;">
                <li><strong class="text-light">Fun &amp; experimental</strong> — designed for learning electronics, KiCad routing, and firmware architecture.</li>
                <li><strong class="text-light">Educational</strong> — documented schematics, SPI shift-register matrix expansion, and QMK/ZMK configs.</li>
                <li><strong class="text-light">Functional daily drivers</strong> — full ISO keycap compatibility on comfortable ortholinear grids.</li>
                <li><strong class="text-light">Modular LEGO Cases</strong> — PCBs drilled to official LEGO stud pitch (1.6mm), snapping onto standard LEGO plates.</li>
              </ul>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="surface-card">
              <div class="card-icon-badge" style="background: rgba(251, 146, 60, 0.12); color: #fb923c; border-color: rgba(251, 146, 60, 0.3);">
                <i class="bi bi-lightbulb"></i>
              </div>
              <h3 class="h4 text-white mb-3">Maker Playground, Not Commercial Endgame</h3>
              <p class="text-secondary" style="line-height: 1.75;">
                This project is an evolving maker journey rather than a static commercial kit. Every revision explores a new microcontroller (STM32, RP2040, nRF52840), display technology (OLED, WeAct e-ink, Sharp Memory, ST7735 IPS LCD), or matrix scanning circuit.
              </p>
              <div class="mt-auto pt-2">
                <a href="about.html" class="btn btn-sm btn-ddmms-outline text-decoration-none">
                  <i class="bi bi-file-earmark-text me-1"></i> Read Full Story &amp; Manifesto
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Parallax Divider 1 -->
    <div class="parallax-band parallax-window" data-parallax-speed="0.38">
      <div class="parallax-bg" style="background-image: url('images/backgrounds/old-brick-wall.webp');"></div>
    </div>

    <!-- Featured Keyboards Preview -->
    <section class="section-block section-bg-alt reveal-section">
      <div class="container">
        <div class="section-header" style="--section-accent: #6cb670;">
          <h2 class="section-title">
            <span class="section-title-highlight" style="color: #6cb670;">Designed</span> <span class="text-white">Keyboards</span>
          </h2>
          <p class="text-secondary mb-2">Flagship ortholinear keyboards in modular LEGO enclosures</p>
          <div class="section-divider"></div>
        </div>

        <div class="row">
"""
    # Preview top 3 keyboards on landing page
    for item in keyboards_data.get("items", [])[:3]:
        page_html += f"""
          <div class="col-lg-4 col-md-6 mb-4">
            <div class="hardware-card">
              <div class="hardware-card-thumb-wrap">
                <a href="{item['id']}.html">
                  <img src="{item['image']}" alt="{item['title']}" class="hardware-card-thumb" loading="lazy">
                </a>
              </div>
              <div class="hardware-card-body">
                <div class="d-flex align-items-center justify-content-between mb-2">
                  <span class="mlego-badge mlego-badge--green">{item['badge']}</span>
                  <span class="badge bg-dark text-secondary border border-secondary border-opacity-25">{item['keys']} Keys</span>
                </div>
                <h3 class="h5 hardware-card-title mb-2">
                  <a href="{item['id']}.html" class="text-white text-decoration-none">{item['title']}</a>
                </h3>
                <p class="hardware-card-desc">{item['summary']}</p>
                <div class="mt-auto pt-2 border-top border-secondary border-opacity-25">
                  <a href="{item['id']}.html" class="btn btn-sm btn-ddmms-primary text-decoration-none w-100 text-center">
                    <i class="bi bi-book me-1"></i> Read Documentation
                  </a>
                </div>
              </div>
            </div>
          </div>
"""
    page_html += """
        </div>

        <div class="text-center mt-3">
          <a href="keyboards.html" class="btn btn-ddmms-outline text-decoration-none">
            <i class="bi bi-grid me-1"></i> Explore All 8 Designed Keyboards &rarr;
          </a>
        </div>
      </div>
    </section>

    <!-- Parallax Divider 2 -->
    <div class="parallax-band parallax-window" data-parallax-speed="0.38">
      <div class="parallax-bg" style="background-image: url('images/backgrounds/stone-wall.webp');"></div>
    </div>

    <!-- Quick Navigation Hub -->
    <section class="section-block reveal-section">
      <div class="container">
        <div class="section-header" style="--section-accent: #fbbf24;">
          <h2 class="section-title">
            <span class="section-title-highlight" style="color: #fbbf24;">Hardware</span> <span class="text-white">Directory</span>
          </h2>
          <p class="text-secondary mb-2">Dedicated sections for POS conversions, mice liberation, and electronics build notes</p>
          <div class="section-divider"></div>
        </div>

        <div class="row g-4">
          <div class="col-md-4">
            <div class="surface-card text-center p-4">
              <div class="card-icon-badge mx-auto" style="background: rgba(251, 191, 36, 0.12); color: #fbbf24; border-color: rgba(251, 191, 36, 0.3);">
                <i class="bi bi-cpu"></i>
              </div>
              <h3 class="h5 text-white mb-2">Vintage POS Conversions</h3>
              <p class="small text-secondary mb-3">Vintage Tipro mechanical point-of-sale terminals restored with custom STM32 daughterboards.</p>
              <a href="converted.html" class="btn btn-sm btn-ddmms-outline text-decoration-none">
                <i class="bi bi-arrow-right me-1"></i> 5 Tipro Models
              </a>
            </div>
          </div>

          <div class="col-md-4">
            <div class="surface-card text-center p-4">
              <div class="card-icon-badge mx-auto" style="background: rgba(129, 140, 248, 0.12); color: #818cf8; border-color: rgba(129, 140, 248, 0.3);">
                <i class="bi bi-mouse"></i>
              </div>
              <h3 class="h5 text-white mb-2">Liberated QMK Mice</h3>
              <p class="small text-secondary mb-3">SteelSeries Prime gaming mouse unlocked via OpenOCD, custom UF2 bootloader, and QMK.</p>
              <a href="mice.html" class="btn btn-sm btn-ddmms-outline text-decoration-none">
                <i class="bi bi-arrow-right me-1"></i> Prime Guide
              </a>
            </div>
          </div>

          <div class="col-md-4">
            <div class="surface-card text-center p-4">
              <div class="card-icon-badge mx-auto" style="background: rgba(244, 114, 182, 0.12); color: #f472b6; border-color: rgba(244, 114, 182, 0.3);">
                <i class="bi bi-journal-code"></i>
              </div>
              <h3 class="h5 text-white mb-2">Hardware &amp; Build Guides</h3>
              <p class="small text-secondary mb-3">Assembly guides, SPI shift-register matrix expansion, 3×3 KiCad matrix tutorial, and breakout PCBs.</p>
              <a href="guides.html" class="btn btn-sm btn-ddmms-outline text-decoration-none">
                <i class="bi bi-arrow-right me-1"></i> 4 Build Guides
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Parallax Divider 3 -->
    <div class="parallax-band parallax-window" data-parallax-speed="0.38">
      <div class="parallax-bg" style="background-image: url('images/backgrounds/stones.webp');"></div>
    </div>

    <!-- Lineup Comparison Preview -->
    <section class="section-block section-bg-alt reveal-section">
      <div class="container">
        <div class="section-header" style="--section-accent: #fb923c;">
          <h2 class="section-title">
            <span class="section-title-highlight" style="color: #fb923c;">Lineup</span> <span class="text-white">Comparison</span>
          </h2>
          <p class="text-secondary mb-2">Quick side-by-side specs overview</p>
          <div class="section-divider"></div>
        </div>

        <div class="specs-table-wrapper table-responsive mb-4">
          <table class="specs-table">
            <thead>
              <tr>
                <th>Model</th>
                <th>Layout</th>
                <th>Keys</th>
                <th>MCU Platform</th>
                <th>Firmware</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
"""
    for row in specs_data.get("items", [])[:6]:
        page_html += f"""
              <tr>
                <td class="fw-bold text-white"><a href="{row['id']}.html" class="text-info text-decoration-none">{row['name']}</a></td>
                <td><span class="mlego-badge">{row['layout']}</span></td>
                <td><span class="badge bg-dark text-light border border-secondary border-opacity-25">{row['keys']}</span></td>
                <td class="small text-secondary">{row['mcu']}</td>
                <td><span class="badge bg-dark text-success border border-success border-opacity-25">{row['firmware']}</span></td>
                <td>
                  <a href="{row['id']}.html" class="btn btn-sm btn-ddmms-outline py-1 px-2 text-decoration-none">
                    <i class="bi bi-file-text me-1"></i> View Page
                  </a>
                </td>
              </tr>
"""
    page_html += """
            </tbody>
          </table>
        </div>

        <div class="text-center">
          <a href="specs.html" class="btn btn-ddmms-outline text-decoration-none">
            <i class="bi bi-table me-1"></i> View Full 14-Model Comparison Matrix &rarr;
          </a>
        </div>
      </div>
    </section>
  </main>
"""
    page_html += render_footer()
    (NEWSITE_DIR / "index.html").write_text(page_html, encoding="utf-8")

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load / Generate section YAML data
    keyboards_yml = DATA_DIR / "keyboards.yml"
    converted_yml = DATA_DIR / "converted.yml"
    mice_yml = DATA_DIR / "mice.yml"
    guides_yml = DATA_DIR / "guides.yml"
    specs_yml = DATA_DIR / "specs.yml"
    about_yml = DATA_DIR / "about.yml"

    keyboards_data = yaml.safe_load(keyboards_yml.read_text(encoding="utf-8"))
    converted_data = yaml.safe_load(converted_yml.read_text(encoding="utf-8"))
    mice_data = yaml.safe_load(mice_yml.read_text(encoding="utf-8"))
    guides_data = yaml.safe_load(guides_yml.read_text(encoding="utf-8"))
    specs_data = yaml.safe_load(specs_yml.read_text(encoding="utf-8"))
    about_data = yaml.safe_load(about_yml.read_text(encoding="utf-8"))

    # Generate Section Index Pages
    print("Generating catalog pages...")
    generate_catalog_page("keyboards", "Designed Keyboards", "Custom ortholinear mechanical keyboards and macropads in modular LEGO cases", keyboards_data["items"], "#6cb670")
    generate_catalog_page("converted", "Vintage POS Conversions", "Rescued mechanical Tipro terminals restored and converted to QMK firmware", converted_data["items"], "#fbbf24")
    generate_catalog_page("mice", "Liberated QMK Mice", "Gaming mice freed from closed-source software with custom QMK firmware and bootloader", mice_data["items"], "#818cf8")
    generate_catalog_page("guides", "Hardware & Build Guides", "Soldering tutorials, matrix theory, shift-register expansion, and KiCad PCB design", guides_data["items"], "#f472b6")
    generate_about_page(about_data)
    generate_specs_page(specs_data)
    generate_landing_page(keyboards_data, converted_data, mice_data, guides_data, specs_data)

    # Generate Individual Detail Pages
    print("Generating individual detail pages...")
    for item in keyboards_data["items"]:
        generate_detail_page(item, "Keyboards", "keyboards.html", f"keyboard_{item['id']}")

    for item in converted_data["items"]:
        generate_detail_page(item, "POS Conversions", "converted.html", f"converted_{item['id']}")

    for item in mice_data["items"]:
        generate_detail_page(item, "QMK Mice", "mice.html", f"mice_{item['id']}")

    for item in guides_data["items"]:
        generate_detail_page(item, "Build Guides", "guides.html", f"guide_{item['id']}")

    print("Successfully built all separate pages for newsite!")

if __name__ == "__main__":
    main()
