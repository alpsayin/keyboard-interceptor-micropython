# keyboard-interceptor-esp
Proof-of-concept keyboard keystroke interceptor for PS/2 protocol proposed to be used with USB-to-ps/2 hardware downgrade

(wip)

#### Motivation
USB programming is hard. I'm lazy.
PS/2 is simple and practically readable by UART.
We want to explore the idea of rapid IOT enabled hardware exploit development.
ESP32 with micropython is good for rapid prototyping which makes it extremely suitable for this case.
 - Wifi is a breeze with micropython
 - Can use MQTT for comms, because why not
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
2. Need to grab LCD library from https://github.com/alpsayin/micropython-esp32-wrover-lcd:
   1. Either clone the repository with its original name to the same directory you clone this repo.
   1. Or copy the py files into lib folder 
3. (Preferred) Use VS Code + Pymakr to upload.

#### What software does
There are two tasks that run in a round-robin manner (not great, not terrible).
1. UART task: polls the uart buffer for incoming bytes and "echoes" them (in reality they're forwarded to pc). Received chars are placed in a capture buffer, which is processed (not yet) and then published to an MQTT topic.
2. MQTT task: listens for MQTT messages and controls the software. Most notably it can inject keystrokes.

#### Future Works &| Contribution Requests
Sure, why not. This will need and I will not bother with:
1. Keystroke processing; captured keystrokes are not really processed and converted to utf8 or similar. Would be better to actually do this processing. 
1. Secure comms; either MQTT over TLS or something better than shared-key-AES. Even an HTTPS based REST API is acceptable. 
1. WiFi AP option; instead of connecting to existing AP. Should be a hidden AP though.
1. Robustness upgrades; no idea what'll happen if WiFi &| MQTT disconnects.
