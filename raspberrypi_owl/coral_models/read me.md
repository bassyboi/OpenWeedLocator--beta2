README
Adding Green-on-Green to the OWL (Experimental)

Welcome to the experimental first iteration of Green-on-Green, an in-crop weed detection algorithm integrated with the OWL (OpenWeedLocator) system. This version is highly experimental and has not been tested yet, so it may require significant troubleshooting and adjustments. While designed to work on a Raspberry Pi 4, LibreComputer, and a Windows desktop computer, there may be potential compatibility issues, especially when using Python 3.11 with pycoral. Proceed with caution and be prepared for potential instability.
Stage 1 | Hardware/Software - Google Coral Installation

To get started with Green-on-Green detection using the Google Coral USB Accelerator on the Raspberry Pi, you must install additional supporting software. This includes the pycoral library and tflite-runtime for Python 3.11. These steps are still in a testing phase and have not been extensively validated, so proceed with caution.
Step 1: Set Up the Installation Environment

Assuming you have already cloned the OpenWeedLocator repository and are working in the OpenWeedLocator/coral_models directory on your Raspberry Pi, navigate to this directory using:

bash

owl@raspberrypi:~ $ cd ~/OpenWeedLocator/coral_models

Step 2: Run the Installation Script

Run the installation file install_coral.sh to install the necessary libraries and dependencies for the Google Coral USB Accelerator. This script will install the non-official pycoral build from a GitHub release, which works with Python 3.11, and the TensorFlow Lite runtime (tflite-runtime==2.14.0). For more details on the installation process, you can also refer to the official Google Coral documentation.

During the installation, you will be prompted to confirm performance options and connect the Google Coral USB device to a USB 3.0 port (blue).

Execute the installation script with the following commands:

bash

owl@raspberrypi:~ $ chmod +x install_coral.sh && ./install_coral.sh

Important Note:

This installation uses a workaround to install pycoral with Python 3.11. This approach is untested and only for development purposes. If you encounter any errors during the pycoral library installation, you may need to manually activate the owl environment and retry the installation:

bash

owl@raspberrypi:~ $ workon owl
(owl) owl@raspberrypi:~/OpenWeedLocator/coral_models$ pip install pycoral-2.13.0-cp311-cp311-linux_aarch64.whl --no-deps

Step 3: Verify the Installation

To test the installation, open a Python terminal and try importing the pycoral library:

bash

(owl) owl@raspberrypi:~/OpenWeedLocator/coral_models$ python
>>> import pycoral

If the import is successful without any errors, then the installation was successful, and you are ready to proceed with running object detection models on the OWL.
Stage 2 | Model Training/Deployment - Inference with the Coral

Running weed detection models on the Google Coral requires generating a .tflite model file that is optimized for the Coral TPU. These models are lightweight and efficient, making them suitable for edge device deployments. It is crucial to use models specifically optimized for the Coral, as generic .tflite files may result in slower performance or failure to run.
Step 1: Test the Installation with a Generic Model

To confirm that the Coral installation is working correctly, it is recommended to download a generic model from the Coral model repository. This step isolates any issues related to the OWL or Coral installation.

Run the following command to download a test model while in the OpenWeedLocator/coral_models directory:

bash

(owl) owl@raspberrypi:~/OpenWeedLocator/coral_models$ wget https://raw.githubusercontent.com/google-coral/test_data/master/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite

Then navigate back to the OpenWeedLocator directory and run owl.py with the gog (Green-on-Green) algorithm specified. If you do not specify a path to the .tflite model, it will automatically select the first model in the directory sorted alphabetically.

If testing indoors, you may need to adjust the camera settings, as the default settings may be too dark. Use the --exp-compensation 4 and --exp-mode auto options if necessary:

bash

(owl) owl@raspberrypi:~/OpenWeedLocator/coral_models$ cd ..
(owl) owl@raspberrypi:~/OpenWeedLocator$ python owl.py --show-display --algorithm gog --exp-compensation 4 --exp-mode auto

If the setup runs correctly, you should see a video feed similar to the Green-on-Brown approach, with red boxes around detected objects. This specific test detects 'potted plants' (COCO category ID 63). You can change the filter_id to detect different COCO categories; see the full list of categories here.
Model Training Options

Once you have confirmed that the installation works, you can begin training and deploying your weed recognition models. There are two main methods to generate optimized .tflite files for the Coral:
Option 1: Train a Model Using TensorFlow

EdjeElectronics provides an excellent step-by-step guide to creating a .tflite model file optimized for the Edge TPU:

    Google Colab walkthrough
    Accompanying YouTube video

Additionally, the official Google Colab tutorial from Coral guides you through the process of training custom datasets.
Option 2: Train a YOLO v5/v8 Model and Export as .tflite

Note: This method is currently not working consistently. Once this issue is resolved, it will be the preferred approach due to the ease of training YOLO models and their relatively high performance. You can track the issue on the Ultralytics repository here.

To train a YOLOv5 model with Weed-AI datasets, refer to this Weed-AI Colab notebook. After training, export the model for the Edge TPU:
YOLOv5 Export Command:

bash

!python export.py --weights path/to/your/weights/best.pt --include edgetpu

YOLOv8 Export Command:

bash

!yolo export model=path/to/your/weights/best.pt format=edgetpu

The GreenOnGreen class in OWL will load the first model alphabetically in the directory if specified with algorithm='gog' or the model specified with algorithm=path/to/model.tflite. Ensure that all your classes are listed in the labels.txt file.
Conclusion

This guide covers the initial setup for integrating Green-on-Green detection with OWL using the Google Coral USB Accelerator. Given that this is a very early version, changes and improvements are expected.
References

    PyImageSearch
    Google Coral Guides
