import zmq
import serial  # For UART communication with LiDAR
import time
import RPi.GPIO as GPIO

# Configuration for LiDAR and Actuator
LIDAR_PORT = "/dev/ttyS0"  # Adjust for your setup
BAUD_RATE = 115200  # Adjust for your LiDAR
TARGET_DISTANCE = 1000  # Target distance in millimeters (1 meter)
THRESHOLD = 50  # Allowable deviation in millimeters

# GPIO setup for actuator control
ACTUATOR_UP_PIN = 17  # Adjust to your GPIO pin for actuator up
ACTUATOR_DOWN_PIN = 27  # Adjust to your GPIO pin for actuator down

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ACTUATOR_UP_PIN, GPIO.OUT)
GPIO.setup(ACTUATOR_DOWN_PIN, GPIO.OUT)

def read_lidar_distance():
    """Read distance from LiDAR sensor."""
    try:
        with serial.Serial(LIDAR_PORT, BAUD_RATE, timeout=1) as lidar:
            lidar.flush()
            if lidar.in_waiting > 0:
                distance_data = lidar.readline().decode('utf-8').strip()
                return int(distance_data)
    except (serial.SerialException, ValueError) as e:
        print(f"Error reading LiDAR distance: {e}")
    return None

def control_actuator(current_distance):
    """Control the actuator based on LiDAR distance reading."""
    if current_distance > TARGET_DISTANCE + THRESHOLD:
        # Move actuator down
        GPIO.output(ACTUATOR_UP_PIN, GPIO.LOW)
        GPIO.output(ACTUATOR_DOWN_PIN, GPIO.HIGH)
        print("Actuator moving down...")
    elif current_distance < TARGET_DISTANCE - THRESHOLD:
        # Move actuator up
        GPIO.output(ACTUATOR_DOWN_PIN, GPIO.LOW)
        GPIO.output(ACTUATOR_UP_PIN, GPIO.HIGH)
        print("Actuator moving up...")
    else:
        # Stop actuator
        GPIO.output(ACTUATOR_UP_PIN, GPIO.LOW)
        GPIO.output(ACTUATOR_DOWN_PIN, GPIO.LOW)
        print("Actuator stopped.")

def main():
    # ZeroMQ Context
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://<SERVER_IP>:5555")  # Replace <SERVER_IP> with the server's IP address

    print("LiDAR client connected to server. Ready to send distance data and receive commands...")

    try:
        while True:
            # Read distance from LiDAR sensor
            distance = read_lidar_distance()

            if distance is not None:
                print(f"LiDAR Distance: {distance} mm")
                # Send distance data to server
                socket.send_string(f"DISTANCE {distance}")
                
                # Receive response from server
                response = socket.recv_string()
                print(f"Received response: {response}")

                # Check for specific commands from the server
                if response.startswith("CONTROL_ACTUATOR"):
                    # Control actuator based on received command
                    control_actuator(distance)
                elif response.startswith("UPDATE_INI"):
                    # Handle other commands like updating configuration files
                    print("Update INI command received.")
                    # Add code to update INI files if necessary
                elif response.startswith("UPLOAD_MODEL"):
                    # Handle model uploads
                    print("Upload model command received.")
                    # Add code to upload model if necessary

            # Sleep to prevent excessive data transmission
            time.sleep(1)
    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
