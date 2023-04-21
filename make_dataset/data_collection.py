# Python Script (use Python 3)
import serial
import time
import csv
from datetime import datetime
import keyboard
import threading

ser = serial.Serial('COM_PORT', 9600)  # Replace 'COM_PORT' with the appropriate port for your Arduino
csv_file = 'data.csv'
pressed_key = 0
stop_program = False
idx = 0

def check_keypress():
    global pressed_key, stop_program
    while True:
        key_event = keyboard.read_event(suppress=True)
        if key_event.event_type == keyboard.KEY_DOWN:
            pressed_key = key_event.name
            if pressed_key == 'esc':
                stop_program = True
                break
        else:
            pressed_key = 0

def main(delay_ms=100):
    global pressed_key, stop_program, idx
    key_thread = threading.Thread(target=check_keypress)
    key_thread.daemon = True
    key_thread.start()

    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
    while not stop_program:
        if ser.inWaiting():
            sensor_data = ser.readline().decode().strip()
            idx += 1
            timestamp = datetime.now().strftime('%F %S.%f')[:-4]
            key = pressed_key if pressed_key != 'esc' else 0
            data_point =[idx] + [timestamp] + sensor_data.split(',') + [key]
            print(data_point)
            writer.writerow(data_point)
            time.sleep(delay_ms/1000)

if __name__ == "__main__":
    main()