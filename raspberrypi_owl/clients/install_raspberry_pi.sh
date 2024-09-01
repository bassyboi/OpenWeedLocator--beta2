#!/bin/bash

# Update and upgrade system
sudo apt-get update && sudo apt-get upgrade -y

# Install necessary packages
sudo apt-get install -y sshpass rsync

# Generate SSH keys if they don't already exist
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""
fi

# Configure passwordless SSH to the main server
MAIN_SERVER_IP="<YOUR_WINDOWS_PC_IP>"
MAIN_SERVER_USER="<YOUR_WINDOWS_PC_USERNAME>"
SSH_PORT=22

# Copy the SSH key to the main server
sshpass -p '<YOUR_WINDOWS_PC_PASSWORD>' ssh-copy-id -o StrictHostKeyChecking=no -p $SSH_PORT $MAIN_SERVER_USER@$MAIN_SERVER_IP

# Create the sync script
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
(crontab -l 2>/dev/null; echo "0 * * * * ~/sync_ip_to_server.sh") | crontab -

# Notify the user
echo "Installation and setup complete. The Raspberry Pi will now sync with the main server every hour."