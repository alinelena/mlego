# Tipro 8×4 — 32-Key POS Keypad Conversion

<div class="spec-badges">
  <span class="spec-badge spec-badge--status">Status: Completed</span>
  <span class="spec-badge">8×4 Ortho (32 Keys)</span>
  <span class="spec-badge">WeAct STM32G431 CoreBoard</span>
  <span class="spec-badge">QMK</span>
</div>

![Tipro 32 8x4 converted](pics/tipro/tipro8x4.webp){ loading=lazy }

## Introduction { #introduction }

A 32-key **Tipro 8×4** mechanical keypad module converted to QMK using a direct-wired **WeAct `STM32G431`** controller board.

## Internal Wiring & MCU { #wiring }

![Tipro 32 8x4 internal PCB wiring](pics/tipro/tipro8x4-pcb.webp){ loading=lazy }

* **Microcontroller**: [WeAct `STM32G431` CoreBoard](https://github.com/WeActStudio/WeActStudio.STM32G431CoreBoard) ([AliExpress reference](https://www.aliexpress.com/item/1005005303669884.html))

## Firmware { #firmware }

Prebuilt firmware can be downloaded from [GitHub Actions (`qmk_firmware`)](https://github.com/alinelena/qmk_firmware/actions/workflows/build.yml) — navigate to the **build firmware for mlego** workflow, select the latest successful run, and download **`tipro32_default`** from the artifacts list.

## Original Condition { #pictures }

![Tipro 32 8x4 original POS module](pics/tipro/tipro8x4-orig.jpeg){ loading=lazy }
