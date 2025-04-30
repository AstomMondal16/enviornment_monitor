from machine import UART
import utime
#Commands
ACTIVE_MODE = b'\xFF\x01\x78\x40\x00\x00\x00\x00\x47'
PASSIVE_MODE = b'\xFF\x01\x78\x41\x00\x00\x00\x00\x46'
READ_GAS = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'
READ_ALL = b'\xFF\x01\x87\x00\x00\x00\x00\x00\x78'
LIGHT_OFF = b'\xFF\x01\x88\x00\x00\x00\x00\x00\x77'
LIGHT_ON = b'\xFF\x01\x89\x00\x00\x00\x00\x00\x76'

class TB600B_CO:
    def __init__(self,uart):
        self.uart = uart
        self.qna = True
    
    def send_command(self,cmd):
        """
        Sends a command in QnA mode and returns the reply received from UART
        """
        self.uart.write(cmd) #Writes the desired command
        utime.sleep(1) #Do not remove, this is a processing time
        return self.uart.read() #Returns the reply sent from the sensor
    
    def changeMode(self):
        """Changes between active upload and QnA mode. Active upload gives a lot of faulty data. Better to use passive."""
        if self.qna==True:
            self.send_command(ACTIVE_MODE)
            self.qna = False
        else:
            self.send_command(PASSIVE_MODE)
            self.qna = True
    
    def led_off(self):
        """Turns sensor LED OFF"""
        self.send_command(LIGHT_OFF)
    
    def led_on(self):
        """Turns sensor LED ON"""
        self.send_command(LIGHT_ON)
    
    def read_gas(self):
        """Reads only the Gas value"""
        if self.qna==True:
            gas_array = self.send_command(READ_GAS)
        else:
            utime.sleep(1)
            gas_array = self.uart.read()
        gas_array = list(gas_array)
        return gas_array[2]*256 + gas_array[3] #Conversion into actual values, given in datasheet
    
    def read_all(self):
        """Reads only the Gas values in ug/m3, ppb, temperature and humidity"""
        if self.qna==False:
            raise(Exception("You should be in QNA mode to do this. Call changeMode()?"))
        all_array = self.send_command(READ_ALL)
        all_array = list(all_array)
        readings = {}
        readings["gas_ugm3"] = all_array[2]*256 + all_array[3] #Conversion into actual values, given in datasheet
        readings["gas_ppb"] = all_array[6]*256 + all_array[7] #Conversion into actual values, given in datasheet
        readings["temperature"] = ((all_array[8] <<8) | all_array[9])/100 #Conversion into actual values, given in datasheet
        readings["humidity"] = ((all_array[10]<<8) | all_array[11])/100 #Conversion into actual values, given in datasheet
        return readings