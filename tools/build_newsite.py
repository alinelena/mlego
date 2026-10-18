# /// script
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
from pathlib import Path
import re
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT_DIR / "notes"
NEWSITE_DIR = ROOT_DIR / "newsite"
DATA_DIR = NEWSITE_DIR / "data"

# Configure YAML multiline string representation
def str_presenter(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

def clean_markdown_for_web(text: str) -> str:
    """Normalize image paths and mkdocs-specific syntax for marked.js"""
    text = re.sub(r'\{:\s*[^}]+\}', '', text)
    text = re.sub(r'\{[.#][^}]+\}', '', text)
    text = re.sub(r'\((\.\./)+pics/', '(pics/', text)
    text = re.sub(r'\(\./pics/', '(pics/', text)
    # Fix internal markdown links to #doc/id
    for doc_id, filename in [
        ("m66", "m66.md"), ("m65", "m65.md"), ("m60", "m60.md"),
        ("m60_split", "m60_split.md"), ("m48", "m48.md"), ("m20", "m20.md"),
        ("m8", "m8.md"), ("m4", "m4.md"), ("tipro8x16", "tipro8x16.md"),
        ("tipro8x12", "tipro8x12.md"), ("tipro8x4", "tipro8x4.md"),
        ("tiproansi-ortho", "tiproansi-ortho.md"), ("tiproortho-ansi", "tiproortho-ansi.md"),
        ("prime", "prime.md"), ("assembly", "assembly.md"),
        ("notenoughpins", "notenoughpins.md"), ("how_matrix_works_extra", "how_matrix_works_extra.md"),
        ("hand5x5", "hand5x5.md")
    ]:
        text = re.sub(rf'\]\((?:\.\./)?(?:keyboards/|converted/|mice/|extra/)?{re.escape(filename)}\)', f'](#doc/{doc_id})', text)
    text = re.sub(r':(?:material|octicons|fontawesome)-[a-z0-9-]+:', '', text)
    text = re.sub(r'^!!!\s+([a-zA-Z0-9_-]+)(?:\s+"([^"]+)")?', r'> **\2**\n>', text, flags=re.MULTILINE)
    return text.strip() + "\n"

def read_note(filename: str) -> str:
    file_path = NOTES_DIR / filename
    if file_path.exists():
        return clean_markdown_for_web(file_path.read_text(encoding="utf-8"))
    return ""

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. site.yml
    site_data = {
        "title": "mlego",
        "description": "Modular LEGO-mounted ortholinear mechanical keyboards, QMK/ZMK firmware, POS conversions, and hardware build notes",
        "author": "Alin M. Elena",
        "base_url": "https://mlego.elena.re",
        "logo": "pics/mlego.webp",
        "logo_webp": "pics/mlego.webp",
        "favicon": "pics/mlego.webp",
        "banner": {
            "enable": True,
            "bg_image_webp": "images/backgrounds/exterior-stone-wall.webp",
            "bg_image": "images/backgrounds/exterior-stone-wall.jpg",
            "title": "mlego notes",
            "subtitle": "Modular LEGO Ortholinear Keyboards • Hardware & QMK/ZMK Firmware"
        },
        "menu": [
            {"name": "Home", "url": "#hero", "icon": "bi-house-door", "color": "#57cbcc"},
            {"name": "About", "url": "#about", "icon": "bi-info-circle", "color": "#2dd4bf"},
            {"name": "Keyboards", "url": "#keyboards", "icon": "bi-keyboard", "color": "#6cb670"},
            {"name": "Converted", "url": "#converted", "icon": "bi-cpu", "color": "#fbbf24"},
            {"name": "Mice", "url": "#mice", "icon": "bi-mouse", "color": "#818cf8"},
            {"name": "Guides", "url": "#guides", "icon": "bi-journal-code", "color": "#f472b6"},
            {"name": "Specs", "url": "#specs", "icon": "bi-table", "color": "#fb923c"},
            {"name": "Classic Site", "url": "classic/", "icon": "bi-journal-text", "color": "#38bdf8"}
        ],
        "dividers": {
            "after_hero": {
                "bg_image_webp": "images/backgrounds/old-brick-wall.webp",
                "bg_image": "images/backgrounds/old-brick-wall.jpg"
            },
            "after_about": {
                "bg_image_webp": "images/backgrounds/old-brick-wall.webp",
                "bg_image": "images/backgrounds/old-brick-wall.jpg"
            },
            "after_keyboards": {
                "bg_image_webp": "images/backgrounds/stone-wall.webp",
                "bg_image": "images/backgrounds/stone-wall.jpg"
            },
            "after_converted": {
                "bg_image_webp": "images/backgrounds/old-wall.webp",
                "bg_image": "images/backgrounds/old-wall.jpg"
            },
            "after_mice": {
                "bg_image_webp": "images/backgrounds/stone-wall-2.webp",
                "bg_image": "images/backgrounds/stone-wall-2.jpg"
            },
            "after_guides": {
                "bg_image_webp": "images/backgrounds/stones.webp",
                "bg_image": "images/backgrounds/stones.jpg"
            },
            "after_specs": {
                "bg_image_webp": "images/backgrounds/brick-wall-2.webp",
                "bg_image": "images/backgrounds/brick-wall-2.jpg"
            }
        },
        "social": [
            {"name": "GitLab", "icon": "bi-git", "url": "https://gitlab.com/m-lego", "color": "#fc6d26"},
            {"name": "GitHub", "icon": "bi-github", "url": "https://github.com/alinelena", "color": "#c9d1d9"},
            {"name": "Website", "icon": "bi-globe", "url": "https://alin.elena.re", "color": "#57cbcc"},
            {"name": "DDMMS", "icon": "bi-building", "url": "https://ddmms.elena.re", "color": "#48b2b3"}
        ],
        "copyright": "Copyright © 2017–2026 Alin M. Elena. All rights reserved."
    }
    (DATA_DIR / "site.yml").write_text(yaml.dump(site_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # 2. about.yml
    about_data = {
        "enable": True,
        "title": "Project Overview",
        "subtitle": "Fun, modular, open-source electronics & mechanical keyboard playground",
        "stats": [
            {"label": "Keyboards Designed", "count": "8", "icon": "bi-keyboard", "color": "#57cbcc"},
            {"label": "m65 Hardware Revisions", "count": "11", "icon": "bi-clock-history", "color": "#6cb670"},
            {"label": "POS Terminals Converted", "count": "5", "icon": "bi-cpu", "color": "#fbbf24"},
            {"label": "Open Source HW & FW", "count": "100%", "icon": "bi-code-slash", "color": "#818cf8"}
        ],
        "manifesto": {
            "what_it_is": [
                "Fun & experimental — designed for learning electronics, KiCad routing, and firmware architecture.",
                "Educational — documented schematics, SPI shift-register matrix expansion, and QMK/ZMK configs.",
                "Functional daily drivers — full ISO keycap compatibility on comfortable ortholinear grids.",
                "Modular LEGO Cases — PCBs drilled to official LEGO stud pitch (1.6mm), snapping onto standard LEGO plates."
            ],
            "what_it_is_not": "This project is an evolving maker journey rather than a static commercial custom kit. Every revision explores a new microcontroller (STM32, RP2040, nRF52840), display technology (OLED, WeAct e-ink, Sharp Memory, ST7735 IPS LCD), or matrix scanning circuit."
        },
        "content": read_note("index.md")
    }
    (DATA_DIR / "about.yml").write_text(yaml.dump(about_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # 3. keyboards.yml
    keyboards_data = {
        "enable": True,
        "title": "Designed Keyboards",
        "subtitle": "Custom ortholinear mechanical keyboards and macropads in modular LEGO cases",
        "items": [
            {
                "id": "m66",
                "title": "m66 (5×14 Ortho)",
                "category": "keyboards",
                "badge": "5×14 Ortho",
                "keys": "66",
                "mcu": "RP2040 / nice!nano / XIAO",
                "firmware": "QMK & ZMK",
                "image": "pics/m66/mlego_m66_rev4-lcd.webp",
                "summary": "Flagship 5×14 ortholinear keyboard with dedicated encoder column, per-key RGB, and modular OLED, e-ink, Sharp Memory, or IPS LCD displays.",
                "content": read_note("m66.md")
            },
            {
                "id": "m65",
                "title": "m65 (5×13 Ortho)",
                "category": "keyboards",
                "badge": "5×13 Ortho",
                "keys": "65",
                "mcu": "STM32F401 / RP2040 / XIAO",
                "firmware": "QMK & ZMK",
                "image": "pics/mlego_m65_rev11_eink.webp",
                "summary": "Original 65-key ISO-friendly LEGO ortholinear keyboard evolved across 11 revisions — from BluePill to Raspberry Pi Pico and Seeed XIAO SPI shift registers.",
                "content": read_note("m65.md")
            },
            {
                "id": "m60",
                "title": "m60 (5×12 Ortho)",
                "category": "keyboards",
                "badge": "5×12 Ortho",
                "keys": "60",
                "mcu": "STM32F401 / RP2040",
                "firmware": "QMK",
                "image": "pics/5x12/m60_rev2.webp",
                "summary": "Preonic-inspired 60-key 5×12 layout in a LEGO case with rotary encoder, RGB strip, and OLED support.",
                "content": read_note("m60.md")
            },
            {
                "id": "m60_split",
                "title": "m60 Split (5×12 Split)",
                "category": "keyboards",
                "badge": "5×12 Split",
                "keys": "60 (2×30)",
                "mcu": "Dual STM32F401 / F411",
                "firmware": "QMK",
                "image": "pics/5x12s/m60_split.webp",
                "summary": "Ergonomic split ortholinear keyboard mounted on twin 16×16 LEGO plates with dual encoders and RGB underglow.",
                "content": read_note("m60_split.md")
            },
            {
                "id": "m48",
                "title": "m48 (4×12 Ortho)",
                "category": "keyboards",
                "badge": "4×12 Ortho",
                "keys": "48",
                "mcu": "STM32F401 / F411",
                "firmware": "QMK",
                "image": "pics/4x12/m48_tty.webp",
                "summary": "Ultra-compact 48-key Planck-style ortholinear keyboard in a LEGO chassis with rotary encoder support.",
                "content": read_note("m48.md")
            },
            {
                "id": "m20",
                "title": "m20 (5×4 Pad)",
                "category": "keyboards",
                "badge": "5×4 Pad",
                "keys": "20",
                "mcu": "Raspberry Pi Pico (RP2040)",
                "firmware": "QMK",
                "image": "pics/m20/m20_v1.webp",
                "summary": "Versatile 20-key macropad/numpad supporting 5-pin Cherry MX and Kailh Choc v2 low-profile switches, rotary encoder, and OLED.",
                "content": read_note("m20.md")
            },
            {
                "id": "m8",
                "title": "m8 (2×4 Pad)",
                "category": "keyboards",
                "badge": "2×4 Pad",
                "keys": "8",
                "mcu": "XIAO RP2040 / 74HC595 + 74HC589",
                "firmware": "QMK",
                "image": "pics/hand/m1-5x5-rounded.webp",
                "summary": "8-key SPI shift-register engineering testbed driving an e-ink display, I²C OLED, and clickable encoder on minimal MCU pins.",
                "content": read_note("m8.md")
            },
            {
                "id": "m4",
                "title": "m4 (2×2 Pad)",
                "category": "keyboards",
                "badge": "2×2 Pad",
                "keys": "4",
                "mcu": "Seeed XIAO BLE / RP2040",
                "firmware": "ZMK & QMK",
                "image": "pics/m4/m4-full.webp",
                "summary": "Ultra-compact 4-key macropad and wireless testbed for prototyping shift-register matrix scanning and BLE firmware.",
                "content": read_note("m4.md")
            }
        ]
    }
    (DATA_DIR / "keyboards.yml").write_text(yaml.dump(keyboards_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # 4. converted.yml
    converted_data = {
        "enable": True,
        "title": "Vintage POS Conversions",
        "subtitle": "Rescued mechanical Tipro terminals restored and converted to QMK firmware",
        "items": [
            {
                "id": "tipro8x16",
                "title": "Tipro 8×16 (128-Key)",
                "category": "converted",
                "badge": "8×16 POS",
                "keys": "128",
                "mcu": "STM32F401 + 74HC595",
                "firmware": "QMK",
                "image": "pics/tipro/m8x16.webp",
                "summary": "Restored 128-key vintage mechanical terminal with polished steel plate, custom daughterboard, 7 status LEDs, and MT3 Dasher keycaps.",
                "content": read_note("tipro8x16.md")
            },
            {
                "id": "tipro8x12",
                "title": "Tipro 8×12 (96-Key)",
                "category": "converted",
                "badge": "8×12 POS",
                "keys": "96",
                "mcu": "STM32F401 + 74HC595",
                "firmware": "QMK",
                "image": "pics/tipro/m8x12-final.webp",
                "summary": "Compact 96-key POS terminal converted to QMK using the shared hand8x16 daughterboard and shift register.",
                "content": read_note("tipro8x12.md")
            },
            {
                "id": "tipro8x4",
                "title": "Tipro 8×4 (32-Key)",
                "category": "converted",
                "badge": "8×4 POS",
                "keys": "32",
                "mcu": "WeAct STM32G431",
                "firmware": "QMK",
                "image": "pics/tipro/tipro8x4.webp",
                "summary": "32-key Tipro POS macropad module powered by a high-performance STM32G431 microcontroller.",
                "content": read_note("tipro8x4.md")
            },
            {
                "id": "tiproansi-ortho",
                "title": "Tipro ANSI-Ortho",
                "category": "converted",
                "badge": "ANSI + Ortho",
                "keys": "Hybrid",
                "mcu": "STM32F401",
                "firmware": "QMK",
                "image": "pics/tipro/tiproansi-ortho.webp",
                "summary": "Combination ANSI 60% layout with dedicated ortholinear macro bank converted to QMK.",
                "content": read_note("tiproansi-ortho.md")
            },
            {
                "id": "tiproortho-ansi",
                "title": "Tipro Ortho-ANSI",
                "category": "converted",
                "badge": "Ortho + ANSI",
                "keys": "Hybrid",
                "mcu": "STM32F401",
                "firmware": "QMK",
                "image": "pics/tipro/tiproortho-ansi.webp",
                "summary": "Left-hand ortholinear keypad paired with standard typewriter section, restored and reswitched.",
                "content": read_note("tiproortho-ansi.md")
            }
        ]
    }
    (DATA_DIR / "converted.yml").write_text(yaml.dump(converted_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # 5. mice.yml
    mice_data = {
        "enable": True,
        "title": "Liberated QMK Mice",
        "subtitle": "Gaming mice freed from closed-source software with custom QMK firmware and bootloader",
        "items": [
            {
                "id": "prime",
                "title": "SteelSeries Prime Mouse",
                "category": "mice",
                "badge": "QMK Mouse",
                "keys": "5-Btn",
                "mcu": "STM32F103 + PMW3389",
                "firmware": "QMK (UF2)",
                "image": "pics/prime.webp",
                "summary": "Hardware teardown, SWD unlock via OpenOCD, UF2 bootloader flashing, and QMK conversion for the SteelSeries Prime gaming mouse.",
                "content": read_note("prime.md")
            }
        ]
    }
    (DATA_DIR / "mice.yml").write_text(yaml.dump(mice_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # 6. guides.yml
    guides_data = {
        "enable": True,
        "title": "Hardware & Build Guides",
        "subtitle": "Soldering tutorials, matrix theory, shift-register expansion, and KiCad PCB design",
        "items": [
            {
                "id": "assembly",
                "title": "Step-by-Step Assembly Guide",
                "category": "guides",
                "badge": "Build Guide",
                "image": "pics/final_3.webp",
                "summary": "Illustrated soldering and assembly walkthrough: sockets, diodes, LED resistor calculations, and LEGO case mounting.",
                "content": read_note("assembly.md")
            },
            {
                "id": "notenoughpins",
                "title": "Not Enough Pins? Matrix Expansion",
                "category": "guides",
                "badge": "Hardware Guide",
                "image": "pics/matrix-2b_v2.webp",
                "summary": "Exhaustive engineering tutorial on driving large matrices from tiny MCUs via SPI shift registers and matrix folding.",
                "content": read_note("notenoughpins.md")
            },
            {
                "id": "how_matrix_works_extra",
                "title": "How Keyboard Matrices Work (3×3)",
                "category": "guides",
                "badge": "Electronics Guide",
                "image": "pics/col2row/pcb-3df-col2row.webp",
                "summary": "Beginner-friendly hardware primer on diode direction, ghosting prevention, KiCad PCB routing, and bootstrapping QMK.",
                "content": read_note("how_matrix_works_extra.md")
            },
            {
                "id": "hand5x5",
                "title": "Handwire Helpers (5×5 Breakout)",
                "category": "guides",
                "badge": "PCB Design",
                "image": "pics/hand/m1-5x5-rounded.webp",
                "summary": "Modular 5×5 switch matrix break-apart PCBs to simplify custom handwiring and speed up prototyping.",
                "content": read_note("hand5x5.md")
            }
        ]
    }
    (DATA_DIR / "guides.yml").write_text(yaml.dump(guides_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # 7. specs.yml
    specs_data = {
        "enable": True,
        "title": "Hardware Comparison Lineup",
        "subtitle": "Comprehensive side-by-side specifications for all mlego keyboard models and conversions",
        "columns": ["Model", "Layout", "Keys", "MCU Platform", "Key Features & Peripherals", "Firmware", "Action"],
        "items": [
            {"id": "m66", "name": "m66", "layout": "5×14 Ortho", "keys": "66", "mcu": "RP2040 / nice!nano / XIAO", "features": "Clickable Encoder, Per-Key RGB, Modular Display (OLED/E-Ink/Sharp/LCD)", "firmware": "QMK & ZMK"},
            {"id": "m65", "name": "m65", "layout": "5×13 Ortho", "keys": "65", "mcu": "STM32F401 / RP2040 / XIAO", "features": "11 Hardware Revisions, Underglow RGB, Shift Register Matrix, E-Ink", "firmware": "QMK & ZMK"},
            {"id": "m60", "name": "m60", "layout": "5×12 Ortho", "keys": "60", "mcu": "STM32F401 / RP2040", "features": "Preonic-style, Rotary encoder, RGB strip, OLED support", "firmware": "QMK"},
            {"id": "m60_split", "name": "m60 Split", "layout": "5×12 Split", "keys": "60 (2×30)", "mcu": "Dual STM32F401 / 411", "features": "Dual 16×16 LEGO baseplates, Dual encoders, Underglow RGB", "firmware": "QMK"},
            {"id": "m48", "name": "m48", "layout": "4×12 Ortho", "keys": "48", "mcu": "STM32F401 / F411", "features": "Planck-style compact, Rotary encoder, RGB strip", "firmware": "QMK"},
            {"id": "m20", "name": "m20", "layout": "5×4 Pad", "keys": "20", "mcu": "Raspberry Pi Pico (RP2040)", "features": "Cherry MX & Kailh Choc v2, Rotary encoder, OLED", "firmware": "QMK"},
            {"id": "m8", "name": "m8", "layout": "2×4 Pad", "keys": "8", "mcu": "XIAO RP2040", "features": "74HC595 + 74HC589 SPI Shift Registers, E-Ink, OLED", "firmware": "QMK"},
            {"id": "m4", "name": "m4", "layout": "2×2 Pad", "keys": "4", "mcu": "Seeed XIAO BLE / RP2040", "features": "Wireless BLE, Shift register prototype, Compact macropad", "firmware": "ZMK & QMK"},
            {"id": "tipro8x16", "name": "Tipro 8×16", "layout": "8×16 POS", "keys": "128", "mcu": "STM32F401", "features": "Polished steel plate, 74HC595 LED expander, MT3 keycaps", "firmware": "QMK"},
            {"id": "tipro8x12", "name": "Tipro 8×12", "layout": "8×12 POS", "keys": "96", "mcu": "STM32F401", "features": "Daughterboard conversion, Shift register LEDs", "firmware": "QMK"},
            {"id": "tipro8x4", "name": "Tipro 8×4", "layout": "8×4 POS", "keys": "32", "mcu": "WeAct STM32G431", "features": "Dedicated 32-key POS macropad module", "firmware": "QMK"},
            {"id": "tiproansi-ortho", "name": "Tipro ANSI-Ortho", "layout": "ANSI + Ortho", "keys": "Hybrid", "mcu": "STM32F401", "features": "Hybrid ANSI 60% + Ortho macro bank", "firmware": "QMK"},
            {"id": "tiproortho-ansi", "name": "Tipro Ortho-ANSI", "layout": "Ortho + ANSI", "keys": "Hybrid", "mcu": "STM32F401", "features": "Left-hand ortho pad + ANSI typewriter", "firmware": "QMK"},
            {"id": "prime", "name": "SS Prime Mouse", "layout": "5-Btn Mouse", "keys": "5", "mcu": "STM32F103", "features": "PixArt PMW3389 sensor, SWD unlocked, UF2 bootloader", "firmware": "QMK"}
        ]
    }
    (DATA_DIR / "specs.yml").write_text(yaml.dump(specs_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # Remove any obsolete json files
    old_json = DATA_DIR / "docs.json"
    if old_json.exists():
        old_json.unlink()
    old_bundle = NEWSITE_DIR / "assets" / "js" / "content-data.js"
    if old_bundle.exists():
        old_bundle.unlink()

    print("Successfully built section YAML files:")
    for yf in sorted(DATA_DIR.glob("*.yml")):
        print(f"  - {yf.name} ({yf.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
