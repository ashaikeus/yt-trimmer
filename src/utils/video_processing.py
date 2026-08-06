import subprocess

from configs import logger


def trim_video(input_path: str, trim_start: int, trim_end: int) -> str:
    output_path = input_path.replace(".mp4", f"__trim_{trim_start}_{trim_end}.mp4")

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            input_path,
            "-ss",
            str(trim_start),
            "-to",
            str(trim_end),
            "-c",
            "copy",
            output_path,
        ],
        capture_output=True,
        text=True,
    )

    return output_path
