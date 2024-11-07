## Overview

Python application to automate the conversion of image and video files.

## Features

- **Command-Line Interface (CLI):** Allows users to specify input/output directories and target formats.
- **Automatic Directory Monitoring:** Watches a specific folder for new image or video files.
- **Extensible Architecture:** Easily add support for additional formats in the future.
- **Robust Logging:** Tracks conversion processes and errors.

## Supported Formats

### Image Formats

- **JPG/JPEG**
- **PNG**
- **BMP**
- **WEBP**
- **RAW**

### Video Formats

- **MP4**
- **AVI**
- **MKV**
- **MOV**
- **WebM**

## Technology Stack

- **Logging:** Python’s built-in `logging` module
- **Packaging:** [setuptools](https://setuptools.pypa.io/) for distribution
- **Configuration Management:** [PyYAML](https://pyyaml.org/)
- **Programming Language:** Python 3.x
- **Directory Monitoring:** [Watchdog](https://python-watchdog.readthedocs.io/)
- **Video Processing:** [FFmpeg](https://ffmpeg.org/)
- **Image Processing:** [Pillow](https://python-pillow.org/)
- **CLI Parsing:** [Argparse](https://docs.python.org/3/library/argparse.html)
- **Version Control:** Git

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your_username/image-video-converter.git
   cd image-video-converter
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. **Setup Folders**

Ensure that the `input` and `output` directories exist in the project's root directory.

### 2. **Run the Application**

It's essential to run the application first before adding files to the `input` folder to ensure real-time detection.

**Note:** Running the application without any command-line arguments will use the default settings specified in `config/config.yaml`.

### 3. **Add Files for Conversion**

With the application running, add your image or video files to the `input` directory. The application will automatically detect and convert them.
