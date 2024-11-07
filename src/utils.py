def is_supported_file(file_path, supported_formats):
    ext = file_path.split('.')[-1].lower()
    return ext in supported_formats