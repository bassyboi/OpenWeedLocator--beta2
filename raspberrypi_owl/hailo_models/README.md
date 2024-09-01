# Hailo Models for Raspberry Pi AI Kit

## Overview

This directory contains models optimized for the Hailo AI acceleration module, specifically designed for use with the Raspberry Pi 5. The Hailo-8L AI module provides 13 tera-operations per second (TOPS) for AI inference tasks, enabling high-performance deep learning applications at the edge. This README provides detailed instructions on setting up the Hailo environment, optimizing models, and running inference on the Hailo hardware.

## Hailo AI Acceleration Module

The Hailo-8L M.2 AI Module is an AI accelerator compatible with the Raspberry Pi 5 through the M.2 HAT+ interface. It supports the M, B+M, and A+E keys of the M.2 form factor and leverages PCIe Gen 3.0 for high-speed data transfer. The module is ideal for edge AI applications such as object detection, classification, and segmentation.

### Key Features of Hailo-8L AI Module

- **13 TOPS Neural Processing Unit (NPU)**: Delivers high performance for AI tasks.
- **Compatibility**: Supports both x86 and ARM architectures.
- **Runtime Software**: Includes HailoRT, a scalable runtime with C/C++ and Python APIs, supporting GStreamer and ONNX runtime for integration with AI pipelines.

## Prerequisites

1. **Raspberry Pi 5**: Ensure it runs the latest Raspberry Pi OS with all updates installed.
2. **Hailo SDK**: Install the Hailo SDK for accessing the development tools and runtime required to run and optimize AI models on the Hailo module.
3. **Dependencies**: Python 3.x, Hailo Model Zoo, GStreamer (if needed).

## Setting Up the Hailo SDK

1. **Install Hailo SDK**: The SDK provides tools such as HailoRT, a runtime environment for deploying AI models. To get started, download and install the Hailo SDK from the [Hailo Developer Zone](https://developer.hailo.ai).

2. **Configure the Environment**: Set up environment variables and install required packages using the following commands:
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install hailo-sdk