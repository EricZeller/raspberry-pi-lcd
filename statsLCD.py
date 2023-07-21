import drivers
import time
from datetime import datetime
import psutil
from gpiozero import CPUTemperature

display = drivers.Lcd()

counter = 0

try:
    print("Writing...")
    while True:
        cpu = CPUTemperature()
        cputemp = str(round(cpu.temperature, 1))

        cpupercent = str(psutil.cpu_percent())
        # Calculate memory information
        memory = psutil.virtual_memory()
        # Convert Bytes to MB (Bytes -> KB -> MB)
        available = round(memory.available/1024.0/1024.0/1024.0,2)
        total = round(memory.total/1024.0/1024.0/1024.0,2)
        used = round(total - available, 2)
        mem_info = str(memory.percent) + "% / " + str(used) + " GB"

        # Calculate disk information
        disk = psutil.disk_usage('/')
        # Convert Bytes to GB (Bytes -> KB -> MB -> GB)
        free = round(disk.free/1024.0/1024.0/1024.0,2)
        total = round(disk.total/1024.0/1024.0/1024.0,2)
        disk_info = str(free) + " GB free"
        
        display.lcd_display_string("Time: " + time.strftime("%H:%M:%S"), 1)
        display.lcd_display_extended_string("CPU: " + cputemp + "{0xDF}" + "C / " + cpupercent + "%  ", 2)
        display.lcd_display_string("RAM: " + mem_info, 3)
        display.lcd_display_string("Disk: " + disk_info, 4)
        time.sleep(0.75)
        counter += 1
        if counter > 60:
            display.lcd_clear()
            counter = 0
            
except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()
    display.lcd_display_string("Stopped at " + time.strftime("%H:%M:%S"), 1)
