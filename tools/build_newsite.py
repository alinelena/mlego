#!/usr/bin/env python3
"""
Build script for newsite.
Reads documentation from notes/ (keeping notes/ completely untouched)
and generates data files and browser bundles for the modern newsite.
"""
from pathlib import Path
import json
import re

ROOT_DIR = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT_DIR / "notes"
NEWSITE_DIR = ROOT_DIR / "newsite"
DATA_DIR = NEWSITE_DIR / "data"

DOCS_MAP = {
    # Keyboards
    "m66": {"title": "m66 (5×14 Ortho)", "category": "keyboards", "badge": "5×14 Ortho", "keys": "66", "file": "m66.md", "image": "pics/m66/mlego_m66_rev4-lcd.webp", "mcu": "RP2040 / nice!nano / XIAO", "firmware": "QMK & ZMK", "summary": "Flagship 5×14 ortholinear keyboard with dedicated encoder column, per-key RGB, and modular OLED, e-ink, Sharp Memory, or IPS LCD displays."},
    "m65": {"title": "m65 (5×13 Ortho)", "category": "keyboards", "badge": "5×13 Ortho", "keys": "65", "file": "m65.md", "image": "pics/mlego_m65_rev11_eink.webp", "mcu": "STM32F401 / RP2040 / XIAO", "firmware": "QMK & ZMK", "summary": "Original 65-key ISO-friendly LEGO ortholinear keyboard evolved across 11 revisions — from BluePill to Raspberry Pi Pico and Seeed XIAO SPI shift registers."},
    "m60": {"title": "m60 (5×12 Ortho)", "category": "keyboards", "badge": "5×12 Ortho", "keys": "60", "file": "m60.md", "image": "pics/5x12/m60_rev2.webp", "mcu": "STM32F401 / RP2040", "firmware": "QMK", "summary": "Preonic-inspired 60-key 5×12 layout in a LEGO case with rotary encoder, RGB strip, and OLED support."},
    "m60_split": {"title": "m60 Split (5×12 Split)", "category": "keyboards", "badge": "5×12 Split", "keys": "60 (2×30)", "file": "m60_split.md", "image": "pics/5x12s/m60_split.webp", "mcu": "Dual STM32F401 / F411", "firmware": "QMK", "summary": "Ergonomic split ortholinear keyboard mounted on twin 16×16 LEGO plates with dual encoders and RGB underglow."},
    "m48": {"title": "m48 (4×12 Ortho)", "category": "keyboards", "badge": "4×12 Ortho", "keys": "48", "file": "m48.md", "image": "pics/4x12/m48_tty.webp", "mcu": "STM32F401 / F411", "firmware": "QMK", "summary": "Ultra-compact 48-key Planck-style ortholinear keyboard in a LEGO chassis with rotary encoder support."},
    "m20": {"title": "m20 (5×4 Pad)", "category": "keyboards", "badge": "5×4 Pad", "keys": "20", "file": "m20.md", "image": "pics/m20/m20_v1.webp", "mcu": "Raspberry Pi Pico (RP2040)", "firmware": "QMK", "summary": "Versatile 20-key macropad/numpad supporting 5-pin Cherry MX and Kailh Choc v2 low-profile switches, rotary encoder, and OLED."},
    "m8": {"title": "m8 (2×4 Pad)", "category": "keyboards", "badge": "2×4 Pad", "keys": "8", "file": "m8.md", "image": "pics/hand/m1-5x5-rounded.webp", "mcu": "XIAO RP2040 / 74HC595 + 74HC589", "firmware": "QMK", "summary": "8-key SPI shift-register engineering testbed driving an e-ink display, I²C OLED, and clickable encoder on minimal MCU pins."},
    "m4": {"title": "m4 (2×2 Pad)", "category": "keyboards", "badge": "2×2 Pad", "keys": "4", "file": "m4.md", "image": "pics/m4/m4-full.webp", "mcu": "Seeed XIAO BLE / RP2040", "firmware": "ZMK & QMK", "summary": "Ultra-compact 4-key macropad and wireless testbed for prototyping shift-register matrix scanning and BLE firmware."},
    
    # Converted POS
    "tipro8x16": {"title": "Tipro 8×16 (128-Key)", "category": "converted", "badge": "8×16 POS", "keys": "128", "file": "tipro8x16.md", "image": "pics/tipro/m8x16.webp", "mcu": "STM32F401 + 74HC595", "firmware": "QMK", "summary": "Restored 128-key vintage mechanical terminal with polished steel plate, custom daughterboard, 7 status LEDs, and MT3 Dasher keycaps."},
    "tipro8x12": {"title": "Tipro 8×12 (96-Key)", "category": "converted", "badge": "8×12 POS", "keys": "96", "file": "tipro8x12.md", "image": "pics/tipro/m8x12-final.webp", "mcu": "STM32F401 + 74HC595", "firmware": "QMK", "summary": "Compact 96-key POS terminal converted to QMK using the shared hand8x16 daughterboard and shift register."},
    "tipro8x4": {"title": "Tipro 8×4 (32-Key)", "category": "converted", "badge": "8×4 POS", "keys": "32", "file": "tipro8x4.md", "image": "pics/tipro/tipro8x4.webp", "mcu": "WeAct STM32G431", "firmware": "QMK", "summary": "32-key Tipro POS macropad module powered by a high-performance STM32G431 microcontroller."},
    "tiproansi-ortho": {"title": "Tipro ANSI-Ortho", "category": "converted", "badge": "ANSI + Ortho", "keys": "Hybrid", "file": "tiproansi-ortho.md", "image": "pics/tipro/tiproansi-ortho.webp", "mcu": "STM32F401", "firmware": "QMK", "summary": "Combination ANSI 60% layout with dedicated ortholinear macro bank converted to QMK."},
    "tiproortho-ansi": {"title": "Tipro Ortho-ANSI", "category": "converted", "badge": "Ortho + ANSI", "keys": "Hybrid", "file": "tiproortho-ansi.md", "image": "pics/tipro/tiproortho-ansi.webp", "mcu": "STM32F401", "firmware": "QMK", "summary": "Left-hand ortholinear keypad paired with standard typewriter section, restored and reswitched."},

    # Mice
    "prime": {"title": "SteelSeries Prime Mouse", "category": "mice", "badge": "QMK Mouse", "keys": "5-Btn", "file": "prime.md", "image": "pics/prime.webp", "mcu": "STM32F103 + PMW3389", "firmware": "QMK (UF2)", "summary": "Hardware teardown, SWD unlock via OpenOCD, UF2 bootloader flashing, and QMK conversion for the SteelSeries Prime gaming mouse."},

    # Guides
    "assembly": {"title": "Step-by-Step Assembly Guide", "category": "guides", "badge": "Build Guide", "file": "assembly.md", "image": "pics/final_3.webp", "summary": "Illustrated soldering and assembly walkthrough: sockets, diodes, LED resistor calculations, and LEGO case mounting."},
    "notenoughpins": {"title": "Not Enough Pins? Matrix Expansion", "category": "guides", "badge": "Hardware Guide", "file": "notenoughpins.md", "image": "pics/matrix-2b_v2.webp", "summary": "Exhaustive engineering tutorial on driving large matrices from tiny MCUs via SPI shift registers and matrix folding."},
    "how_matrix_works_extra": {"title": "How Keyboard Matrices Work (3×3)", "category": "guides", "badge": "Electronics Guide", "file": "how_matrix_works_extra.md", "image": "pics/col2row/pcb-3df-col2row.webp", "summary": "Beginner-friendly hardware primer on diode direction, ghosting prevention, KiCad PCB routing, and bootstrapping QMK."},
    "hand5x5": {"title": "Handwire Helpers (5×5 Breakout)", "category": "guides", "badge": "PCB Design", "file": "hand5x5.md", "image": "pics/hand/m1-5x5-rounded.webp", "summary": "Modular 5×5 switch matrix break-apart PCBs to simplify custom handwiring and speed up prototyping."},

    # Section Indexes
    "home": {"title": "mlego Overview", "category": "overview", "badge": "Overview", "file": "index.md", "image": "pics/keybs.webp", "summary": "Project manifesto, philosophy, design goals, and hardware lineup."},
    "keyboards_index": {"title": "Keyboards Catalog", "category": "keyboards", "badge": "Catalog", "file": "keyboards/index.md", "image": "pics/m65-rev1-10.webp", "summary": "Overview of the entire custom ortholinear keyboard collection."},
    "converted_index": {"title": "POS Conversions Catalog", "category": "converted", "badge": "Catalog", "file": "converted/index.md", "image": "pics/converted-all.webp", "summary": "Overview of rescued and converted Tipro POS terminals."},
    "mice_index": {"title": "Liberated QMK Mice", "category": "mice", "badge": "Catalog", "file": "mice/index.md", "image": "pics/prime.webp", "summary": "Overview of commercial gaming mice running open-source QMK firmware."},
    "extra_index": {"title": "Engineering Notes Catalog", "category": "guides", "badge": "Catalog", "file": "extra/index.md", "image": "pics/matrix-2b_v2.webp", "summary": "Hardware design notes, tutorials, and firmware deep-dives."}
}

def clean_markdown_for_web(text: str) -> str:
    """Normalize image paths and mkdocs-specific syntax for marked.js"""
    # Replace {: loading=lazy } or {.md-button} etc.
    text = re.sub(r'\{:\s*[^}]+\}', '', text)
    text = re.sub(r'\{[.#][^}]+\}', '', text)
    # Fix image paths: "../pics/" or "pics/" -> "pics/"
    text = re.sub(r'\((\.\./)+pics/', '(pics/', text)
    text = re.sub(r'\(\./pics/', '(pics/', text)
    # Fix internal markdown links to #doc/id
    for doc_id, meta in DOCS_MAP.items():
        doc_filename = meta["file"].split("/")[-1]
        text = re.sub(rf'\]\((?:\.\./)?(?:keyboards/|converted/|mice/|extra/)?{re.escape(doc_filename)}\)', f'](#doc/{doc_id})', text)
    # Replace octicon/material emojis with text/icons
    text = re.sub(r':(?:material|octicons|fontawesome)-[a-z0-9-]+:', '', text)
    # Replace markdown admonitions (!!! note -> blockquote)
    text = re.sub(r'^!!!\s+([a-zA-Z0-9_-]+)(?:\s+"([^"]+)")?', r'> **\2**\n>', text, flags=re.MULTILINE)
    return text

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    docs_content = {}
    for doc_id, meta in DOCS_MAP.items():
        file_path = NOTES_DIR / meta["file"]
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            docs_content[doc_id] = {
                "id": doc_id,
                "title": meta["title"],
                "category": meta["category"],
                "badge": meta.get("badge", ""),
                "summary": meta.get("summary", ""),
                "image": meta.get("image", ""),
                "mcu": meta.get("mcu", ""),
                "firmware": meta.get("firmware", ""),
                "keys": meta.get("keys", ""),
                "markdown": clean_markdown_for_web(content),
            }
        else:
            print(f"Warning: {file_path} not found")

    # Generate JSON
    (DATA_DIR / "docs.json").write_text(json.dumps(docs_content, indent=2), encoding="utf-8")
    
    # Generate standalone JS bundle so it runs with zero server dependencies / without CORS issues
    js_content = f"/* Auto-generated by tools/build_newsite.py */\nwindow.MLEGO_DATA = {json.dumps(docs_content, indent=2)};\n"
    (NEWSITE_DIR / "assets" / "js" / "content-data.js").write_text(js_content, encoding="utf-8")
    
    print(f"Successfully compiled {len(docs_content)} documentation pages to newsite/data/ and newsite/assets/js/content-data.js")

if __name__ == "__main__":
    main()

