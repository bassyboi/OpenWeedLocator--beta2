### Open Weed Locator (OWL) System - Operator's Manual

This Operator's Manual provides comprehensive instructions for using the Open Weed Locator (OWL) system in the field. The OWL system is designed to detect weeds in agricultural fields using advanced computer vision and machine learning techniques. It allows operators to control sprayers or other actuators based on weed detection or perform a "Boom Flush" to treat an entire area.
Table of Contents

 System Configuration
    Operating the OWL System
    Using the Boom Flush Feature
    Adjusting and Customizing Settings
    Troubleshooting Guide
    Safety and Best Practices

## System Configuration

Before operating the OWL system, make sure to configure it properly:

 INI Configuration File: The system uses a configuration file (config/DAY_SENSITIVITY_2.ini) to set all operational parameters such as camera settings, detection thresholds, relay control, and data collection.
        Navigate to the config folder and open the DAY_SENSITIVITY_2.ini file.
        Adjust settings like camera resolution, exposure compensation, detection thresholds, and relay control pins based on your field setup and equipment.

Relay Setup: Ensure that each relay number is correctly mapped to the corresponding GPIO pin on your control device. This is configured in the [Relays] section of the INI file.

## Operating the OWL System

To operate the OWL system, follow these steps:

 Starting the OWL Program: Run the OWL script from the command line with optional parameters:

    python owl.py --show-display --focus --input <path_to_input_file_or_directory>

 --show-display: Optional. If enabled, it shows the video feed with detection overlays.
 
 --focus: Optional. Adds FFT blur analysis to help evaluate image clarity.
 
 --input: Optional. Specifies the path to an image directory, single image, or video file to process. If not provided, the camera feed will be used.


## System Controls During Operation:
     
Activate Boom Flush: Press B key to activate all connected sprayers or devices for a defined period.
Stop Boom Flush: Press E key to immediately turn off all devices.
Save Detection Settings: Press S key to save the current detection settings to a new configuration file.
Exit the System: Press Esc key to safely stop all operations and shut down connected devices.


## Using the Boom Flush Feature

The Boom Flush feature allows all connected relays (e.g., sprayers) to activate at once for a specified duration, ideal for treating large areas uniformly.

 Starting Boom Flush: Press B while the system is running.
 Stopping Boom Flush: Press E to turn off all relays immediately.

To adjust the duration of the Boom Flush, modify the hoot() method in owl.py:

python

self.boom_flush(duration=5)

Change the duration to the desired time in seconds.
Adjusting and Customizing Settings

 Change Detection Algorithms: Switch between algorithms (GreenOnGreen, GreenOnBrown, etc.) in the config/DAY_SENSITIVITY_2.ini file under the [System] section:

   ini

   algorithm = gog  # Options: gog (GreenOnGreen) or gob (GreenOnBrown)

   Adjust Detection Thresholds: If --show-display is enabled, use the on-screen trackbars to adjust thresholds like ExG, Hue, Saturation, and Brightness during runtime.

   Configuring Relay Controls: Update the relay mapping in the [Relays] section of the INI file to match your field equipment setup.

   Data Collection Mode: Enable or disable data collection by setting sample_images to True or False in the [DataCollection] section. Specify the sampling method (whole, centered, etc.) and frequency for image capture.


## Troubleshooting Guide

Missing Software Modules: If you receive a "ModuleNotFoundError," install the missing Python package:

    
    pip install <missing_module>

Device Connection Issues: Check all connections (cameras, relays, etc.) and ensure they are configured correctly. Restart the OWL system if problems persist.

Algorithm-Related Errors: Verify that the detection algorithm is correctly specified and that all required model files are in place. For Coral device users, ensure it is properly connected.

## Safety and Best Practices

Ensure Safety: Before using the Boom Flush feature or any automated controls, make sure the area is clear of people, animals, and equipment that should not be exposed to chemicals or treatments.
Verify Setup: Double-check that all devices, such as relays and sprayers, are properly set up and tested for simultaneous operation.
Monitor System Performance: Regularly check logs and relay statuses to detect any potential errors or malfunctions early, ensuring smooth and safe operation.

## Conclusion

The OWL system provides a powerful, customizable solution for targeted weed control and area treatment in agricultural settings. By following this manual, you can effectively operate, adjust, and troubleshoot the OWL system to suit your specific needs.
