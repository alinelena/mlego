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

def clean_markdown_for_web(text: str) -> str:
    """Normalize image paths, links, and mkdocs syntax"""
    # Strip MkDocs attribute annotations like {: loading=lazy }, { loading=lazy }, { #anchor }, { .md-button }
    text = re.sub(r'\{:\s*[^}]+\}', '', text)
    text = re.sub(r'\{[.#][^}]+\}', '', text)
    text = re.sub(r'\{\s*loading=lazy\s*\}', '', text)

    # Normalize relative image paths to pics/...
    text = re.sub(r'\((\.\./)+pics/', '(pics/', text)
    text = re.sub(r'\(\./pics/', '(pics/', text)

    # Internal anchor-based doc links (#doc/name)
    text = re.sub(r'\(#doc/([a-zA-Z0-9_-]+)\)', r'(\1.html)', text)

    # Section index links
    text = re.sub(r'\]\((?:\.\./)?keyboards/index\.md\)', r'](keyboards.html)', text)
    text = re.sub(r'\]\((?:\.\./)?converted/index\.md\)', r'](converted.html)', text)
    text = re.sub(r'\]\((?:\.\./)?mice/index\.md\)', r'](mice.html)', text)
    text = re.sub(r'\]\((?:\.\./)?extra/index\.md\)', r'](guides.html)', text)
    text = re.sub(r'\]\((?:\.\./)?index\.md\)', r'](index.html)', text)

    # Inter-page markdown links: ](name.md#anchor) -> ](name.html#anchor)
    text = re.sub(
        r'\]\((?:\.\./)?(?:keyboards/|converted/|mice/|extra/)?([a-zA-Z0-9_-]+)\.md(#[^)]+)?\)',
        r'](\1.html\2)',
        text
    )

    # Strip MkDocs icon shortcuts like :material-keyboard:
    text = re.sub(r':(?:material|octicons|fontawesome)-[a-z0-9-]+:', '', text)

    # Convert MkDocs content tabs (=== "Title") to clean section subheadings
    lines = text.splitlines()
    processed_lines = []
    in_tab = False
    for line in lines:
        tab_match = re.match(r'^===\s+"([^"]+)"', line)
        if tab_match:
            title = tab_match.group(1)
            processed_lines.append(f'<h5 class="mt-4 mb-2 text-info">{title}</h5>')
            in_tab = True
        elif in_tab:
            if line.startswith("    "):
                processed_lines.append(line[4:])
            elif line.strip() == "":
                processed_lines.append("")
            else:
                in_tab = False
                processed_lines.append(line)
        else:
            processed_lines.append(line)
    text = "\n".join(processed_lines)

    # Convert collapsible blocks (??? code "Title") and admonitions (!!! note "Title")
    text = re.sub(r'^\?\?\?\+?\s+(?:[a-zA-Z0-9_-]+)?(?:\s+"([^"]+)")?', r'> **\1**\n>', text, flags=re.MULTILINE)
    text = re.sub(r'^!!!\s+([a-zA-Z0-9_-]+)(?:\s+"([^"]+)")?', r'> **\2**\n>', text, flags=re.MULTILINE)

    return text.strip() + "\n"

def md_to_html(md_text: str) -> str:
    """Convert cleaned markdown to semantic HTML"""
    return markdown.markdown(
        md_text,
        extensions=['extra', 'tables', 'fenced_code', 'toc', 'sane_lists']
    )

def read_note(filename: str) -> str:
    """Read a markdown file directly from the notes/ directory and render to HTML"""
    file_path = NOTES_DIR / filename
    if not file_path.exists():
        print(f"Warning: Note file not found: {file_path}")
        return ""
    raw_md = file_path.read_text(encoding="utf-8")
    cleaned_md = clean_markdown_for_web(raw_md)
    return md_to_html(cleaned_md)

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

    # 2. Render About Page (sourced directly from notes/index.md)
    about_file = about_data.get("file", "index.md")
    about_tpl = env.get_template("about.html")
    about_html = about_tpl.render(
        title="About Project & Manifesto",
        description="Project overview, philosophy, and history of mlego keyboards",
        active_page="about",
        active_group="about",
        about=about_data,
        html_content=read_note(about_file),
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

    # 5. Render Detail Pages (content sourced directly from notes/<item.file>)
    detail_tpl = env.get_template("detail.html")
    detail_configs = [
        (keyboards_data["items"], "Keyboards", "keyboards.html", "keyboards"),
        (converted_data["items"], "POS Conversions", "converted.html", "converted"),
        (mice_data["items"], "QMK Mice", "mice.html", "mice"),
        (guides_data["items"], "Build Guides", "guides.html", "guides"),
    ]

    count = 0
    for items, parent_title, parent_url, group_id in detail_configs:
        for item in items:
            note_filename = item.get("file", f"{item['id']}.md")
            rendered_content = read_note(note_filename)
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
            count += 1

    print(f"Successfully rendered all {count + 7} pages with Jinja2 templates directly from notes/*.md!")

if __name__ == "__main__":
    main()
