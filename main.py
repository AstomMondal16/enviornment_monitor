from machine import UART, Pin, I2C
import utime
from TB600B import TB600B_CO as TB600B
from ze40b import ZE40B
from SSD1306 import SSD1306_I2C
import time

# Initialize UART
uart = UART(1, 9600, tx=41, rx=42)
uart.init(9600, bits=8, parity=None, stop=1)

# Initialize TB600B sensor
sensor = TB600B(uart)

# Initialize ZE40B sensor
# sensor_ze40b = ZE40B(uart_num=1, tx_pin=41, rx_pin=42, baud_rate=9600)

# Initialize I2C and OLED display
i2c = I2C(0, sda=Pin(4), scl=Pin(5))
oled = SSD1306_I2C(128, 32, i2c)

# Expected Behavior: Repeat forever
while True:
    # Clear the OLED screen
    oled.fill(0)
    
    # Turn LED on for TB600B sensor
    sensor.led_on()
    
    # Check if the sensor is in Q&A mode, if not, change mode
    if not sensor.qna:
        print("Changing mode to Q&A...")
        sensor.changeMode()
    
    # Print all sensor data (if applicable)
    sensor_data = sensor.read_all()
    
    # Turn LED off after reading
    sensor.led_off()
    
    # Switch to Q&A mode using ZE40B instance
    print("Switching to Q&A mode...")
    sensor_ze40b.set_qa_mode()  # Call on the instance of ZE40B
    
    # Request gas concentration data from ZE40B
    print("Requesting gas concentration...")
    try:
        concentration = sensor_ze40b.read_concentration()  # Read gas concentration from ZE40B
        print(f"Gas Concentration: {concentration['ppb']} ppb, "
              f"{concentration['mg/m3']:.3f} mg/m³, "
              f"{concentration['ppm']:.3f} ppm")
        
        # Display sensor data on OLED in the desired order
        oled.text("Temp: {:.2f}C".format(sensor_data['temperature']), 0, 0)
        oled.text("Humidity: {:.2f}%".format(sensor_data['humidity']), 0, 10)
        oled.show()
        time.sleep(2)
        
        oled.fill(0)
        oled.text("co: {:.2f} ug/m3".format(sensor_data['gas_ugm3']), 0, 0)
        oled.text("voc:{} ppb".format(concentration['ppb']), 0, 10)
        oled.show()
    
    except Exception as e:
        print(f"Error reading concentration: {e}")
    
    # Wait 5 seconds before taking the next reading
    utime.sleep(30)
