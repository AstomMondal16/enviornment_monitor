from machine import UART, Pin, I2C
import time
#from ssd1306 import SSD1306_I2C

# Initialize I2C and OLED display
# i2c = I2C(0, sda=Pin(4), scl=Pin(5))
# oled = SSD1306_I2C(128, 32, i2c)

# Define UART pins and configuration
TX_PIN = 40
RX_PIN = 39
BAUD_RATE = 9600

# Commands for the TB600B_TVOC_10 sensor
ACTIVE_MODE = b'\xFF\x01\x78\x40\x00\x00\x00\x00\x47'
PASSIVE_MODE = b'\xFF\x01\x78\x41\x00\x00\x00\x00\x46'
READ_GAS = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'
READ_ALL = b'\xFF\x01\x87\x00\x00\x00\x00\x00\x78'
LIGHT_OFF = b'\xFF\x01\x88\x00\x00\x00\x00\x00\x77'
LIGHT_ON = b'\xFF\x01\x89\x00\x00\x00\x00\x00\x76'


def send_command(command):
    """Send a command to the sensor and read the response."""
    uart.write(command)
    time.sleep(0.1)  # Wait for the sensor to respond
    if uart.any():
        response = uart.read()
        return response
    return None

def set_active_mode():
    """Set the sensor to active mode."""
    return send_command(ACTIVE_MODE)

def set_passive_mode():
    """Set the sensor to passive mode."""
    return send_command(PASSIVE_MODE)

def led_off():
    """Turns sensor LED OFF"""
    uart.write(LIGHT_OFF)
    time.sleep(0.5)

def led_on():
    """Turns sensor LED ON"""
    uart.write(LIGHT_ON)
    time.sleep(0.5)


def read_gas_concentration():
    """Read the gas concentration from the sensor."""
    response = send_command(READ_GAS)
    if response and len(response) >= 9:
        high_byte = response[2]
        low_byte = response[3]
        concentration = ((high_byte << 8) | low_byte) / 1000.0
        return round(concentration, 3)
    return None

def read_all_data():
    """Read gas concentration, temperature, and humidity."""
    response = send_command(READ_ALL)
    if response and len(response) >= 13:
        gas_high = response[2]
        gas_low = response[3]
        temp_high = response[8]
        temp_low = response[9]
        hum_high = response[10]
        hum_low = response[11]

        gas_concentration = round(((gas_high << 8) | gas_low) / 1000.0, 3)
        temperature = round(((temp_high << 8) | temp_low) / 100.0, 3)
        humidity = round(((hum_high << 8) | hum_low) / 100.0, 3)

        return gas_concentration, temperature, humidity
    return None


# Example usage
if __name__ == "__main__":
    # Initialize UART
    uart = UART(1, baudrate=BAUD_RATE, tx=Pin(TX_PIN), rx=Pin(RX_PIN))

    print("Initializing sensor...")
    set_active_mode()
    time.sleep(2)

    while True:
#         oled.fill(0)
        led_on()
        gas = read_gas_concentration()
        if gas is not None:
            print(f"Gas Concentration: {gas:.3f} ppm")
#             oled.text(f"Gas: {gas:.3f} ppm", 0, 0)
#             oled.show()

        data = read_all_data()
        if data:
            gas, temp, hum = data
            print(f"Gas: {gas:.3f} ppm, Temp: {temp:.3f} C, Humidity: {hum:.3f}%")
#             oled.text(f"Gas: {gas:.3f} ppm", 0, 0)
#             oled.text(f"Temp: {temp:.3f} C", 0, 10)
#             oled.text(f"Humidity: {hum:.3f}%", 0, 20)
#             oled.show()

        led_off()
        time.sleep(5)
