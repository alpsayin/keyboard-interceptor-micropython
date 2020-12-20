
from widgets import TextArea
import colors
from machine import Pin, SPI
from ili9341 import ILI9341


display = None


def _center_justify(line, numcols):
    if len(line) >= numcols:
        return line
    return (' '*((numcols-len(line))//2))+line


def _right_justify(line, numcols):
    if len(line) >= numcols:
        return line
    return (' '*((numcols-len(line))))+line

class Display():
    def __init__(self):
        # super().__init__()
        self.display = None
        self.subtitle = ''
        # turn on the backlight
        self.backlight = Pin(5, Pin.OUT)
        self.backlight.value(0)

    def init_lcd(self):
        # use VSPI (ID=2) at 80mhz
        spi = SPI(
            2,
            baudrate=32000000,
            mosi=Pin(23, Pin.OUT),  # mosi = 23
            miso=Pin(25, Pin.IN),   # miso = 25
            sck=Pin(19, Pin.OUT)   # sclk = 19
        )
        self.display = ILI9341(
            spi,
            cs=Pin(22, Pin.OUT),          # cs   = 22
            dc=Pin(21, Pin.OUT),          # dc   = 21
            rst=Pin(18, Pin.OUT),         # rst  = 18
            width=240,
            height=320
        )
        self.display.fill(0)

    def wifi_connecting(self, wlan_ssid, wlan_key):
        txtarea = TextArea(
            self.display,
            10,
            24,
            x=10,
            y=10,
            bg=colors.RGB_BLACK,
            fg=colors.RGB_WHITE
        )
        txtarea.append("** Connecting to Wifi **")
        txtarea.append("------------------------")
        txtarea.append(wlan_ssid)
        # txtarea.append(wlan_key)
        txtarea.append('WLAN_KEY HIDDEN')
        txtarea.paint()

    def wifi_connected(self, ifconfig, dhcp_hostname):
        txtarea = TextArea(
            self.display,
            10,
            24,
            x=10,
            y=10,
            bg=colors.RGB_BLACK,
            fg=colors.RGB_WHITE
        )
        txtarea.lines = []
        txtarea.append("** CONNECTED **")
        txtarea.append("------------------------")
        txtarea.append("IP: %s" % ifconfig[0])
        txtarea.append("GW: %s" % ifconfig[2])
        txtarea.append("DNS: %s" % ifconfig[3])
        txtarea.append("Hostname: %s" % dhcp_hostname)
        txtarea.paint()

    def update_popup(self, cmd='', subtitle=None):
        if subtitle is not None:
            self.subtitle = subtitle
        numcols = 9
        numlines = 6
        txtarea = TextArea(
            self.display,
            numlines,
            numcols,
            x=80,
            y=240,
            bg=colors.RGB_WHITE,
            fg=colors.RGB_BLACK,
            border=colors.RGB_PURPLE
        )
        txtarea.append('@alpsayin')
        txtarea.append('---------')
        txtarea.append(self.subtitle)
        txtarea.append('---------')
        for line in cmd.splitlines():
            center_aligned_line = _center_justify(line, numcols)
            txtarea.append(center_aligned_line)
        txtarea.paint()
