import sys
import os
from main import *


def change_file_extension(path):
    directory, filename = os.path.split(path)
    filename_without_extension, extension = os.path.splitext(filename)
    new_filename = f"{filename_without_extension}.mkv"
    new_path = os.path.join(directory, new_filename)
    return new_path


def process_single_input(video_input_path: str, model_name: str, scale_factor: int):
    upscaler = esrgan_video_upscaler(model_name, scale_factor)
    upscaler.upscale_video(video_input_path, change_file_extension(video_input_path))


def search_videos(folder_path, whitelisted_extensions: tuple = ('.mp4', '.webm', '.mov', '.gif'), recursive=False):
    videos = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            for extension in whitelisted_extensions:
                if file.endswith(extension):
                    videos.append(os.path.join(root, file))
        if not recursive:
            break
    return videos


def process_directory_input(video_input_path: str, model_name: str, scale_factor: int,
                            whitelisted_extensions: tuple = None):
    if whitelisted_extensions is not None:
        videos_list = search_videos(video_input_path, whitelisted_extensions)
    else:
        videos_list = search_videos(video_input_path)

    upscaler = esrgan_video_upscaler(model_name, scale_factor)

    for video in videos_list:
        upscaler.upscale_video(video, change_file_extension(video))


def main():
    video_input_path = sys.argv[3]
    model_name = fr"esrgan\models\{sys.argv[1]}"
    scale_factor = int(sys.argv[2])

    if os.path.isfile(video_input_path):
        process_single_input(video_input_path, model_name, scale_factor)
    elif os.path.isdir(video_input_path):
        if len(sys.argv) == 5:
            process_directory_input(video_input_path, model_name, scale_factor, tuple(sys.argv[4].split(",")))
        else:
            process_directory_input(video_input_path, model_name, scale_factor)


main()
