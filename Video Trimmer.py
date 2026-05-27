"""
video_trimmer.py
----------------
Trim video segments at given time intervals and join them.

Requirements:
    pip install moviepy

Usage:
    Edit the SEGMENTS list below with your desired cut points,
    set INPUT_FILE to your video path, then run:
        python video_trimmer.py
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os


# ─────────────────────────────────────────────
# CONFIGURATION — edit these values
# ─────────────────────────────────────────────

INPUT_FILE = "C:\\Downloads\\Bob-a-Thon_Uncertainty_Refund_V1.0.mp4"          # ← your input video file path

OUTPUT_FILE = "C:\\Downloads\\Bob-a-Thon_Uncertainty_Refund_V1.0_trimmed.mp4"      # ← output joined video file path

# Define segments as (start, end) in seconds
# Helper: 1 min 25 sec = 85.0 seconds
#         1 min 35 sec = 95.0 seconds
#         3 min 56 sec = 236.0 seconds
#         4 min 45 sec = 285.0 seconds

SEGMENTS = [
    (2.08,  95.0),   # Segment 1: 1:25 → 1:35
    (236.0, 285.0),  # Segment 2: 3:56 → 4:45
]


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def mmss_to_seconds(time_str: str) -> float:
    """
    Convert 'MM:SS' or 'MM:SS.ff' string to float seconds.
    Examples:
        '1:25'   → 85.0
        '3:56'   → 236.0
        '1:25.5' → 85.5
    """
    parts = time_str.strip().split(":")
    minutes = int(parts[0])
    seconds = float(parts[1])
    return minutes * 60 + seconds


def seconds_to_mmss(seconds: float) -> str:
    """Convert float seconds back to MM:SS string for display."""
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m}:{s:05.2f}"


def trim_and_join(input_path: str, segments: list, output_path: str):
    """
    Trim multiple segments from a video and join them into one output file.

    Args:
        input_path : path to source video
        segments   : list of (start_sec, end_sec) tuples
        output_path: path to write final joined video
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print(f"\n📂 Loading video: {input_path}")
    source = VideoFileClip(input_path)
    print(f"   Duration : {seconds_to_mmss(source.duration)} ({source.duration:.2f}s)")
    print(f"   FPS      : {source.fps}")
    print(f"   Size     : {source.size[0]}x{source.size[1]}")

    clips = []
    for i, (start, end) in enumerate(segments, 1):
        # Clamp to video duration
        start = max(0, min(start, source.duration))
        end   = max(0, min(end,   source.duration))

        if start >= end:
            print(f"\n⚠️  Segment {i} skipped: start ({seconds_to_mmss(start)}) >= end ({seconds_to_mmss(end)})")
            continue

        print(f"\n✂️  Segment {i}: {seconds_to_mmss(start)} → {seconds_to_mmss(end)}  ({end-start:.2f}s)")
        clip = source.subclip(start, end)
        clips.append(clip)

    if not clips:
        print("\n❌ No valid segments found. Exiting.")
        source.close()
        return

    print(f"\n🔗 Joining {len(clips)} segment(s)...")
    final = concatenate_videoclips(clips, method="compose")

    print(f"📝 Writing output: {output_path}")
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp_audio.m4a",
        remove_temp=True,
        logger="bar"
    )

    # Cleanup
    final.close()
    source.close()
    for c in clips:
        c.close()

    print(f"\n✅ Done! Output saved to: {output_path}")
    print(f"   Total duration: {seconds_to_mmss(final.duration)}")


# ─────────────────────────────────────────────
# INTERACTIVE MODE — enter times as MM:SS
# ─────────────────────────────────────────────

def interactive_mode():
    """Prompt user to enter segments interactively as MM:SS strings."""
    print("\n🎬 Video Trimmer — Interactive Mode")
    print("─" * 40)

    input_file = input("Enter input video file path: ").strip().strip('"')
    output_file = input("Enter output file name [output_trimmed.mp4]: ").strip() or "output_trimmed.mp4"

    segments = []
    print("\nEnter segments (MM:SS format, e.g. 1:25). Type 'done' when finished.")

    while True:
        seg_num = len(segments) + 1
        start_str = input(f"\nSegment {seg_num} — Start time (MM:SS) or 'done': ").strip()
        if start_str.lower() == "done":
            break
        end_str = input(f"Segment {seg_num} — End   time (MM:SS): ").strip()

        try:
            start_sec = mmss_to_seconds(start_str)
            end_sec   = mmss_to_seconds(end_str)
            segments.append((start_sec, end_sec))
            print(f"   → Added: {start_sec:.2f}s to {end_sec:.2f}s")
        except Exception as e:
            print(f"   ⚠️  Invalid time format: {e}. Try again.")

    if not segments:
        print("No segments entered. Exiting.")
        return

    trim_and_join(input_file, segments, output_file)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Run interactive prompt mode
        interactive_mode()
    else:
        # Run with hardcoded config at top of file
        trim_and_join(INPUT_FILE, SEGMENTS, OUTPUT_FILE)