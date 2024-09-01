!/usr/bin/env python

import zmq
import time
from threading import Thread

# ZeroMQ Client Setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://<SERVER_IP>:5555")  # Replace <SERVER_IP> with actual server IP

def register_device():
    # Register LiDAR device with the server
    socket.send(b'REGISTER')
    print(socket.recv().decode())

def lidar_health_check():
    # Perform periodic health checks
    while True:
        socket.send(b'PING')
        response = socket.recv().decode()
        if response == 'PONG':
            print("[INFO] LiDAR is operating normally.")
        else:
            print("[WARNING] LiDAR health check failed.")
        time.sleep(10)

def main():
    # Main function to run LiDAR operations
    register_device()
    Thread(target=lidar_health_check, daemon=True).start()
    
    # Example of LiDAR operation loop
    while True:
        # Simulate LiDAR distance measurement
        distance = 1.0  # Replace with actual LiDAR measurement logic
        print(f"[INFO] LiDAR distance measurement: {distance} meters")
        time.sleep(1)

if __name__ == "__main__":
    main()
