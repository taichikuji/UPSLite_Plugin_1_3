# UPS-Lite Plugin for Pwnagotchi

This plugin is based on pisugar3.py script, which is in itself based on UPS_Lite 1.1. This plugin is made to work with UPS-Lite 1.3 by XiaoJ.

## 🛠️ Key Changes from PiSugar Script

### 1. **Replaced I2C Address and Registers**
   - **Modified (`UPS-Lite`)**: 
     - Changed I2C address to `0x62` for the CW2015 chip.
     - Added CW2015-specific registers:
       - `CW2015_REG_SOC` (`0x04`): Reads battery capacity as a percentage.
       - `CW2015_REG_VCELL` (`0x02`): Reads battery voltage in volts.
       - `CW2015_REG_MODE` (`0x0A`): For initializing the chip (QuickStart).

---

### 2. **QuickStart Initialization**
   - Added a `quick_start()` method to initialize the CW2015 fuel gauge chip and trigger its fuel-gauge calculations.
   Note: CW2015 takes a while to start and requires a "two-run" process to properly read the battery, as experienced previously myself.

---

### 3. **Battery Capacity and Voltage Methods**
   - **Added**:
     - `capacity()` method to fetch battery percentage.
     - `voltage()` method to monitor battery voltage (optional for display).

---

### 4. **UI Integration**
   - The plugin now dynamically updates the battery percentage on the Pwnagotchi UI.

---

### 5. **Low Battery Shutdown**
   - Implemented a feature to check battery levels and shut down the device when capacity falls below a configurable threshold.
   - Adds a multiple-sample verification to ensure accurate capacity readings before triggering shutdown.

---

## 💾 Installation Instructions
1. Save the plugin file as `upslite.py` in the Pwnagotchi plugins directory:
   ```bash
   /usr/local/share/pwnagotchi/plugins/custom-plugins/upslite.py
   ```
2. Update your `config.toml` file:
   ```toml
   main.plugins.upslite.enabled = true
   main.plugins.upslite.shutdown = 5  # Shutdown at 5% battery
   ```
3. Restart Pwnagotchi service or reboot the device itself:
   ```bash
   sudo systemctl restart pwnagotchi
   ```
    or:

   ```bash
   sudo reboot now
   ```

---

### 🔧 Configuration Options
- **`shutdown`**: Set the battery percentage threshold for automatic shutdown. Defaults to `5%`.

---

### 📋 Notes
- Ensure that this **[guide](https://github.com/linshuqin329/UPS-Lite/blob/master/UPS-Lite_V1.3_CW2015/Instructions%20for%20UPS-Lite%20V1.3.pdf)** is followed properly before proceeding. By the end of this guide, you should have a Python script named `UPS_Lite_V1.3_CW2015.py` that properly executed on your home folder.
- Ensure the I2C interface is enabled on your Raspberry Pi via `raspi-config`.
- Install required dependencies:
  ```bash
  sudo apt-get install -y python3-smbus i2c-tools
  ```