
#!/usr/bin/env python

import zmq
import time
import threading
from utils.camera_handler import CameraHandler
from utils.greenonbrown import GreenOnBrown
from utils.relay_controller import RelayController
from utils.error_handler import ErrorHandler

# ZeroMQ Client Setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://<SERVER_IP>:5555")  # Replace <SERVER_IP> with actual server IP

def register_device():
    # Register OWL device with the server
    socket.send(b'REGISTER')
    print(socket.recv().decode())

def receive_commands():
    # Receive commands from the server and execute
    while True:
        socket.send(b'REQUEST_COMMAND')
        command = socket.recv().decode()
        if command == 'STOP':
            print("[INFO] Stopping OWL operations.")
            break
        else:
            print(f"[INFO] Executing command: {command}")
            # Add command execution logic here

def main():
    # Main function to run OWL operations
    register_device()
    threading.Thread(target=receive_commands, daemon=True).start()
    
    # Example of OWL operation loop
    camera = CameraHandler()
    weed_detector = GreenOnBrown()
    relay = RelayController()

    while True:
        frame = camera.capture_frame()
        weeds = weed_detector.detect_weeds(frame)
        relay.control_relays(weeds)
        time.sleep(1)

if __name__ == "__main__":
    main()
