import argparse
import logging
from logging.handlers import RotatingFileHandler
import time
from config import Config
from converter import Converter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, converter, target_image_format, target_video_format):
        super().__init__()
        self.converter = converter
        self.target_image_format = target_image_format
        self.target_video_format = target_video_format

    def on_created(self, event):
        if event.is_directory:
            logging.info(f"Ignored directory creation: {event.src_path}")
            return
        file_path = event.src_path

        # Ignore hidden files
        if os.path.basename(file_path).startswith('.'):
            logging.info(f"Ignored hidden file: {file_path}")
            return

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

def setup_logging(log_level, log_file='logs/app.log'):
    os.makedirs('logs', exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Rotating File Handler
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

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

    # Verify that input and output directories exist
    if not os.path.isdir(input_dir):
        logging.error(f"Input directory does not exist: {input_dir}")
        return
    if not os.path.isdir(output_dir):
        logging.error(f"Output directory does not exist: {output_dir}")
        return

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