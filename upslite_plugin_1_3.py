# Based on pisugar3.py from https://github.com/taiyonemo
# Made specifically to address the problems not fully resolved by the UPS-Lite python plugin available publicly by PhreakBoutique. Auto-Shutdown feature fixed and recovered as well.
#
# To setup, please read the README.md available below;
# https://github.com/taichikuji/UPSLite_Plugin_1_3/blob/main/README.md

import logging
import struct
import time

from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi

class UPSLite:
    CW2015_ADDRESS = 0x62
    CW2015_REG_VCELL = 0x02
    CW2015_REG_SOC = 0x04
    CW2015_REG_MODE = 0x0A

    def __init__(self):
        # Only import when the module is loaded and enabled
        import smbus
        self._bus = smbus.SMBus(1)
        self.quick_start()

    def quick_start(self):
        try:
            self._bus.write_word_data(self.CW2015_ADDRESS, self.CW2015_REG_MODE, 0x30)
        except Exception as e:
            logging.error(f"[upslite] Error during QuickStart: {e}")

    def capacity(self):
        try:
            read = self._bus.read_word_data(self.CW2015_ADDRESS, self.CW2015_REG_SOC)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            return swapped / 256  # Convert to percentage
        except Exception as e:
            logging.error(f"[upslite] Failed to read battery capacity: {e}")
            return 0

    def voltage(self):
        try:
            read = self._bus.read_word_data(self.CW2015_ADDRESS, self.CW2015_REG_VCELL)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            return swapped * 0.305 / 1000  # Convert to volts
        except Exception as e:
            logging.error(f"[upslite] Failed to read battery voltage: {e}")
            return 0

class UPSLitePlugin(plugins.Plugin):
    __author__ = 'Taichikuji'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin that adds a percentage indicator for UPS-Lite'

    def __init__(self):
        self.ups = None

    def on_loaded(self):
        self.ups = UPSLite()
        logging.info("[upslite] Plugin loaded.")

    def on_ui_setup(self, ui):
        try:
            ui.add_element('bat', LabeledValue(color=BLACK, label='BAT', value='0%', 
                                               position=(ui.width() / 2 + 10, 0), 
                                               label_font=fonts.Bold, text_font=fonts.Medium))
        except Exception as err:
            logging.warning(f"[upslite] UI setup error: {err}")

    def on_unload(self, ui):
        try:
            with ui._lock:
                ui.remove_element('bat')
        except Exception as err:
            logging.warning(f"[upslite] UI unload error: {err}")

    def on_ui_update(self, ui):
        try:
            capacity = self.ups.capacity()
            if capacity == 0:
                logging.warning("[upslite] Battery capacity read as 0, possible issue with I2C communication.")

            ui.set('bat', f"{int(capacity)}%")
            if capacity <= self.options.get('shutdown', 5):  # Shutdown threshold
                logging.info('[upslite] Battery capacity low. Preparing to shut down.')
                capacities = [capacity]
                for _ in range(5):
                    time.sleep(0.5)
                    capacities.append(self.ups.capacity())
                max_capacity = max(capacities)
                if max_capacity <= self.options.get('shutdown', 5):
                    logging.info('[upslite] Battery exhausted. Shutting down.')
                    ui.update(force=True, new_data={'status': 'Battery exhausted, bye ...'})
                    pwnagotchi.shutdown()
        except Exception as e:
            logging.error(f"[upslite] Error updating UI: {e}")
