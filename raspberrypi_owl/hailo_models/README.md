Open Weed Locator (OWL) - Green-on-Green Integration
Overview

Welcome to the Open Weed Locator (OWL) with Green-on-Green in-crop weed detection, now adapted for use with the Hailo AI acceleration module. This guide provides steps for setting up the hardware and software on a Raspberry Pi 5 and outlines the process of running and training weed recognition models with the Hailo AI module. Please note, this adaptation has not yet been tested and is considered experimental.
Prerequisites

    Raspberry Pi 5 with Raspberry Pi OS installed
    Hailo AI acceleration module with the Raspberry Pi M.2 HAT+
    Access to the internet on Raspberry Pi
    Open Weed Locator (OWL) software repository cloned to your device

Installation
Step 1: Software Setup

    Clone the OWL Repository:

    bash

git clone [] ~/owl
cd ~/owl

Install the Hailo SDK: Navigate to the models directory and run the installation script tailored for the Hailo AI module. This script will install all necessary dependencies and configure the Hailo AI module for use.

bash

cd models
chmod +x install_hailo.sh
./install_hailo.sh

If you encounter any issues during the installation, ensure that you are working within the correct virtual environment:

bash

    workon owl  # Activate the virtual environment; adjust as needed based on your setup
    pip install hailo-sdk

Step 2: Verifying Installation

After installation, verify that the Hailo SDK is correctly installed by importing it in a Python shell:

bash

python
>>> import hailo_sdk
>>> exit()

Running the Detection Model

With the Hailo AI module set up, you can now run the weed detection model.

    Download a Compatible Model: Ensure that you have a Hailo-compatible model file in the models directory. If unsure, download a test model:

    bash

wget [Link to a Hailo-compatible model]  # Replace with actual URL

Execute the Detection Script: Return to the OWL root directory and run the detection script using the Hailo AI module.

bash

    cd ..
    python owl.py --show-display --algorithm hailo
Model Training and Deployment

To successfully train and deploy your own models on the Hailo AI module:

    Training Models: Follow detailed guides provided by Hailo or available through community resources that explain how to train models compatible with the Hailo AI hardware. These resources will typically include specific steps on data preparation, model architecture considerations, and training procedures that are optimized for Hailo's AI technology.

    Optimization and Conversion: Once your models are trained, ensure they are converted and optimized for deployment on the Hailo AI module. This process may involve using Hailo’s own tools or specific commands that prepare the model to run efficiently on the Hailo hardware.

Troubleshooting

If you encounter issues during the setup or operation of your Hailo AI module or the Open Weed Locator software:

    Installation Checks: Verify that all components are installed correctly. Revisit the installation steps to ensure that nothing was missed and that all software components are compatible with your version of the Raspberry Pi and Hailo module.

    Software Compatibility: Ensure that your operating system and all libraries are up to date. Compatibility issues between the software and hardware can lead to unexpected errors.

    Hardware Connections: Double-check all hardware connections, especially the seating of the Hailo AI module in the Raspberry Pi M.2 HAT+. Loose connections can cause failures in detecting the module.

    Error Logs: Review the error logs for any specific messages that might indicate what went wrong. This can provide clues on whether the issue is related to software, hardware, or model performance.

    Consult Documentation: Use the Hailo AI module documentation for specific troubleshooting steps. The manufacturer’s support can offer detailed guidance and technical support for dealing with complex issues.

    Community Forums: If the issue persists, consider seeking help from community forums where other users may have encountered and resolved similar problems.
