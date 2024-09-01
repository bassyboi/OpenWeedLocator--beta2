#!/usr/bin/env python
import zmq
import os
import argparse
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from configparser import ConfigParser
import paramiko
from concurrent.futures import ThreadPoolExecutor
from utils.button_inputs import BasicController
from utils.image_sampler import ImageRecorder
from utils.blur_algorithms import fft_blur
from utils.greenonbrown import GreenOnBrown
from utils.relay_control import RelayController, StatusIndicator
from utils.frame_reader import FrameReader
from multiprocessing import Value, Process
from pathlib import Path
from datetime import datetime
from imutils.video import FPS
from utils.video import VideoStream
from time import strftime
import imutils
import sys
import cv2

# Add LiDARNode class to handle LiDAR operations
class LiDARNode:
    def __init__(self, lidar_port='/dev/ttyS0', baud_rate=115200, target_distance=1000, threshold=50):
        self.lidar_port = lidar_port
        self.baud_rate = baud_rate
        self.target_distance = target_distance
        self.threshold = threshold
        self.lidar_enabled = False  # Enable/disable flag

    def read_lidar_distance(self):
        """Function to read distance data from LiDAR."""
        # Example of reading from a serial port
        # Add actual LiDAR reading logic here
        return 1000  # Placeholder distance

    def control_actuator(self, current_distance):
        """Control the actuator based on LiDAR distance reading."""
        if not self.lidar_enabled:
            return

        # Logic to control actuator based on current_distance
        print(f"Controlling actuator: Current Distance = {current_distance}")

# Existing functions
def nothing(x):
    pass

def update_ini_file(file_path, new_content):
    """Function to update the .ini file."""
    with open(file_path, 'w') as file:
        file.write(new_content)
    print(f"Updated INI file at {file_path}")

def upload_model(model_path, destination_path):
    """Function to upload a model to the specified path."""
    os.system(f"scp {model_path} {destination_path}")
    print(f"Uploaded model to {destination_path}")

class ZeroMQServer:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.bind("tcp://*:5555")
        print("ZeroMQ Server started and bound to tcp://*:5555")

    def send_command(self, command):
        try:
            self.socket.send_string(command)
            print(f"Sent command: {command}")
            response = self.socket.recv_string()
            print(f"Received response: {response}")
            return response
        except Exception as e:
            print(f"Error sending command: {e}")
            return None

    def send_file_to_pi(self, hostname, username, password, local_path, remote_path):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=username, password=password)
            sftp = ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            ssh.close()
            print(f"Successfully sent {local_path} to {hostname}:{remote_path}")
            return True
        except Exception as e:
            print(f"Error sending file to {hostname}: {e}")
            return False

class Owl:
    def __init__(self, show_display=False, focus=False, input_file_or_directory=None,
                 config_file='config/DAY_SENSITIVITY_2.ini', lidar_node=None):
        self._config_path = Path(__file__).parent / config_file
        self.config = ConfigParser()
        self.config.read(self._config_path)
        self.lidar_node = lidar_node

    def update_config_file(self, new_config_file):
        self._config_path = Path(__file__).parent / new_config_file
        self.config.read(self._config_path)
        print(f"Configuration file updated to {self._config_path}")

    def boom_flush(self, duration=5):
        pass

    def stop_boom_flush(self):
        pass

    def hoot(self):
        if self.lidar_node and self.lidar_node.lidar_enabled:
            distance = self.lidar_node.read_lidar_distance()
            print(f"LiDAR Distance: {distance} mm")
            self.lidar_node.control_actuator(distance)

class ServerUI:
    def __init__(self, server):
        self.server = server
        self.config = ConfigParser()
        self.lidar_node = LiDARNode()  # Initialize LiDAR Node
        self.raspberry_pis = [
            {"hostname": "192.168.1.100", "username": "pi", "password": "raspberry"},
            {"hostname": "192.168.1.101", "username": "pi", "password": "raspberry"},
        ]
        self.root = tk.Tk()
        self.root.title("ZeroMQ Server Control Panel")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.create_system_tab()
        self.create_controller_tab()
        self.create_visualisation_tab()
        self.create_camera_tab()
        self.create_green_on_green_tab()
        self.create_green_on_brown_tab()
        self.create_data_collection_tab()
        self.create_relays_tab()
        self.create_lidar_tab()  # Add LiDAR configuration tab
        self.save_button = tk.Button(self.root, text="Save Configuration", command=self.save_configuration)
        self.save_button.grid(row=1, column=0, padx=5, pady=5)
        self.send_button = tk.Button(self.root, text="Send Config to Raspberry Pis", command=self.send_config_to_raspberry_pis)
        self.send_button.grid(row=2, column=0, padx=5, pady=5)

    def create_lidar_tab(self):
        """Create a tab for LiDAR configuration and control."""
        self.lidar_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.lidar_tab, text='LiDAR Control')
        self.lidar_enable_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.lidar_tab, text="Enable LiDAR", variable=self.lidar_enable_var).grid(row=0, column=0)
        self.lidar_distance_label = tk.Label(self.lidar_tab, text="LiDAR Distance: N/A")
        self.lidar_distance_label.grid(row=1, column=0)

    def save_configuration(self):
        self.config['System'] = {
            'algorithm': self.algorithm_entry.get(),
            'input_file_or_directory': self.input_entry.get(),
            'relay_num': self.relay_num_entry.get(),
            'actuation_duration': self.actuation_duration_entry.get(),
            'delay': self.delay_entry.get()
        }
        config_path = 'OpenWeedLocator/config/config.ini'
        with open(config_path, 'w') as configfile:
            self.config.write(configfile)
        messagebox.showinfo("Success", f"Configuration saved to {config_path}")

    def send_config_to_raspberry_pis(self):
        local_path = 'OpenWeedLocator/config/config.ini'
        remote_path = '/home/pi/OpenWeedLocator/config/config.ini'
        with ThreadPoolExecutor(max_workers=len(self.raspberry_pis)) as executor:
            futures = []
            for pi in self.raspberry_pis:
                futures.append(executor.submit(self.server.send_file_to_pi, pi['hostname'], pi['username'], pi['password'], local_path, remote_path))
            for future in futures:
                if future.result():
                    print("File sent successfully!")
                else:
                    print("Failed to send file to one of the Raspberry Pis.")
        messagebox.showinfo("Info", "Configuration file transfer completed.")

if __name__ == "__main__":
    server = ZeroMQServer()
    ap = argparse.ArgumentParser()
    ap.add_argument('--show-display', action='store_true', default=False, help='show display windows')
    ap.add_argument('--focus', action='store_true', default=False, help='add FFT blur to output frame')
    ap.add_argument('--input', type=str, default=None, help='path to image directory, single image or video file')
    ap.add_argument('--enable-lidar', action='store_true', help='Enable LiDAR node')

    args = ap.parse_args()
    lidar_node = LiDARNode() if args.enable_lidar else None

    owl = Owl(config_file='config/DAY_SENSITIVITY_2.ini',
              show_display=args.show_display,
              focus=args.focus,
              input_file_or_directory=args.input,
              lidar_node=lidar_node)

    zmq_process = Process(target=server.send_command, args=('Command example',))
    zmq_process.start()
    app = ServerUI(server)
    owl.hoot()
    zmq_process.join()
