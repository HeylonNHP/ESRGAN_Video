import create_init
from pathlib import Path

import numpy as np
import cv2
import os
import sys
import ffmpeg

from tqdm import tqdm
from cv2 import VideoWriter

init_file_generator = create_init.create_init("esrgan")
init_file_generator.create_init_files()
sys.path.insert(0, os.getcwd() + os.path.sep + 'esrgan')
import esrgan.upscale
import esrgan.utils.dataops as ops


class esrgan_video_upscaler():
    model_scale_factor = 1
    model_name = ""

    def __init__(self, model_name, scale_factor):
        self.model_name = model_name
        self.model_scale_factor = scale_factor

    def upscale_video(self, video_path):
        upscaler = esrgan.upscale.Upscale(input=Path("input"), output=Path("output"), model=self.model_name,
                                          alpha_mode=esrgan.upscale.AlphaOptions.SWAPPING, fp16=True)
        upscaler.load_model(self.model_name)
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # video details
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # upscaled details
        upscaled_width = width * upscaler.last_scale
        upscaled_height = height * upscaler.last_scale
        rescale_factor = float(self.model_scale_factor / float(upscaler.last_scale))
        rescaled_width = int(rescale_factor * upscaled_width)
        rescaled_height = int(rescale_factor * upscaled_height)

        # loading bar
        progress_bar = tqdm(total=total_frames)

        depth: int = None

        # Set up the FFmpeg command with the desired output format and codec

        output_file = "output.mp4"
        input_args = {
            "format": "rawvideo",
            "s": f"{rescaled_width}x{rescaled_height}",
            "pixel_format": "rgb24",
            "r": str(fps),
        }
        output_args = {
            "vcodec": "libx264",
            "pix_fmt": "yuv420p",
            "preset": "veryslow",
            "format": "mp4",
            "crf": "20",
        }

        orig_input_video = ffmpeg.input(video_path)
        process = (ffmpeg.input("pipe:", **input_args)
                   .concat(orig_input_video.audio, v=1, a=1).output(output_file,
                                                                    **output_args).overwrite_output().run_async(
            pipe_stdin=True))

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame
            ret, frame = cap.read()

            # If the frame was read successfully
            if ret:
                # Prepare to split frame to save VRAM
                frame = cv2.copyMakeBorder(frame, 16, 16, 16, 16, cv2.BORDER_WRAP)
                # Parse the upscaling function upscaler.upscale, and the original frame to the auto splitter
                upscaled_frame, depth = ops.auto_split_upscale(
                    frame, upscaler.upscale, upscaler.last_scale, max_depth=depth
                )
                upscaled_frame = upscaler.crop_seamless(upscaled_frame, upscaler.last_scale)

                if rescale_factor != 1:
                    upscaled_frame = cv2.resize(upscaled_frame, (0, 0), fx=rescale_factor, fy=rescale_factor,
                                                interpolation=cv2.INTER_AREA)
                output_image = cv2.convertScaleAbs(upscaled_frame, alpha=1)

                # Convert to rgb24 and pipe to ffmpeg
                rgb24_output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
                byte_array = np.asarray(rgb24_output_image)
                process.stdin.write(byte_array)

                progress_bar.update(1)

            # If the frame was not read successfully, exit the loop
            else:
                break

        # Release the video file and destroy the window
        cap.release()
        cv2.destroyAllWindows()
        process.stdin.close()
        process.wait()


def main():
    video_input_path = sys.argv[3]
    model_name = fr"esrgan\models\{sys.argv[1]}"
    scale_factor = int(sys.argv[2])
    upscaler = esrgan_video_upscaler(model_name, scale_factor)
    upscaler.upscale_video(video_input_path)


main()
