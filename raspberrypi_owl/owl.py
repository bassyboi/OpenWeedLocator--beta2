#!/usr/bin/env python

import argparse
import zmq
import threading
import cv2
import imutils
from utils.camera_handler import CameraHandler
from utils.relay_control import RelayController
from utils.weed_detection import GreenOnBrown, GreenOnGreen

# ZeroMQ Client Setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://<SERVER_IP>:5555")  # Replace <SERVER_IP> with actual server IP


def register_device():
    """Register OWL device with the server."""
    socket.send(b'REGISTER')
    print(socket.recv().decode())


def receive_commands():
    """Receive commands from the server and execute them."""
    while True:
        socket.send(b'REQUEST_COMMAND')
        command = socket.recv().decode()
        if command == 'STOP':
            print("[INFO] Stopping OWL operations.")
            break
        else:
            print(f"[INFO] Executing command: {command}")
            # Add command execution logic here if needed


def owl_operations(show_display, focus, input_file_or_directory, algorithm):
    """Main function to run OWL operations."""
    # Initialize camera, relay controller, and weed detection based on selected algorithm
    camera = CameraHandler(resolution=(640, 480))  # Set the desired resolution
    relay_controller = RelayController(relay_dict={1: 11, 2: 13})  # Example relay dict

    # Choose weed detection algorithm based on user input
    if algorithm == 'gog':
        weed_detector = GreenOnGreen(
            model_path='path/to/model.tflite')  # Replace with actual model path
    else:
        weed_detector = GreenOnBrown()

    camera.start()  # Start the camera

    # Main processing loop
    while True:
        frame = camera.read()

        # Skip processing if the frame is not captured properly
        if frame is None:
            print("[INFO] Frame is None. Stopping...")
            break

        # Perform weed detection using the chosen algorithm
        if algorithm == 'gog':
            cnts, boxes, weed_centres, image_out = weed_detector.inference(
                frame, confidence=0.5)
        else:
            cnts, boxes, weed_centres, image_out = weed_detector.detect_weeds(
                frame)

        # Control relays based on detected weed positions
        relay_controller.control_relays(weed_centres)

        # Display the output if the show-display flag is set
        if show_display:
            cv2.imshow("Detection Output", imutils.resize(image_out, width=800))
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                print("[INFO] Exiting...")
                break

    # Stop the camera and cleanup
    camera.stop()
    cv2.destroyAllWindows()


def main():
    """Main function that registers the OWL device and starts operations."""
    # Parse command-line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('--show-display', action='store_true', default=False,
                    help='show display windows')
    ap.add_argument('--focus', action='store_true', default=False,
                    help='add FFT blur to output frame')
    ap.add_argument('--input', type=str, default=None,
                    help='path to image directory, single image or video file')
    ap.add_argument('--algorithm', type=str, default='gob',
                    choices=['gob', 'gog'],
                    help='algorithm to use: GreenOnBrown (gob) or GreenOnGreen (gog)')

    args = ap.parse_args()

    # Register the device with the server
    register_device()

    # Start the thread to receive commands from the server
    threading.Thread(target=receive_commands, daemon=True).start()

    # Start OWL operations
    owl_operations(show_display=args.show_display,
                   focus=args.focus,
                   input_file_or_directory=args.input,
                   algorithm=args.algorithm)


if __name__ == "__main__":
    main()
