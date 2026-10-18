# /// script
# dependencies = [
#     "pyyaml>=6.0",
#     "markdown>=3.6",
#     "jinja2>=3.1",
# ]
# ///
from pathlib import Path
import re
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

ROOT_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT_DIR / "notes"
NEWSITE_DIR = ROOT_DIR / "newsite"
DATA_DIR = NEWSITE_DIR / "data"
TEMPLATES_DIR = ROOT_DIR / "templates"

# Configure Jinja2 environment
env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

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

def md_to_html(md_text: str) -> str:
    """Convert cleaned markdown to semantic HTML"""
    return markdown.markdown(
        md_text,
        extensions=['extra', 'tables', 'fenced_code', 'toc', 'sane_lists']
    )

def main():
    NEWSITE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load section YAML files
    keyboards_data = yaml.safe_load((DATA_DIR / "keyboards.yml").read_text(encoding="utf-8"))
    converted_data = yaml.safe_load((DATA_DIR / "converted.yml").read_text(encoding="utf-8"))
    mice_data = yaml.safe_load((DATA_DIR / "mice.yml").read_text(encoding="utf-8"))
    guides_data = yaml.safe_load((DATA_DIR / "guides.yml").read_text(encoding="utf-8"))
    specs_data = yaml.safe_load((DATA_DIR / "specs.yml").read_text(encoding="utf-8"))
    about_data = yaml.safe_load((DATA_DIR / "about.yml").read_text(encoding="utf-8"))

    # 1. Render Landing Page
    index_tpl = env.get_template("index.html")
    index_html = index_tpl.render(
        title="Modular LEGO Ortholinear Keyboards & Hardware Notes",
        description="Custom ISO-friendly ortholinear mechanical keyboards, macropads, vintage POS terminal conversions, and QMK/ZMK firmware — all mounted in modular LEGO cases.",
        active_page="home",
        active_group="home",
        about=about_data,
        keyboards=keyboards_data,
        converted=converted_data,
        mice=mice_data,
        guides=guides_data,
        specs=specs_data,
    )
    (NEWSITE_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # 2. Render About Page
    about_tpl = env.get_template("about.html")
    about_html = about_tpl.render(
        title="About Project & Manifesto",
        description="Project overview, philosophy, and history of mlego keyboards",
        active_page="about",
        active_group="about",
        about=about_data,
        html_content=md_to_html(clean_markdown_for_web(about_data.get("content", ""))),
    )
    (NEWSITE_DIR / "about.html").write_text(about_html, encoding="utf-8")

    # 3. Render Specs Page
    specs_tpl = env.get_template("specs.html")
    specs_html = specs_tpl.render(
        title="Hardware Comparison Lineup",
        description="Full side-by-side specifications for all mlego keyboards and conversions",
        active_page="specs",
        active_group="specs",
        specs=specs_data,
    )
    (NEWSITE_DIR / "specs.html").write_text(specs_html, encoding="utf-8")

    # 4. Render Catalog Pages
    catalog_tpl = env.get_template("catalog.html")
    catalog_configs = [
        ("keyboards", "Designed Keyboards", "Custom ortholinear mechanical keyboards and macropads in modular LEGO cases", keyboards_data["items"], "#6cb670"),
        ("converted", "Vintage POS Conversions", "Rescued mechanical Tipro terminals restored and converted to QMK firmware", converted_data["items"], "#fbbf24"),
        ("mice", "Liberated QMK Mice", "Gaming mice freed from closed-source software with custom QMK firmware and bootloader", mice_data["items"], "#818cf8"),
        ("guides", "Hardware & Build Guides", "Soldering tutorials, matrix theory, shift-register expansion, and KiCad PCB design", guides_data["items"], "#f472b6"),
    ]

    for cat_id, cat_title, cat_subtitle, cat_items, cat_accent in catalog_configs:
        cat_html = catalog_tpl.render(
            title=cat_title,
            subtitle=cat_subtitle,
            description=cat_subtitle,
            active_page=cat_id,
            active_group=cat_id,
            items=cat_items,
            accent_color=cat_accent,
        )
        (NEWSITE_DIR / f"{cat_id}.html").write_text(cat_html, encoding="utf-8")

    # 5. Render Detail Pages
    detail_tpl = env.get_template("detail.html")
    detail_configs = [
        (keyboards_data["items"], "Keyboards", "keyboards.html", "keyboards"),
        (converted_data["items"], "POS Conversions", "converted.html", "converted"),
        (mice_data["items"], "QMK Mice", "mice.html", "mice"),
        (guides_data["items"], "Build Guides", "guides.html", "guides"),
    ]

    for items, parent_title, parent_url, group_id in detail_configs:
        for item in items:
            raw_content = clean_markdown_for_web(item.get("content", ""))
            rendered_content = md_to_html(raw_content)
            det_html = detail_tpl.render(
                title=item["title"],
                description=item.get("summary", ""),
                active_page=item["id"],
                active_group=group_id,
                item=item,
                parent_title=parent_title,
                parent_url=parent_url,
                html_content=rendered_content,
            )
            (NEWSITE_DIR / f"{item['id']}.html").write_text(det_html, encoding="utf-8")

    print("Successfully rendered all pages with Jinja2 templates!")

if __name__ == "__main__":
    main()
