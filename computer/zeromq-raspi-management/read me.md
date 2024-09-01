ZeroMQ-Based Raspberry Pi Management System

This project provides a framework for managing multiple Raspberry Pi devices from a central computer using ZeroMQ for communication. The system allows the central computer to send commands to Raspberry Pi devices to perform tasks such as updating .ini configuration files, uploading models, and executing other operations.
Table of Contents

    Overview
    Features
    Architecture
    Requirements
    Setup
        Central Computer (Server)
        Raspberry Pi Devices (Clients)
    Usage
    Commands
    Security Considerations
    Contributing
    License

Overview

This project enables a command-and-control approach where a central computer (server) communicates with multiple Raspberry Pi devices (clients) over WiFi using ZeroMQ. The Raspberry Pis run models and can be remotely configured by sending commands from the central server. The system avoids the need for a central broker and supports decentralized, high-performance communication.
Features

    Decentralized Communication: Uses ZeroMQ for direct communication between the server and clients.
    Remote Configuration: Allows changing .ini configuration files and uploading models remotely.
    Flexible Command Handling: Easily extendable to add new commands and functionalities.
    High Performance: Designed for low-latency, high-throughput communication over WiFi.
    Scalable: Supports multiple Raspberry Pi clients connected to a single central server.

Architecture

    Central Computer (Server): Acts as the command center, sending commands to Raspberry Pi devices to perform tasks.
    Raspberry Pi Devices (Clients): Each device listens for commands from the server, performs the required tasks (e.g., updating files, uploading models), and sends back a response.

Requirements

    ZeroMQ and PyZMQ installed on all devices (server and clients).
    Python 3.x installed on all devices.

Setup
Central Computer (Server)

    Install ZeroMQ and PyZMQ:

    bash

sudo apt-get install libzmq3-dev
pip install pyzmq

Clone the Repository:

bash

git clone https://github.com/yourusername/your-repo.git
cd your-repo

Run the Server Script:

bash

    python server.py

Raspberry Pi Devices (Clients)

    Install ZeroMQ and PyZMQ:

    bash

sudo apt-get install libzmq3-dev
pip install pyzmq

Clone the Repository:

bash

git clone https://github.com/yourusername/your-repo.git
cd your-repo

Edit client.py to Connect to the Server's IP Address:

    Replace <SERVER_IP> with the IP address of the central computer in the client.py file:

    python

    SERVER_IP = "<SERVER_IP>"  # Replace with the central computer's IP address

Run the Client Script:

bash

    python client.py

Usage

    Start the Server:
        Run the server.py script on the central computer to start listening for commands.

    Start the Clients:
        Run the client.py script on each Raspberry Pi device. Ensure they are connected to the same network as the central computer.

    Send Commands from the Server:
        Enter commands in the server terminal to instruct the Raspberry Pi devices to perform tasks. For example, UPDATE_INI, UPLOAD_MODEL, etc.

Commands

    UPDATE_INI: Updates the .ini configuration file on the Raspberry Pi devices. The specific file and content are defined in the client.py script.
    UPLOAD_MODEL: Uploads a model file to a specified path on the Raspberry Pi devices. The source and destination paths are defined in the client.py script.

You can customize and add more commands in the handle_command() function in client.py.
Security Considerations

    Network Security: Ensure that your network is secure and not exposed to unauthorized access. Use strong WiFi passwords and consider using a VPN.
    Authentication and Encryption: ZeroMQ does not provide built-in security. You can implement CurveZMQ for encrypted communication and authenticated connections.
    File Transfers: When uploading models or changing files, ensure paths are validated to prevent malicious file manipulation.

Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes.
License

This project is licensed under the MIT License - see the LICENSE file for details.