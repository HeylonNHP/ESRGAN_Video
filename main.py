from pathlib import Path

import cv2
import os
import sys

from cv2 import VideoWriter

sys.path.insert(0, os.getcwd() + os.path.sep + 'esrgan')
import esrgan.upscale


class esrgan_video_upscaler():
    model_scale_factor = 1
    model_name = ""

    def __init__(self, model_name, scale_factor):
        self.model_name = model_name
        self.model_scale_factor = scale_factor

    def upscale_video(self, video_path):
        upscaler = esrgan.upscale.Upscale(input=Path("input"), output=Path("output"), model=self.model_name,
                                          alpha_mode=esrgan.upscale.AlphaOptions.SWAPPING)
        upscaler.load_model(self.model_name)
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Open the output video file
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')
        out: VideoWriter = None
        calculated_scaling_factor: int

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame
            ret, frame = cap.read()

            # If the frame was read successfully
            if ret:
                upscaled_frame = upscaler.upscale(frame)

                if out is None:
                    # Initialise output once the output resolution is known
                    upscaled_frame_height, upscaled_frame_width = upscaled_frame.shape[:2]
                    calculated_scaling_factor = ((upscaled_frame_height / height) + (
                            upscaled_frame_width / width)) / 2.0
                    out = cv2.VideoWriter('output.mkv', fourcc, fps,
                                          (int(width * self.model_scale_factor),
                                           int(height * self.model_scale_factor)))

                if self.model_scale_factor < calculated_scaling_factor:
                    scale = float(self.model_scale_factor) / float(calculated_scaling_factor)
                    upscaled_frame = cv2.resize(upscaled_frame, (0, 0), fx=scale, fy=scale,
                                                interpolation=cv2.INTER_AREA)
                out.write(cv2.convertScaleAbs(upscaled_frame, alpha=(1)))

            # If the frame was not read successfully, exit the loop
            else:
                break

        # Release the video file and destroy the window
        cap.release()
        out.release()
        cv2.destroyAllWindows()


def main():
    video_input_path = sys.argv[3]
    model_name = fr"esrgan\models\{sys.argv[1]}"
    scale_factor = int(sys.argv[2])
    upscaler = esrgan_video_upscaler(model_name, scale_factor)
    upscaler.upscale_video(video_input_path)


main()
