# Extra Engineering Notes & Guides

Practical build guides, hardware design notes, and firmware tutorials covering keyboard matrix scanning, pin expansion, and PCB assembly.

<div class="grid cards" markdown>

-   ![Assembly guide soldering](../pics/final_3.webp){ loading=lazy }

    ### [Step-by-Step Assembly Guide](../assembly.md)

    `Soldering` · `Sockets` · `Diodes` · `LEGO Case`

    Illustrated walkthrough for assembling an mlego keyboard: socketing the MCU and OLED, bending and soldering through-hole `1N4148` diodes, calculating LED resistors, mounting switches, and building the LEGO enclosure.

    [:octicons-arrow-right-24: Read Assembly Guide](../assembly.md)

-   ![Shift register matrix schematic](../pics/matrix-2b_v2.webp){ loading=lazy }

    ### [Not Enough Pins? Matrix Expansion](../notenoughpins.md)

    `74HC595` · `74HC165` · `74HC589` · `Matrix Remapping`

    How to drive a 65+ key matrix, rotary encoder, and display from a low-pin-count MCU like the Seeed XIAO RP2040 using SPI shift registers or mathematical matrix restructuring (`5×13` → `8×9`).

    [:octicons-arrow-right-24: Explore Pin Expansion Techniques](../notenoughpins.md)

-   ![3x3 matrix schematic](../pics/col2row/pcb-3df-col2row.webp){ loading=lazy }

    ### [How a Keyboard Matrix Works (3×3 Example)](../how_matrix_works_extra.md)

    `COL2ROW vs ROW2COL` · `qmk new-keyboard` · `STM32 & RP2040`

    Hands-on beginner tutorial explaining diode orientation, ghosting prevention, bootstrapping a new QMK keyboard definition from scratch, and designing a 3×3 PCB in KiCad.

    [:octicons-arrow-right-24: Read Matrix & QMK Tutorial](../how_matrix_works_extra.md)

-   ![Handwire 5x5 helper PCB](../pics/hand/m1-5x5-rounded.webp){ loading=lazy }

    ### [Handwire Helpers (Modular 5×5 PCB)](../hand5x5.md)

    `5×5 Snap-Apart Grid` · `Cherry MX & Kailh Choc v2`

    Tired of point-to-point handwiring? Use these modular 5×5 switch matrix PCBs that can be cut to custom dimensions and chained together.

    [:octicons-arrow-right-24: View 5×5 Helper PCBs & Gerbers](../hand5x5.md)

</div>
