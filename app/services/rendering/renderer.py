from pathlib import Path
import subprocess
import uuid


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def render_side_by_side(
    clip1_path: Path,
    clip2_path: Path
) -> Path:

    output_filename = f"{uuid.uuid4()}.mp4"
    output_path = OUTPUT_DIR / output_filename

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i", str(clip1_path),
        "-i", str(clip2_path),
        "-filter_complex",
        (
            "[0:v]scale=960:540[left];"
            "[1:v]scale=960:540[right];"
            "[left][right]hstack=inputs=2[v]"
        ),
        "-map", "[v]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        str(output_path)
    ]

    subprocess.run(
        ffmpeg_command,
        check=True
    )

    return output_path