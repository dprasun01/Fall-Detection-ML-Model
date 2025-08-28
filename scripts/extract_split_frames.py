import cv2
import os
from PIL import Image
import imagehash


def extract_and_split_frames(
    video_path, output_folder, interval=1, video_index=0, cam_number=0
):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load the video file
    video = cv2.VideoCapture(video_path)

    # Get the video's frames per second and calculate the frame interval
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_interval = fps * interval

    # Initialize frame counter and set for storing unique image hashes
    frame_count = 0
    seen_hashes = set()
    success, frame = video.read()

    while success:
        # Check if the current frame is at the specified interval
        if frame_count % frame_interval == 0:
            # Get frame dimensions and split to keep only the right half
            height, width = frame.shape[:2]
            midpoint = width // 2
            right_half = frame[:, midpoint:]

            # Convert the right half to PIL format for hashing
            pil_image = Image.fromarray(cv2.cvtColor(right_half, cv2.COLOR_BGR2RGB))

            # Compute perceptual hash and check for duplicates
            img_hash = imagehash.phash(pil_image)
            if img_hash not in seen_hashes:
                # Save unique frame
                seen_hashes.add(img_hash)
                frame_filename = os.path.join(
                    output_folder,
                    f"video{video_index}_cam{cam_number}_frame_{frame_count // frame_interval:04d}.jpg",
                )
                cv2.imwrite(frame_filename, right_half)
                print(f"Saved {frame_filename}")
            else:
                print(f"Duplicate frame at {frame_count}, skipping save.")

        # Read the next frame
        success, frame = video.read()
        frame_count += 1

    # Release the video capture object
    video.release()
    print(
        f"Frame extraction and saving right half complete for video {video_index} cam{cam_number}."
    )


if __name__ == "__main__":
    for i in range(1, 9):
        # Process frames for cam0
        vid_src = f"../fall/fall-0{i}-cam0.mp4"
        extract_and_split_frames(
            vid_src, "../frames/fall", interval=1, video_index=i, cam_number=0
        )

        # Process frames for cam1
        vid_src = f"../fall/fall-0{i}-cam1.mp4"
        extract_and_split_frames(
            vid_src, "../frames/fall", interval=1, video_index=i, cam_number=1
        )
