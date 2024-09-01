
# OpenWeedLocator beta2 Project

## Project Overview
OpenWeedLocator is a comprehensive system designed for precision agriculture, focusing on weed detection and management. The project is divided into three main components:
1. **Computer**: Central server-side management for coordinating operations across Raspberry Pi devices using ZeroMQ.
2. **Raspberry Pi OWL**: Weed detection and relay control using machine learning models on Raspberry Pi devices.
3. **LiDAR Raspberry Pi**: Height control system for maintaining a set distance over crops using LiDAR on Raspberry Pi.

## Directory Structure

### 1. `computer/`
This directory contains scripts and tools for server-side management and central coordination of Raspberry Pi devices.

- **`zeromq-raspi-management/`**: Server-side scripts for managing communication with Raspberry Pi devices using ZeroMQ.
- **`dev/`**: Development-related scripts and utilities.
- **`docs/`**: Documentation for the project.
- **`README.md`, `CONTRIBUTING.md`, `LICENSE`, `CITATION.cff`, `CODE_OF_CONDUCT.md`**: Project documentation and licenses.
- **`non_rpi_requirements.txt`**, **`environment.yml`**: Dependency files for non-Raspberry Pi environments.

### 2. `raspberrypi_owl/`
Contains all necessary scripts and models to run the OWL (Open Weed Locator) application on Raspberry Pi devices for weed detection and relay control.

- **`owl.py`**: Main script for running weed detection and relay control.
- **`utils/`**: Utility scripts for algorithms, video handling, relay control, data logging, and more.
- **`config/`**: Configuration files for OWL operations.
- **`coral_models/`**, **`hailo_models/`**: Machine learning models for Coral Edge TPU and Hailo devices.
- **`display/`**, **`images/`**: Display assets and images used by OWL.
- **`clients/`**: Client-side scripts for ZeroMQ communication with the central computer.
- **`logs/`**: Log files generated during OWL operations.
- **`3D Models/`**: 3D models for physical setups of the OWL system.
- **Shell Scripts (`owl_boot.sh`, `owl_boot_wrapper.sh`, `owl_setup.sh`, `update_owl.sh`, `focus_owl.sh`)**: Scripts for setting up, managing, and updating the OWL system on Raspberry Pi.

### 3. `lidar_raspberrypi/`
Contains scripts and configurations for LiDAR-based height control systems on Raspberry Pi devices.

- **`rasberrypi lidar boom height/`**: Scripts and configurations specific to the LiDAR height control system.

## Setup Instructions

### 1. Setting Up the Main Computer
- Install necessary dependencies using `non_rpi_requirements.txt` or `environment.yml`.
- Configure and run the ZeroMQ server-side scripts located in `computer/zeromq-raspi-management/server`.

### 2. Setting Up Raspberry Pi for OWL
- Install dependencies listed in `raspberrypi_owl/requirements.txt`.
- Run `owl_setup.sh` to set up the OWL system.
- Use `owl.py` to start the weed detection system. Command-line arguments can be used for configuration (e.g., `--show-display`, `--focus`, `--input`).

### 3. Setting Up Raspberry Pi for LiDAR
- Navigate to `lidar_raspberrypi/rasberrypi lidar boom height`.
- Follow specific setup instructions in the documentation provided within the directory.

## Usage Instructions

### Running the OWL Detection System
- Run `owl.py` with appropriate configuration and model paths.
- Monitor output via display or command-line interface.

### Managing LiDAR Height Control
- Ensure all necessary hardware is connected and configured.
- Run the LiDAR scripts to maintain the set distance over crops.

### Using ZeroMQ Management System
- Start the ZeroMQ server on the main computer.
- Run the client-side scripts from `raspberrypi_owl/clients` on Raspberry Pi devices.

## Dependencies and Requirements
- **Computer**: See `non_rpi_requirements.txt` and `environment.yml` for server-side dependencies.
- **Raspberry Pi (OWL)**: See `raspberrypi_owl/requirements.txt` for necessary Python libraries and tools.
- **Raspberry Pi (LiDAR)**: Check specific requirements in `lidar_raspberrypi/rasberrypi lidar boom height`.

## Troubleshooting and Support
- Ensure all dependencies are correctly installed.
- Verify that hardware components are connected and functioning.
- Check log files in `raspberrypi_owl/logs/` for error messages.
- Refer to `docs/` for detailed documentation and guides.

## Contributions and Support
See `CONTRIBUTING.md` for guidelines on contributing to this project. For any issues or support, please refer to the project's `CODE_OF_CONDUCT.md` and open an issue on the GitHub repository.

