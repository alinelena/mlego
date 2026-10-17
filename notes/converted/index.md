# Converted POS Terminals

Vintage mechanical **Tipro** point-of-sale (POS) terminals rescued from eBay, stripped down, cleaned, resoldered with fresh switches, and converted to run **QMK Firmware** using custom STM32 daughterboards.

![Converted Tipro POS collection](../pics/converted-all.webp){ loading=lazy }

## Tipro Conversion Projects

<div class="grid cards" markdown>

-   ![Tipro 8x16](../pics/tipro/m8x16.webp){ loading=lazy }

    ### [Tipro 8×16 (128-Key)](../tipro8x16.md)

    `8×16 Ortho` · `STM32F401` · `74HC595 LEDs`

    Full 128-key mechanical matrix terminal restored with a polished steel plate, painted case, custom daughterboard PCB, and MT3 Dasher / `/dev/tty` keycaps.

    [:octicons-arrow-right-24: Tipro 8×16 Build Notes](../tipro8x16.md)

-   ![Tipro 8x12](../pics/tipro/m8x12-final.webp){ loading=lazy }

    ### [Tipro 8×12 (96-Key)](../tipro8x12.md)

    `8×12 Ortho` · `STM32F401` · `QMK`

    Compact 96-key 8×12 Tipro terminal converted using the shared `hand8x16` STM32 daughterboard and shift-register status LEDs.

    [:octicons-arrow-right-24: Tipro 8×12 Build Notes](../tipro8x12.md)

-   ![Tipro 8x4](../pics/tipro/tipro8x4.webp){ loading=lazy }

    ### [Tipro 8×4 (32-Key Pad)](../tipro8x4.md)

    `8×4 Grid` · `WeAct STM32G431` · `QMK`

    Dedicated 32-key Tipro macropad/module powered by a WeAct `STM32G431` core board.

    [:octicons-arrow-right-24: Tipro 8×4 Build Notes](../tipro8x4.md)

-   ![Tipro ANSI-Ortho](../pics/tipro/tiproansi-ortho.webp){ loading=lazy }

    ### [Tipro ANSI-Ortho](../tiproansi-ortho.md)

    `Hybrid ANSI + Ortho` · `STM32F401` · `QMK`

    Combination ANSI 60% + top/side ortholinear macro bank converted with the `hand8x16` controller board.

    [:octicons-arrow-right-24: Tipro ANSI-Ortho Notes](../tiproansi-ortho.md)

-   ![Tipro Ortho-ANSI](../pics/tipro/tiproortho-ansi.webp){ loading=lazy }

    ### [Tipro Ortho-ANSI](../tiproortho-ansi.md)

    `Hybrid Ortho + ANSI` · `STM32F401` · `QMK`

    Left-hand ortholinear keypad paired with a standard staggered section, restored and re-switched for QMK.

    [:octicons-arrow-right-24: Tipro Ortho-ANSI Notes](../tiproortho-ansi.md)

</div>
