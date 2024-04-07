import webview
import threading
import serial
import serial.tools.list_ports
import pygame
import queue
import sys
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
simulated_serial_data = queue.Queue()

pygame.init()
pygame.mixer.init()
com_port = "COM4"  # Example: COM3, change this as needed
baud_rate = 9600  # Set the baud rate

# Global variables
latest_command = None
serial_connection = None
current_file = None
monitored_port = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def play_audio(file_name):
    global current_file
    file_path = resource_path(file_name)  # Get the correct file path
    if not pygame.mixer.music.get_busy() or current_file != file_path:
        pygame.mixer.music.load(file_path)  # Load the file from the correct path
        pygame.mixer.music.play()
        current_file = file_path


def stop_audio():
    pygame.mixer.music.stop()

def read_serial_data():
    global latest_command, serial_connection, current_file
    while True:
        command_received = False
        if not simulated_serial_data.empty():
            latest_command = simulated_serial_data.get().strip()
            command_received = True
            print(f"Simulated Received: {latest_command}")
        elif serial_connection and serial_connection.in_waiting > 0:
            latest_command = serial_connection.readline().decode('utf-8').strip()
            command_received = True
            print(f"Actual Received: {latest_command}")

        if command_received and latest_command != current_file:
            if latest_command == "leftB" or latest_command == "rightB" or latest_command == "buzzer": 
                play_audio("buzzer.wav")
            elif latest_command == "endgame":
                play_audio("endgame.wav")
            elif latest_command == "horn":
                play_audio("horn.wav")
            elif latest_command == "weapon":
                play_audio("weapon.wav")
            elif latest_command == "feet":
                play_audio("feet.wav")
            elif latest_command == "A0":  # STOP AUDIO
                stop_audio()

        
def start_serial_monitoring(port):
    global serial_connection
    try:
        if serial_connection:
            serial_connection.close()  # Close the existing connection if open
        serial_connection = serial.Serial(port, baud_rate, timeout=1)
        threading.Thread(target=read_serial_data, daemon=True).start()
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_ports')
def list_ports():
    ports = serial.tools.list_ports.comports()
    return jsonify([port.device for port in ports])

@app.route('/send_command', methods=['POST'])
def send_command():
    global serial_connection, simulated_serial_data
    command = request.form['command']
    if serial_connection and serial_connection.is_open:
        serial_connection.write(command.encode())
        # Simulate the command as if it is coming from the serial port
        simulated_serial_data.put(command)
        return jsonify({'status': 'success', 'command': command})
    else:
        return jsonify({'status': 'error', 'message': 'Serial port not open'})


@app.route('/get_latest_command')
def get_latest_command():
    return jsonify({'command': latest_command})

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    global monitored_port, serial_connection, latest_command
    port = request.form['port']
    monitored_port = port
    latest_command = ""  # Clear the latest command when a new port is selected
    if serial_connection:
        serial_connection.close()  # Close the existing connection if open
    start_serial_monitoring(port)
    return jsonify({'status': 'success', 'message': f'Monitoring started on {port}'})

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False), daemon=True).start()
    webview.create_window("Com Port Serial Interchanger", "http://localhost:5000/")

    webview.start()