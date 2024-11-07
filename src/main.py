from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from converter import Converter
from config import Config
import argparse
import logging
import time

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, converter, target_image_format, target_video_format):
        super().__init__()
        self.converter = converter
        self.target_image_format = target_image_format
        self.target_video_format = target_video_format

    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        logging.info(f"Detected new file: {file_path}")
        if self.converter.is_image(file_path):
            self.converter.convert_image(file_path, self.target_image_format)
        elif self.converter.is_video(file_path):
            self.converter.convert_video(file_path, self.target_video_format)
        else:
            logging.warning(f"Unsupported file format: {file_path}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Image and Video Conversion Automation')
    parser.add_argument('--input_dir', type=str, help='Path to the input directory')
    parser.add_argument('--output_dir', type=str, help='Path to the output directory')
    parser.add_argument('--image_format', type=str, help='Target image format (e.g., png, jpg)')
    parser.add_argument('--video_format', type=str, help='Target video format (e.g., mp4, avi)')
    parser.add_argument('--log_level', type=str, help='Logging level (e.g., DEBUG, INFO)')
    return parser.parse_args()

def setup_logging(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    args = parse_arguments()
    config = Config()

    # Override config with CLI arguments if provided
    input_dir = args.input_dir if args.input_dir else config.get('input_dir')
    output_dir = args.output_dir if args.output_dir else config.get('output_dir')
    image_format = args.image_format if args.image_format else config.get('default_image_format')
    video_format = args.video_format if args.video_format else config.get('default_video_format')
    log_level = args.log_level if args.log_level else config.get('log_level')

    setup_logging(log_level)
    logging.info('Starting Image and Video Conversion Automation')
    logging.info(f'Input Directory: {input_dir}')
    logging.info(f'Output Directory: {output_dir}')
    logging.info(f'Default Image Format: {image_format}')
    logging.info(f'Default Video Format: {video_format}')

    # Retrieve supported formats
    supported_image_formats = config.get_supported_image_formats()
    supported_video_formats = config.get_supported_video_formats()

    logging.info(f'Supported Image Formats: {", ".join(supported_image_formats)}')
    logging.info(f'Supported Video Formats: {", ".join(supported_video_formats)}')

    # Initialize Converter
    converter = Converter(config)

    # Set up event handler and observer
    event_handler = FileEventHandler(converter, image_format, video_format)
    observer = Observer()
    observer.schedule(event_handler, path=input_dir, recursive=False)
    observer.start()
    logging.info(f"Monitoring '{input_dir}' for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopping directory monitoring.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        observer.stop()
    
    observer.join()

if __name__ == '__main__':
    main() 