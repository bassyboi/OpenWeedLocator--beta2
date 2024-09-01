# PowerShell script to manage Raspberry Pi connections using ZeroMQ
# This script allows managing device registrations, sending commands, and checking device status

# Define server connection details
$serverAddress = "tcp://localhost:5555"

# Function to send a command to the server
function Send-Command {
    param (
        [string]$DeviceID,
        [string]$Command
    )

    Write-Host "Sending command '$Command' to device '$DeviceID'..."
    # Implement ZeroMQ client to send command
    python -c "import zmq; ctx = zmq.Context(); sock = ctx.socket(zmq.REQ); sock.connect('$serverAddress'); sock.send_string('$DeviceID $Command'); print(sock.recv_string())"
}

# Function to list all connected devices
function List-Devices {
    Write-Host "Requesting list of connected devices..."
    # Implement ZeroMQ client to request device list
    python -c "import zmq; ctx = zmq.Context(); sock = ctx.socket(zmq.REQ); sock.connect('$serverAddress'); sock.send_string('list'); print(sock.recv_string())"
}

# Main script loop
while ($true) {
    Write-Host "Options: list, send [DeviceID] [Command], exit"
    $input = Read-Host "Enter your command"

    if ($input -eq "list") {
        List-Devices
    } elseif ($input -match "^send (\S+) (.+)$") {
        $DeviceID = $matches[1]
        $Command = $matches[2]
        Send-Command -DeviceID $DeviceID -Command $Command
    } elseif ($input -eq "exit") {
        break
    } else {
        Write-Host "Invalid command."
    }
}
