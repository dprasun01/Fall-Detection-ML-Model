import cv2
import os


def crop_video_right_half(input_path, output_path):
    """
    Crop the right-side half of the video frames and save as a new video.
    """

    # Open the video
    cap = cv2.VideoCapture(input_path)

    # Check if the video is opened successfully
    if not cap.isOpened():
        print(f"Error: Cannot open video {input_path}")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for the output video

    # Define the output video writer
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width // 2, frame_height))

    print(f"Processing video: {input_path}")
    print(f"Original Dimensions: {frame_width}x{frame_height}, FPS: {fps}")
    print(f"Saving cropped video to: {output_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Crop the right-side half
        right_half = frame[:, frame_width // 2 :]

        # Write the frame to the output video
        out.write(right_half)

    # Release resources
    cap.release()
    out.release()
    print("Processing complete.")


if __name__ == "__main__":

    input_folder = "../videos_uncropped/no_fall/"
    output_folder = "../videos_cropped/no_fall/"

    for idx in range(1, 41):

        if len(str(idx)) == 1:
            input_video = input_folder + "adl-0" + str(idx) + "-cam0.mp4"
            output_video = output_folder + "adl-0" + str(idx) + "-cam0.mp4"
        else:
            input_video = input_folder + "adl-" + str(idx) + "-cam0.mp4"
            output_video = output_folder + "adl-" + str(idx) + "-cam0.mp4"

        crop_video_right_half(input_video, output_video)
