
#!/usr/bin/env python

import zmq
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# ZeroMQ Context Initialization
context = zmq.Context()
socket = context.socket(zmq.ROUTER)  # Using ROUTER for managing multiple clients
socket.bind("tcp://*:5555")

# Device Management
devices = {}
device_health = {}
command_history = []

def check_device_health():
    # Periodically check the health of connected devices.
    while True:
        for device_id in list(devices.keys()):
            try:
                socket.send_multipart([device_id, b"PING"])
                message = socket.recv_multipart(flags=zmq.NOBLOCK)
                if message[1] == b"PONG":
                    device_health[device_id] = 'Healthy'
            except zmq.Again:
                print(f"[WARNING] Device {device_id.decode()} did not respond.")
                device_health[device_id] = 'Unresponsive'
            time.sleep(1)  # Health check interval

def handle_client_message(client_id, message):
    # Handle incoming messages from clients.
    if message == b'REGISTER':
        devices[client_id] = {'status': 'Connected'}
        device_health[client_id] = 'Healthy'
        print(f"[INFO] New device registered: {client_id.decode()}")
    elif message.startswith(b'ERROR'):
        error_msg = message.decode()
        print(f"[ERROR] {error_msg}")
    else:
        print(f"[INFO] Message from {client_id.decode()}: {message.decode()}")

def receive_messages():
    # Continuously receive messages from clients.
    while True:
        client_id, message = socket.recv_multipart()
        handle_client_message(client_id, message)

def send_command_to_device(device_id, command):
    # Send a command to a specific device.
    if device_id in devices:
        socket.send_multipart([device_id.encode(), command.encode()])
        print(f"[INFO] Sent command '{command}' to device {device_id}")
        command_history.append((device_id, command))
    else:
        print(f"[ERROR] Device {device_id} not found.")

def list_devices():
    # List all connected devices and their status.
    print("Connected Devices:")
    for device_id, status in devices.items():
        print(f"  - {device_id.decode()}: {status['status']}, Health: {device_health.get(device_id, 'Unknown')}")

def command_line_interface():
    # Simple CLI for server management.
    while True:
        print("\nCommands: list, send [device_id] [command], history, exit")
        user_input = input("> ").strip().split()

        if not user_input:
            continue
        elif user_input[0] == 'list':
            list_devices()
        elif user_input[0] == 'send' and len(user_input) >= 3:
            send_command_to_device(user_input[1], ' '.join(user_input[2:]))
        elif user_input[0] == 'history':
            print("Command History:")
            for device, cmd in command_history:
                print(f"  - {device}: {cmd}")
        elif user_input[0] == 'exit':
            break
        else:
            print("[ERROR] Invalid command.")

# Main function
def main():
    # Main function to start server operations.
    print("[INFO] Starting ZeroMQ server...")
    
    # Start message receiving thread
    threading.Thread(target=receive_messages, daemon=True).start()
    
    # Start health check thread
    threading.Thread(target=check_device_health, daemon=True).start()

    # Start CLI for server management
    command_line_interface()

if __name__ == "__main__":
    main()
