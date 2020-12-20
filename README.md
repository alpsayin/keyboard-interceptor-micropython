# keyboard-interceptor-esp
Proof-of-concept keyboard keystroke interceptor for PS/2 protocol proposed to be used with USB-to-ps/2 hardware downgrade

(wip)

#### Motivation
USB programming is hard. I'm lazy.
PS/2 is simple and practically readable by UART.
We want to explore the idea of rapid IOT enabled hardware exploit development
ESP32 with micropython is good for rapid prototyping which is very suitable for this case.
 - wifi is a breeze with micropython
 - can use MQTT for comms, because why not
 - encryption is possible
 - code readability is superb
 - they're cheap 
 - We can power an ESP32 from the power line of PS/2 which is actually powered by USB in our case.

#### Goals
1. Interception
2. Blocking
3. Injection

#### Steps
1. Buy cheap USB->PS/2 and PS/2->USB to downgrade the communication protocol.
2. Strip out the CLK signal to measure the keyboard's baudrate.
3. Connect keyboard's data line to UART RX and connect UART TX to PC's data line.

#### Contributions
Sure, why not. This will need and I will not bother with:
1. Secure comms; either MQTT over TLS or something better than shared-key-AES.
2. WiFi AP option instead of connecting to existing AP. Should be a hidden AP though.
