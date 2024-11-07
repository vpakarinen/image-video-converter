import moviepy.editor as mp
from PIL import Image
import logging
import os

class Converter:
    def __init__(self, config):
        self.input_dir = config.get('input_dir')
        self.output_dir = config.get('output_dir')
        self.supported_image_formats = config.get_supported_image_formats()
        self.supported_video_formats = config.get_supported_video_formats()

    def is_image(self, file_path):
        ext = os.path.splitext(file_path)[1][1:].lower()
        return ext in self.supported_image_formats

    def is_video(self, file_path):
        ext = os.path.splitext(file_path)[1][1:].lower()
        return ext in self.supported_video_formats

    def convert_image(self, file_path, target_format):
        try:
            with Image.open(file_path) as img:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(self.output_dir, f"{base_name}.{target_format}")
                img.save(output_path, target_format.upper())
                logging.info(f"Converted Image: {file_path} -> {output_path}")
        except Exception as e:
            logging.error(f"Failed to convert image {file_path}: {e}")

    def convert_video(self, file_path, target_format):
        try:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join(self.output_dir, f"{base_name}.{target_format}")
            clip = mp.VideoFileClip(file_path)
            clip.write_videofile(output_path, codec='libx264')
            logging.info(f"Converted Video: {file_path} -> {output_path}")
        except Exception as e:
            logging.error(f"Failed to convert video {file_path}: {e}")

    def process_file(self, file_path, target_format):
        if self.is_image(file_path):
            self.convert_image(file_path, target_format)
        elif self.is_video(file_path):
            self.convert_video(file_path, target_format)
        else:
            logging.warning(f"Unsupported file format: {file_path}")