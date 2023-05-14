import cv2
import os
import sys

sys.path.insert(0, os.getcwd() + os.path.sep + 'esrgan')
import esrgan.upscale


class esrgan_video_upscaler():

    def upscale_video(self):
        upscaler = esrgan.upscale.Upscale()
        # Open the video file
        cap = cv2.VideoCapture(r'N:\video\cat-cats.gif')

        # Set the frame counter to 0
        frame_count = 0

        # Loop through the video frames
        while cap.isOpened():

            # Read a frame
            ret, frame = cap.read()

            # If the frame was read successfully
            if ret:

                # Show the frame
                cv2.imshow('Frame', frame)

                # Increment the frame counter
                frame_count += 1

                # If we have shown 5 frames, exit the loop
                if frame_count == 5:
                    break

            # If the frame was not read successfully, exit the loop
            else:
                break

        # Release the video file and destroy the window
        cap.release()
        cv2.destroyAllWindows()


def main():
    upscaler = esrgan_video_upscaler()
    upscaler.upscale_video()


main()
