import sys

from main import *


def change_file_extension(path):
    directory, filename = os.path.split(path)
    filename_without_extension, extension = os.path.splitext(filename)
    new_filename = f"{filename_without_extension}.mkv"
    new_path = os.path.join(directory, new_filename)
    return new_path


def main():
    video_input_path = sys.argv[3]
    model_name = fr"esrgan\models\{sys.argv[1]}"
    scale_factor = int(sys.argv[2])
    upscaler = esrgan_video_upscaler(model_name, scale_factor)
    upscaler.upscale_video(video_input_path, change_file_extension(video_input_path))


main()
