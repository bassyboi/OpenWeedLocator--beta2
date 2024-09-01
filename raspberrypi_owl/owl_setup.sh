#!/bin/bash

# Function to display a loading screen or progress indicator
show_loading() {
  echo -ne "[INFO] $1 in progress...\r"
  sleep 1
  echo -ne "[INFO] $1 in progress...\r"
}

# Function to check the exit status of the last executed command and log it
check_status() {
  if [ $? -ne 0 ]; then
    echo "[ERROR] $1 failed. Check the logs for more details." | tee -a owl_setup.log
    exit 1
  else
    echo "[INFO] $1 completed successfully." | tee -a owl_setup.log
  fi
}

# Create a log file for setup process
echo "[INFO] Starting OWL Raspberry Pi setup..." > owl_setup.log

# Free up space
show_loading "Freeing up space by removing unnecessary packages"
echo "[INFO] Freeing up space by removing unnecessary packages..." | tee -a owl_setup.log
sudo apt-get purge -y wolfram-engine >> owl_setup.log 2>&1
sudo apt-get purge -y libreoffice* >> owl_setup.log 2>&1
sudo apt-get clean >> owl_setup.log 2>&1
check_status "Cleaning up"

sudo apt-get autoremove -y >> owl_setup.log 2>&1
check_status "Removing unnecessary packages"

# Update the system and firmware
show_loading "Updating the system and firmware"
echo "[INFO] Updating the system and firmware..." | tee -a owl_setup.log
sudo apt-get update && sudo apt-get upgrade -y >> owl_setup.log 2>&1
check_status "System update and upgrade"

sudo rpi-update >> owl_setup.log 2>&1
check_status "Firmware update"

# Install required libraries for GUI
show_loading "Installing required libraries for GUI"
echo "[INFO] Installing required libraries for GUI..." | tee -a owl_setup.log
sudo apt-get install -y python3-tk python3-pil python3-pil.imagetk >> owl_setup.log 2>&1
check_status "Installing Python libraries for GUI"

# Set up the virtual environment
show_loading "Setting up the virtual environment"
echo "[INFO] Setting up the virtual environment..." | tee -a owl_setup.log
sudo apt-get install -y python3-virtualenv python3-virtualenvwrapper >> owl_setup.log 2>&1
check_status "Installing virtual environment tools"

echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
check_status "Updating .bashrc for virtualenvwrapper"

# Create and activate a virtual environment
show_loading "Creating and activating virtual environment 'owl_env'"
echo "[INFO] Creating and activating virtual environment 'owl_env'..." | tee -a owl_setup.log
mkvirtualenv owl_env -p python3 >> owl_setup.log 2>&1
check_status "Creating virtual environment 'owl_env'"

workon owl_env
check_status "Activating virtual environment 'owl_env'"

# Install Python dependencies from requirements.txt
show_loading "Installing Python dependencies"
echo "[INFO] Installing Python dependencies from requirements.txt..." | tee -a owl_setup.log
pip install -r requirements.txt >> owl_setup.log 2>&1
check_status "Installing Python dependencies"

# Install Python dependencies for clients from 'clients/requirements.txt'
show_loading "Installing Python dependencies for clients"
echo "[INFO] Installing Python dependencies for clients..." | tee -a owl_setup.log
pip install -r clients/requirements.txt >> owl_setup.log 2>&1
check_status "Installing Python dependencies for clients"

# Copy 'clients' folder to a proper location
show_loading "Setting up client scripts"
echo "[INFO] Copying client scripts to /home/pi/clients..." | tee -a owl_setup.log
mkdir -p /home/pi/clients
cp -r clients/* /home/pi/clients/
check_status "Copying client scripts"

# Create a systemd service file to run OWL on boot
show_loading "Creating systemd service file"
echo "[INFO] Creating systemd service file for OWL..." | tee -a owl_setup.log

SERVICE_FILE=/etc/systemd/system/owl.service

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=OWL Service to Run on Boot
After=network.target

[Service]
User=pi  # Replace 'pi' with your Raspberry Pi user if different
WorkingDirectory=/home/pi/raspberrypi_owl  # Replace with your OWL directory
ExecStart=/home/pi/.virtualenvs/owl_env/bin/python /home/pi/raspberrypi_owl/owl.py  # Replace with the path to your Python script
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

check_status "Creating systemd service file"

# Create a systemd service file to run the clients on boot
show_loading "Creating systemd service file for clients"
echo "[INFO] Creating systemd service file for clients..." | tee -a owl_setup.log

CLIENT_SERVICE_FILE=/etc/systemd/system/clients.service

sudo bash -c "cat > $CLIENT_SERVICE_FILE" <<EOL
[Unit]
Description=Clients Service to Run on Boot
After=network.target

[Service]
User=pi  # Replace 'pi' with your Raspberry Pi user if different
WorkingDirectory=/home/pi/clients  # Replace with your clients directory
ExecStart=/home/pi/.virtualenvs/owl_env/bin/python /home/pi/clients/client.py  # Replace with the main client script
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

check_status "Creating clients systemd service file"

# Reload systemd, enable, and start the services
show_loading "Enabling and starting OWL and clients services"
echo "[INFO] Enabling and starting OWL and clients services..." | tee -a owl_setup.log
sudo systemctl daemon-reload >> owl_setup.log 2>&1
check_status "Reloading systemd"

sudo systemctl enable owl.service >> owl_setup.log 2>&1
check_status "Enabling OWL service"

sudo systemctl start owl.service >> owl_setup.log 2>&1
check_status "Starting OWL service"

sudo systemctl enable clients.service >> owl_setup.log 2>&1
check_status "Enabling clients service"

sudo systemctl start clients.service >> owl_setup.log 2>&1
check_status "Starting clients service"

# Notify completion
echo "[INFO] OWL Raspberry Pi setup completed successfully!" | tee -a owl_setup.log
echo "[INFO] OWL and Clients will run automatically on boot." | tee -a owl_setup.log
