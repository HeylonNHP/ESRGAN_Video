from pathlib import Path

import cv2
import os
import sys

sys.path.insert(0, os.getcwd() + os.path.sep + 'esrgan')
import esrgan.upscale


class esrgan_video_upscaler():
    model_scale_factor = 4
    model_name = r"esrgan\models\4x-UltraSharp-upscale-jpeg-images.pth"

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
        out = cv2.VideoWriter('output.mkv', fourcc, fps,
                              (width * self.model_scale_factor, height * self.model_scale_factor))

        # Loop through the video frames
        while cap.isOpened():

            # Read a frame
            ret, frame = cap.read()

            # If the frame was read successfully
            if ret:

                upscaled_frame = upscaler.upscale(frame)

                # Show the frame
                # cv2.imshow('Frame', frame)
                # cv2.imshow('Upscaled_frame', upscaled_frame)
                # cv2.imwrite("1.png", upscaled_frame)
                out.write(cv2.convertScaleAbs(upscaled_frame, alpha=(1)))

            # If the frame was not read successfully, exit the loop
            else:
                break

        # Release the video file and destroy the window
        cap.release()
        out.release()
        cv2.destroyAllWindows()


def main():
    video_input_path = sys.argv[1]
    upscaler = esrgan_video_upscaler()
    upscaler.upscale_video(video_input_path)


main()
