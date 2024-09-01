## README: LiDAR-Based Height Control System with Networked Communication
# Overview

This project implements a LiDAR-based height control system using a Raspberry Pi to maintain a set distance (approximately 1 meter) over crops using hydraulics or an electrical actuator. The system is integrated into a network of Raspberry Pi nodes, each with a specific purpose, using ZeroMQ for communication. This enables coordinated operations across different nodes in the network.
Components

Raspberry Pi: Serves as the main controller for the LiDAR sensor and actuator control.

LiDAR Sensor: Used for measuring the distance from the sensor to the crop.

Actuator or Hydraulic System: Adjusts the height of the system to maintain the desired distance.

ZeroMQ Library: Facilitates network communication between multiple Raspberry Pi nodes.

Motor Driver or Relay Module: Controls the actuator or hydraulic system.

## Installation

Install Dependencies:
Ensure your Raspberry Pi is updated:

   

sudo apt-get update
sudo apt-get upgrade

## Install necessary Python libraries:



    sudo apt-get install python3-pip
    pip3 install RPi.GPIO pyserial pyzmq
    sudo apt-get install libzmq3-dev

## Connect Hardware:

Connect the LiDAR sensor to the Raspberry Pi via UART or I2C.
    
Connect the actuator or hydraulic system to the appropriate GPIO pins via a motor driver or relay module.

## Clone the Repository:

Clone this repository to your Raspberry Pi:

    bash

    git clone <repository-url>
    cd <repository-directory>

## Run the LiDAR Node Script:

 Run the LiDAR node script to start distance measurement and height control:



    python3 lidar_control.py

## Run the Central Command Node:

 On a different Raspberry Pi or central server, run the command center script to receive data and manage commands:

   

        python3 command_center.py

## Usage

LiDAR Node: Continuously measures the distance to the crops and adjusts the height of the system using an actuator or hydraulic system.

Central Command Node: Receives data from the LiDAR node and other nodes, allowing for centralized decision-making and command dissemination.

## Configuration

Modify lidar_control.py and command_center.py to set up specific IP addresses, ports, 

target distances, thresholds, and GPIO pins as per your setup requirements.

## Network Communication

The system uses ZeroMQ with a PUB-SUB model for communication between nodes. The LiDAR node publishes distance data, and the central command node subscribes to these messages to process them and potentially send commands back.

## Troubleshooting

Ensure all dependencies are installed.

Verify correct hardware connections.

Check network configurations and ensure all devices are on the same network.

Test individual components (LiDAR, actuators) separately to ensure they function correctly before integration.

## Future Enhancements

Implement security features like encrypted communication.

Expand the network to include more nodes with different purposes.

Add a graphical user interface (GUI) for easier control and monitoring.