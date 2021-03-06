# keyboard-interceptor-micropython (esp32)
Proof-of-concept keyboard keystroke interceptor for PS/2 protocol proposed to be used with USB-to-ps/2 hardware downgrade

(wip)

#### Motivation
USB programming is hard. I'm lazy.
PS/2 is simple and practically readable by UART.
We want to explore the idea of rapid IOT enabled hardware exploit development.
ESP32 with micropython is good for rapid prototyping which makes it extremely suitable for this case.
 - Wifi is a breeze with micropython
 - WebRepl means we already have access to the device console so we don't even need to bother with comms (http://micropython.org/webrepl/#espresso0.local:8266/ )
   - But there is a simple MQTT library for comms, so why not
 - Encryption is possible
 - Code readability is superb
 - They're cheap and accessible 
 - We can power an ESP32 from the power line of PS/2 which is actually powered by USB in our case.

#### Goals
1. Interception
2. Blocking
3. Injection

#### Hardware Preparation Steps
1. Buy cheap USB->PS/2 and PS/2->USB to downgrade the communication protocol.
2. Strip out the CLK signal to measure the keyboard's baudrate.
3. Connect keyboard's data line to UART RX and connect UART TX to PC's data line.
4. Connect 5V supply to ESP32's 5V input (not tested yet). 

#### Software Preparation Steps
1. Download and install the latest micropython firmware from https://micrpython.org
2. (Preferred) Use VS Code + Pymakr to upload.

#### What software does
There are two tasks and a periodic timer that run in a round-robin manner (not great, not terrible).
1. UART task: polls the uart buffer for incoming bytes and "echoes" them (in reality they're forwarded to pc). Received chars are placed in a capture buffer, which is processed (not yet) and then published to an MQTT topic.
2. MQTT task: listens for MQTT messages and controls the software. Most notably it can inject keystrokes.
Timer: Sets the uart baudrate with respect to the recently measured clock frequency

#### Future Works &| Contribution Requests
Sure, why not. This will need and I will not bother with:
1. Keystroke processing; captured keystrokes are not really processed and converted to utf8 or similar. Would be better to actually do this processing. 
   - Some good references to actually implement processing of keyscan codes in the future
      - https://techdocs.altium.com/display/FPGA/PS2+Keyboard+Scan+Codes
      - https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
      - https://www.nutsvolts.com/magazine/article/get-ascii-data-from-ps-2-keyboards
1. Secure comms; either MQTT over TLS or something better than shared-key-AES. Even an HTTPS based REST API is acceptable. 
   - Regarding AES: currently available modes are CBC & CTR. https://docs.micropython.org/en/latest/library/ucryptolib.html
   - Regarding SSL (i think it's better to go SSL):https://github.com/micropython/micropython/pull/3398
1. WiFi AP option; instead of connecting to existing AP. Should be a hidden AP though.
   - Wifi AP: http://docs.micropython.org/en/v1.13/esp32/quickref.html#networking
1. Robustness upgrades; no idea what'll happen if WiFi &| MQTT disconnects.
