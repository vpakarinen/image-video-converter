import moviepy.editor as mp
from PIL import Image
import logging
import time
import os

class Converter:
    def __init__(self, config):
        self.input_dir = os.path.abspath(config.get('input_dir'))
        self.output_dir = os.path.abspath(config.get('output_dir'))
        self.supported_image_formats = config.get_supported_image_formats()
        self.supported_video_formats = config.get_supported_video_formats()

    def is_image(self, file_path):
        ext = os.path.splitext(file_path)[1][1:].lower()
        return ext in self.supported_image_formats

    def is_video(self, file_path):
        ext = os.path.splitext(file_path)[1][1:].lower()
        return ext in self.supported_video_formats

    def get_pillow_format(self, format_str):
        format_map = {
            'jpg': 'JPEG',
            'jpeg': 'JPEG',
            'png': 'PNG',
            'bmp': 'BMP',
            'webp': 'WEBP'
        }
        return format_map.get(format_str.lower(), format_str.upper())

    def convert_image(self, file_path, target_format):
        # Wait a brief moment to ensure the file is fully written
        time.sleep(0.1)
        
        try:
            # Convert to absolute path
            abs_file_path = os.path.abspath(file_path)
            
            if not os.path.isfile(abs_file_path):
                logging.error(f"File does not exist: {abs_file_path}")
                return

            # Try to open the file first to verify access
            try:
                with open(abs_file_path, 'rb') as test_file:
                    pass
            except PermissionError:
                logging.error(f"Permission denied accessing file: {abs_file_path}")
                return

            with Image.open(abs_file_path) as img:
                base_name = os.path.splitext(os.path.basename(abs_file_path))[0]
                output_path = os.path.join(self.output_dir, f"{base_name}.{target_format}")
                
                # Get the correct Pillow format
                pillow_format = self.get_pillow_format(target_format)
                
                # Convert image
                if img.mode in ('RGBA', 'LA') and pillow_format == 'JPEG':
                    # Convert RGBA to RGB for JPEG
                    img = img.convert('RGB')
                
                img.save(output_path, pillow_format)
                logging.info(f"Converted Image: {abs_file_path} -> {output_path}")
        except Exception as e:
            logging.error(f"Failed to convert image {file_path}: {e}")

    def convert_video(self, file_path, target_format):
        try:
            abs_file_path = os.path.abspath(file_path)
            
            if not os.path.isfile(abs_file_path):
                logging.error(f"File does not exist: {abs_file_path}")
                return

            base_name = os.path.splitext(os.path.basename(abs_file_path))[0]
            output_path = os.path.join(self.output_dir, f"{base_name}.{target_format}")
            clip = mp.VideoFileClip(abs_file_path)
            clip.write_videofile(output_path, codec='libx264')
            logging.info(f"Converted Video: {abs_file_path} -> {output_path}")
        except Exception as e:
            logging.error(f"Failed to convert video {file_path}: {e}")

    def process_file(self, file_path, target_format):
        if self.is_image(file_path):
            self.convert_image(file_path, target_format)
        elif self.is_video(file_path):
            self.convert_video(file_path, target_format)
        else:
            logging.warning(f"Unsupported file format: {file_path}")