"""
Video modules for Fomo
"""
from typing import Tuple, Union
import subprocess
import cv2
import numpy as np
from pydub import AudioSegment


def mp3_to_mp4_converter(
    config, mp3_path, mp4_path, temp_video_path, show_info, radio_name
) -> Tuple[bool, Union[str, None]]:
    """
    Helper function to generate video based on the audio.
    Used audio's to generate the waveform
    :param config: Configuration of the video
    :param mp3_path: Path of the audio file
    :param mp4_path: Path of the video file
    :param temp_video_path: Path of the temporary video file
    :param show_info: Details of the show
    :param radio_name: Name of the radio
    :return: Bool to check if the video file is generated along with the errors
    """
    try:
        # Load audio
        audio = AudioSegment.from_file(mp3_path)
        samples = np.array(audio.get_array_of_samples())
        samples = samples / np.max(np.abs(samples))

        # Video properties
        video_size = config.get("resolution")
        fps = config.get("fps")
        duration = len(samples) / audio.frame_rate
        frame_count = int(duration * fps)

        # Create video writer
        out = cv2.VideoWriter(
            temp_video_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, video_size
        )
        for i in range(frame_count):
            # Create a blank black frame
            frame = np.zeros((video_size[1], video_size[0], 3), dtype=np.uint8)

            # Add text
            top_text = radio_name
            top_font = cv2.FONT_HERSHEY_DUPLEX
            top_font_scale = 1.5
            top_color = config.get("title_color")
            top_thickness = 3
            top_text_size = cv2.getTextSize(
                top_text, top_font, top_font_scale, top_thickness
            )[0]
            top_text_x = (video_size[0] - top_text_size[0]) // 2
            top_text_y = 100
            cv2.putText(
                frame,
                top_text,
                (top_text_x, top_text_y),
                top_font,
                top_font_scale,
                top_color,
                top_thickness,
                lineType=cv2.LINE_AA,
            )

            # Add show text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.8
            color = config.get("subtitle_color")
            thickness = 2
            text_size = cv2.getTextSize(show_info, font, font_scale, thickness)[0]
            text_x = (video_size[0] - text_size[0]) // 2
            text_y = 150
            cv2.putText(
                frame,
                show_info,
                (text_x, text_y),
                font,
                font_scale,
                color,
                thickness,
                lineType=cv2.LINE_AA,
            )

            # Generate waveform
            start = int(i * len(samples) / frame_count)
            end = start + int(len(samples) / frame_count)
            wave = samples[start:end]
            center = video_size[1] // 2

            # Draw waveform on the frame
            for x_axis, sample in enumerate(wave[: video_size[0]]):
                y_axis = int(center + sample * 200)
                cv2.line(frame, (x_axis, center), (x_axis, y_axis), config.get("waveform_color"), 2)
            out.write(frame)
        out.release()

        # Merge audio with the video using ffmpeg
        ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-i",
            temp_video_path,
            "-i",
            mp3_path,
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "28",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            mp4_path,
        ]
        subprocess.run(ffmpeg_command, check=True)
        return True, None
    except Exception as exception:
        return False, str(exception)
