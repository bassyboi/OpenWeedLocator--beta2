#!/bin/bash

# Update and upgrade the system
echo "Updating and upgrading the system..."
sudo apt-get update && sudo apt-get upgrade -y

# Install necessary packages for LiDAR communication and GPIO control
echo "Installing necessary packages..."
sudo apt-get install -y python3-pip python3-serial sshpass rsync

# Install Python libraries for LiDAR communication and GPIO control
echo "Installing Python libraries..."
pip3 install RPi.GPIO pyserial zmq

# Generate SSH keys if they don't already exist
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "Generating SSH keys..."
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""
fi

# Configure passwordless SSH to the main server
MAIN_SERVER_IP="<YOUR_WINDOWS_PC_IP>"
MAIN_SERVER_USER="<YOUR_WINDOWS_PC_USERNAME>"
SSH_PORT=22

# Copy the SSH key to the main server
echo "Configuring passwordless SSH to the main server..."
sshpass -p '<YOUR_WINDOWS_PC_PASSWORD>' ssh-copy-id -o StrictHostKeyChecking=no -p $SSH_PORT $MAIN_SERVER_USER@$MAIN_SERVER_IP

# Create the sync script to sync IP to the main server and pull configuration files
echo "Creating sync script..."
cat <<EOL > ~/sync_ip_to_server.sh
#!/bin/bash
HOSTNAME=\$(hostname)
IP_ADDRESS=\$(hostname -I | awk '{print \$1}')
DATE=\$(date +"%Y-%m-%d %H:%M:%S")

# Sync IP and hostname to the main server
echo "\$HOSTNAME,\$IP_ADDRESS,\$DATE" | ssh -p $SSH_PORT $MAIN_SERVER_USER@$MAIN_SERVER_IP "cat >> ~/raspberry_pi_ips.txt"

# Sync configuration files from the main server to Raspberry Pi
rsync -avz -e "ssh -p $SSH_PORT" $MAIN_SERVER_USER@$MAIN_SERVER_IP:/path/to/server/config/ /home/pi/OpenWeedLocator/config/
EOL

# Make the sync script executable
chmod +x ~/sync_ip_to_server.sh

# Add cron job to run the sync script every hour
echo "Adding cron job for hourly sync..."
(crontab -l 2>/dev/null; echo "0 * * * * ~/sync_ip_to_server.sh") | crontab -

# Create a Python script to run the LiDAR-based system
echo "Creating LiDAR control script..."
cat <<EOF > ~/lidar_control.py
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
        GPIO.output(ACTUATOR_UP_PIN, GPIO.LOW)
        GPIO.output(ACTUATOR_DOWN_PIN, GPIO.HIGH)
        print("Actuator moving down...")
    elif current_distance < TARGET_DISTANCE - THRESHOLD:
        GPIO.output(ACTUATOR_DOWN_PIN, GPIO.LOW)
        GPIO.output(ACTUATOR_UP_PIN, GPIO.HIGH)
        print("Actuator moving up...")
    else:
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
            distance = read_lidar_distance()
            if distance is not None:
                print(f"LiDAR Distance: {distance} mm")
                socket.send_string(f"DISTANCE {distance}")
                response = socket.recv_string()
                print(f"Received response: {response}")

                if response.startswith("CONTROL_ACTUATOR"):
                    control_actuator(distance)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Client shutting down...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
EOF

# Make the Python script executable
chmod +x ~/lidar_control.py

# Create a systemd service file to run the LiDAR script on startup
echo "Creating systemd service to run LiDAR script on startup..."
cat <<EOL | sudo tee /etc/systemd/system/lidar_control.service
[Unit]
Description=LiDAR Control Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/lidar_control.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable lidar_control.service
sudo systemctl start lidar_control.service

# Notify the user
echo "LiDAR installation and setup complete. The LiDAR control system will run on startup."
