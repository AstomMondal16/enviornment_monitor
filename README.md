# Air Quality Monitoring System

This project involves interfacing three key air quality sensors — the **PMSA003A** dust sensor, **TB600B** CO sensor, and **ZE40B** VOC sensor — to monitor particulate matter (PM), carbon monoxide (CO), and volatile organic compounds (VOC) in the environment. This system is designed to be used with a microcontroller like an ESP32 or similar.

## Sensors Overview

### 1. PMSA003A (Plantower) - Dust Sensor
- Measures particulate matter concentrations: PM1.0, PM2.5, and PM10.
- Communicates via UART.
- Operating voltage: 5V
- Data format: Structured binary with checksum.

### 2. TB600B - Carbon Monoxide (CO) Sensor
- Electrochemical sensor for detecting CO concentrations.
- Analog output that requires ADC for microcontroller readings.
- Output range typically 0–3V depending on concentration.

### 3. ZE40B - VOC Sensor (MH-ZE40B)
- Detects multiple volatile organic compounds including formaldehyde and other harmful gases.
- Communicates via UART.
- Returns gas concentrations in ppm.
- Operating voltage: 5V

## Features

- Real-time air quality data collection.
- Support for UART and analog sensors.
- Easy integration with ESP32, Raspberry Pi, Arduino, etc.
- Extendable for LoRa, MQTT, or cloud-based applications.

## Wiring Summary

| Sensor          | Interface | TX Pin | RX Pin | Power | Notes                              |
|-----------------|-----------|--------|--------|-------|------------------------------------|
| **PMSA003A**    | UART      | 11     | 12     | 5V    | Use `UART(1, baudrate=9600, tx=11, rx=12)` |
| **TB600B**      | UART      | 41     | 42     | 5V    | Use `UART(1, 9600, tx=41, rx=42)` |
| **ZE40B (CO)**  | UART      | 7      | 8      | 5V    | Use `DEFAULT_UART_NUM = 1, DEFAULT_TXD_PIN = 7, DEFAULT_RXD_PIN = 8` |
| **SCD4x (I2C)** | I2C       | 4      | 5      | 3.3V  | Use `I2C(0, sda=Pin(4), scl=Pin(5))` |

## Installation

1. **Hardware Setup:**
   - Connect each sensor according to the pin configuration listed in the table above.
   - Ensure the correct power (5V for sensors and 3.3V for I2C devices) is supplied to the sensors.
  
2. **Software Setup:**
   - Install the required libraries for your microcontroller environment (e.g., MicroPython or Arduino).
   - Flash the firmware to your microcontroller.

3. **Running the System:**
   - Once powered up, the system will begin collecting air quality data from the sensors.
   - You can use the serial monitor to observe the real-time data output.

## Sample Output

The following data can be expected from the sensors:

PM1.0: 12 µg/m³ PM2.5: 18 µg/m³ PM10: 20 µg/m³ CO: 5.4 ppm VOC: 0.12 ppm

## Libraries / Dependencies

- **PMSA003A**: Custom UART parser for the PMSA003A dust sensor.
- **TB600B**: Use an ADC pin to read the analog output.
- **ZE40B**: UART communication library to read the VOC sensor.
- **SCD4x**: I2C library for reading the SCD4x sensor.

### Python Dependencies (if using Raspberry Pi):
- `pyserial` for UART communication
- `machine` and `time` for MicroPython (if used)

## Notes

- **PMSA003A** should be placed vertically for optimal airflow.
- **TB600B (CO sensor)** requires calibration and might have an analog output range of 0-3V, requiring ADC to measure.
- **ZE40B (VOC sensor)** communicates via UART and may require a custom parser.
- **SSD1306** uses I2C for communication with the display.

## References

- [PMSA003A Datasheet (Plantower)](https://files.particle.io/datasheets/PM2.5-sensor/PMSA003A-Series-DataMan-EN-v2.6.pdf)
- [ZE40B Datasheet](https://www.winsen-sensor.com/d/files/PDF/Gas%20Sensor/ZE40B.pdf)
- [TB600B_CO](https://ecsense.com/wp-content/uploads/2021/01/TB600B_CO_10ppm_Technical-Specification20200513.pdf)
- [SSD1306](https://robu.in/wp-content/uploads/2019/12/ER-OLEDM0.91-1_Datasheet_617717.pdf)


---

Developed by Astom Mondal

