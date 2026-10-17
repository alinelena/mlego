# Step-by-Step Assembly Guide

<div class="spec-badges">
  <span class="spec-badge">Build Time: ~2 Hours</span>
  <span class="spec-badge">Through-Hole Soldering</span>
  <span class="spec-badge">Modular LEGO Enclosure</span>
</div>

## Before You Start { #before-you-start }

!!! warning "Prerequisites"
    This guide assumes you know basic through-hole soldering, have reviewed the **BOM** section for your keyboard revision, and have all components and the PCB ready. While the soldering complexity is low, expect the full assembly to take around **2 hours**.

!!! info "Familiarize Yourself with the PCB"
    * **Front side**: The side with the silkscreen artwork (switches, MCU socket, and OLED mount on this side).
    * **Back side**: The underside where component leads are soldered.
    * You can ignore `R4` and `R5` on older revisions (`m65 Rev 4`), as they are only used in advanced configurations with special $\text{I}^2\text{C}$ pull-ups.

<div class="image-grid" markdown>
![PCB front side](pics/m65-rev4-pcb-front.webp){ loading=lazy }
![PCB back side](pics/m65-rev4-pcb-back.webp){ loading=lazy }
</div>

## 1. Preparing the MCU Socket & Headers { #mcu }

!!! tip "Always Socket Your Microcontroller"
    Whatever MCU board you use (`STM32` BlackPill, Raspberry Pi Pico `RP2040`, or Seeed Studio `XIAO`), **strongly consider socketing it** so it can be replaced or reused easily.

1. For 40-pin boards, I use **machined round pin headers** paired with a **40-way DIL socket** (or two single-row 20-pin female headers, which are especially convenient for Raspberry Pi Pico boards).

<div class="image-grid" markdown>
![Round headers and 40-way DIL socket](pics/header_1.webp){ loading=lazy }
![Single-row female header sockets](pics/sockets.webp){ loading=lazy }
</div>

!!! danger "Header Orientation"
    Insert the male header pins partway into the socket with the **conical/tapered pins pointing down into the socket**, then place the MCU board on top. Using the socket as a jig keeps both rows perfectly parallel.

<div class="image-grid" markdown>
![Headers seated in socket jig](pics/header_2.webp){ loading=lazy }
![MCU placed on top of headers ready to solder](pics/header_3.webp){ loading=lazy }
</div>

2. Verify the headers are vertical and stable. Solder the two corner pins of each row first to tack the alignment, then solder the remaining pins.

<div class="image-grid" markdown>
![Soldered MCU headers top view](pics/header_4.webp){ loading=lazy }
![Soldered MCU headers side profile](pics/header_5.webp){ loading=lazy }
</div>

## 2. Preparing the OLED Display { #oled }

If your build includes an $\text{I}^2\text{C}$ OLED screen, socket it as well using a 4-pin row of round machine pins and a low-profile 1×4 socket:

1. Use the keyboard PCB itself as an alignment jig: place the 4-pin header into the PCB pads (conical side pointing down toward the PCB), seat the OLED module on top, and level it with a bit of Blu-Tack or painter's tape.
2. Solder the 4 pins to the **OLED module only** (do not solder the header directly to the keyboard PCB!), then remove the OLED assembly.

<div class="image-grid" markdown>
![OLED header and socket](pics/header_6.webp){ loading=lazy }
![OLED aligned on PCB jig](pics/header_7.webp){ loading=lazy }
![Completed removable OLED module](pics/header_8.webp){ loading=lazy }
</div>

## 3. Soldering the Diodes { #diodes }

Prepare your `1N4148` (DO-35 through-hole) signal diodes (65 or 66 for `m65`/`m66`, 60 for `m60`, 48 for `m48`, 20 for `m20`).

1. Bend the leads at $90^\circ$ as shown below.

![1N4148 diode bent at 90 degrees](pics/diodes_1.webp){ loading=lazy }

!!! danger "Diode Polarity (Black Cathode Band)"
    Note the **black ring/collar (cathode)** at one end of the glass body. Insert every diode from the front of the PCB with the **black collar oriented toward the bottom/lower pad** (matching the silkscreen diode triangle/bar symbol).

2. Splay the leads outward on the back of the PCB to hold each diode snug against the board while flipping it over. Working column by column is fastest.

<div class="image-grid" markdown>
![Diodes inserted on front side](pics/diodes_2.webp){ loading=lazy }
![Diode leads bent on back side](pics/diodes_3.webp){ loading=lazy }
</div>

!!! warning "Trimming Diode Leads"
    After soldering, use flush cutters to trim the excess leads cleanly at the solder joint. *(Alternatively, you can wiggle the leads until they snap off at the joint, though it is good practice to briefly reflow the joint afterward if you do so.)*

3. For the horizontal diodes along the top row, bend one lead straight down beside the glass body as shown below so you can populate the entire row in one pass:

<div class="image-grid" markdown>
![Soldered diode joint](pics/diodes_4.webp){ loading=lazy }
![Top row diode bending](pics/diodes_5.webp){ loading=lazy }
![All diodes soldered](pics/diodes_6.webp){ loading=lazy }
</div>

## 4. Soldering the Resistors { #resistors }

Resistors are non-polarized — bend, insert, and splay the leads just like the diodes, ensuring the right resistance value goes into each footprint:

!!! warning "Resistor Values (Rev 4–6)"
    * **`R3` ($100\text{ k}\Omega$ or $22\text{ k}\Omega$)**: Required on `STM32F401`/`F411` BlackPill builds so the MCU enters DFU bootloader mode reliably.
    * **`R1` & `R2` (LED Current-Limiting)**: Select based on your LED color and desired brightness — $510\text{ }\Omega$ gives a pleasant glow on green/yellow LEDs, while $1\text{ k}\Omega$ works well for bright white LEDs.

!!! note "Testing LED Brightness & Polarity"
    Before soldering `R1`/`R2` and the LEDs, test them on a breadboard (or with DuPont jumper wires from a $3.3\text{ V}$ pin on your MCU) to confirm you like the brightness and to verify which LED leg is positive ($3.3\text{ V}$) and which is negative (`GND`) — some batch LEDs do not follow the standard long-leg-anode convention!

<div class="image-grid" markdown>
![Resistors inserted](pics/resistor_1.webp){ loading=lazy }
![Resistors soldered](pics/resistor_2.webp){ loading=lazy }
</div>

## 5. Soldering the MCU & OLED Sockets { #sockets }

1. Place the 40-way DIL MCU socket (or female headers) onto the front of the PCB and hold it flat with painter's tape.
2. Flip the board over, solder the diagonal corner pins first while pressing the socket flush against the PCB, verify alignment, and solder all remaining pins.
3. Repeat for the 4-pin OLED socket.

<div class="image-grid" markdown>
![MCU socket taped in place](pics/socket_1.webp){ loading=lazy }
![OLED socket placed](pics/socket_2.webp){ loading=lazy }
![Sockets soldered](pics/socket_3.webp){ loading=lazy }
</div>

## 6. Soldering Indicator LEDs { #leds }

!!! danger "LED Polarity"
    Insert each LED into the position matching its resistor (`R1` or `R2`). Ensure the **cathode (ground) leg goes into the square-plated hole**. Splay the legs, solder from the back, and trim flush.

<div class="image-grid" markdown>
![Indicator LEDs inserted](pics/led_1.webp){ loading=lazy }
![Indicator LEDs soldered](pics/led_2.webp){ loading=lazy }
</div>

## 7. Mounting & Soldering Switches { #switches }

1. Inspect your 5-pin switches to make sure no metal pins are bent, then press them firmly into the PCB until the plastic legs snap flush.
2. Sight down each row and column to confirm all switches sit level and straight.

!!! warning "Loose-Fitting Switches"
    Some switch housings (such as certain Kailh batches) fit slightly looser in PCB-mount holes. Place a flat hardcover book on top of the switches when flipping the board over so every switch stays seated flush against the PCB while soldering.

<div class="image-grid" markdown>
![Switches seated on front](pics/switches_1.webp){ loading=lazy }
![Switch pins ready to solder on back](pics/switches_2.webp){ loading=lazy }
</div>

## 8. Soldering the Rotary Encoder { #encoder }

Snap the EC11 rotary encoder into its footprint at the top-right corner. On earlier revisions (`Rev 1–8`), only the 3 rotational pins are routed; on `Rev 9+` and `m66`, all 5 signal pins (including the push-button switch) are active. Solder all signal pins as well as the two side mounting tabs for mechanical strength.

<div class="image-grid" markdown>
![Rotary encoder seated](pics/encoder_1.webp){ loading=lazy }
![Rotary encoder soldered](pics/encoder_2.webp){ loading=lazy }
</div>

!!! success "PCB Soldering Complete!"
    Your keyboard PCB assembly is now electrically complete.

## 9. Building the LEGO Enclosure & Final Testing { #the-box }

1. Assemble your LEGO base using a $16\times 32$ baseplate (or two $16\times 16$ plates) and perimeter $1\times 2$ / $1\times 4$ plates. For a $\sim 6^\circ$ typing angle, stack a full brick + plate along the top edge.
2. Add a sheet of hobbycraft foam inside the cavity for sound dampening, then align the PCB mounting holes over the perimeter LEGO studs and press down gently until the $1.6\text{ mm}$ PCB sits flush with the studs.
3. Seat the socketed MCU, OLED screen, and encoder knob, then plug in the USB cable.

<div class="image-grid" markdown>
![LEGO baseplate parts](pics/lego_1.webp){ loading=lazy }
![LEGO perimeter walls assembled](pics/lego_2.webp){ loading=lazy }
![PCB mounted on LEGO case](pics/final_1.webp){ loading=lazy }
![MCU and OLED seated](pics/final_2.webp){ loading=lazy }
</div>

!!! success "First Power-On Checklist"
    * **OLED Screen**: Displays "an elephant inside a boa constrictor" splash graphic for a few seconds, then switches to the active layer indicator and live WPM counter.
    * **Rotary Encoder**: Turning the knob adjusts system volume (`Vol+` / `Vol-`).
    * **Layer Tap-Dance LEDs**:
        * Double-tap the **3rd key from the left on the bottom row** (`Lower`): the first indicator LED next to the encoder lights up (double-tap again to toggle off).
        * Double-tap the **5th key from the left on the bottom row** (`Raise`): the second indicator LED lights up.
    * **Key Matrix**: Test every switch in a keyboard tester — then install your keycaps and enjoy!

![Finished mlego keyboard with keycaps](pics/final_3.webp){ loading=lazy }
