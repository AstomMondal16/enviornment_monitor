import machine
import time

# Default UART parameters
DEFAULT_UART_NUM = 1
DEFAULT_TXD_PIN = 7
DEFAULT_RXD_PIN = 8
DEFAULT_BAUD_RATE = 9600

# Commands
QA_MODE_CMD = b'\xFF\x01\x78\x41\x00\x00\x00\x00\x46'
READ_CONCENTRATION_CMD = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'

class ZE40B:
    def __init__(self, uart_num=DEFAULT_UART_NUM, tx_pin=DEFAULT_TXD_PIN, rx_pin=DEFAULT_RXD_PIN, baud_rate=DEFAULT_BAUD_RATE):
        """
        Initialize the ZE40B sensor with UART configuration.
        
        :param uart_num: UART port number
        :param tx_pin: GPIO pin for UART TX
        :param rx_pin: GPIO pin for UART RX
        :param baud_rate: Baud rate for UART communication
        """
        self.uart = machine.UART(uart_num, baudrate=baud_rate, tx=tx_pin, rx=rx_pin, timeout=1000)

    def send_command(self, cmd):
        """
        Send a command to the sensor.
        
        :param cmd: Byte command to send
        """
        self.uart.write(cmd)

    def read_data(self, length):
        """
        Read data from the sensor.
        
        :param length: Number of bytes to read
        :return: Byte array of data read
        """
        return self.uart.read(length)

    @staticmethod
    def calculate_checksum(data):
        """
        Calculate the checksum for a data packet.
        
        :param data: Byte array of data
        :return: Calculated checksum value
        """
        checksum = sum(data[1:8]) & 0xFF
        return (~checksum + 1) & 0xFF

    @staticmethod
    def parse_gas_concentration(data):
        """
        Parse the gas concentration from the sensor data packet.
        
        :param data: Byte array of data
        :return: Dictionary with gas concentration in different units
        :raises ValueError: If the data is invalid
        """
        if data[0] != 0xFF:
            raise ValueError("Invalid start byte.")

        checksum = ZE40B.calculate_checksum(data)
        if checksum != data[8]:
            raise ValueError("Checksum mismatch.")

        concentration_ppb = (data[2] << 8) | data[3]
        concentration_mg_m3 = concentration_ppb / 1000.0
        concentration_ppm = concentration_ppb / 1000.0
        return {
            "ppb": concentration_ppb,
            "mg/m3": concentration_mg_m3,
            "ppm": concentration_ppm
        }

    def set_qa_mode(self):
        """
        Switch the sensor to Q&A mode.
        """
        self.send_command(QA_MODE_CMD)
        time.sleep(0.1)

    def read_concentration(self):
        """
        Read the gas concentration from the sensor.
        
        :return: Dictionary with gas concentration in different units
        :raises ValueError: If the response is invalid
        """
        self.send_command(READ_CONCENTRATION_CMD)
        response = self.read_data(9)
        if response and len(response) >= 9:
            return self.parse_gas_concentration(response)
        else:
            raise ValueError("Invalid response or no data received.")
