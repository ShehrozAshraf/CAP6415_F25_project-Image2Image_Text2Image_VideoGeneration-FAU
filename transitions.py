import subprocess
import json
import shutil
import os

# -------------------------------------------------------------------
# Locate FFmpeg and FFprobe on your system.
# shutil.which() returns the absolute path if "ffmpeg" or "ffprobe" is
# available in your PATH environment variable.
#
# If not found, we fall back to your manually installed Windows path.
# -------------------------------------------------------------------
FFMPEG = shutil.which("ffmpeg") or r"C:\Nano\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\Nano\ffmpeg-8.0.1-essentials_build\bin\ffprobe.exe"

# List of all scene video files that will be merged with crossfades.
videos = [
    "scene_1.mp4",
    "scene_2.mp4",
    "scene_3.mp4",
    "scene_4.mp4",
    "scene_5.mp4",
    "scene_6.mp4",
    "scene_7.mp4",
    "scene_8.mp4",
    "scene_9.mp4",
    "scene_10.mp4",
    "scene_11.mp4",
    "scene_12.mp4",
    "scene_13.mp4",
    "scene_14.mp4"
]

OUTPUT = "final_output_fixed.mp4"   # Name of final rendered video
FADE = 1                            # Fade duration in seconds


# -------------------------------------------------------------------
# get_duration(file)
# Uses ffprobe to extract the exact duration of each video file.
#
# Why do this?
#   - FFmpeg requires a correct timeline when chaining xfades.
#   - Your clips have mixed durations (4s, 8s), so transitions must
#     be placed precisely in time, otherwise the next scene will freeze.
#
# ffprobe outputs JSON → we parse it and return the duration as float.
# -------------------------------------------------------------------
def get_duration(file):
    result = subprocess.run([
        FFPROBE, "-v", "error",
        "-select_streams", "v:0",        # Select only the video stream
        "-show_entries", "format=duration",
        "-of", "json",                   # Output in JSON format
        file
    ], capture_output=True, text=True)

    # Extract duration value from JSON
    return float(json.loads(result.stdout)["format"]["duration"])


# -------------------------------------------------------------------
# merge(videos, output)
#
# The heart of the system.
#
# What this function does:
#   1. Gets duration of each clip using get_duration()
#   2. Builds FFmpeg input list
#   3. Constructs a dynamic filter_complex chain:
#         xfade for video
#         acrossfade for audio
#   4. COMPUTES THE CORRECT OFFSET FOR EVERY TRANSITION
#
# Why offset math matters:
#   - Each transition must occur at the end of the CURRENT RESULT,
#     not at cumulative video index timings.
#
# This completely prevents freeze/stutter issues.
# -------------------------------------------------------------------
def merge(videos, output):

    # Get durations for every input clip
    durations = [get_duration(v) for v in videos]

    # ---------------------------
    # Build FFmpeg input arguments
    # Example: -i scene_1.mp4 -i scene_2.mp4 ...
    # ---------------------------
    inputs = []
    for v in videos:
        inputs += ["-i", v]

    filters = []       # Will hold all xfade + acrossfade commands
    v_prev = "0:v"     # Start video fade chain with first clip
    a_prev = "0:a"     # Start audio fade chain with first clip

    # Initial output duration = duration of first clip
    # We use this to calculate the offset of the next transition.
    out_duration = durations[0]

    # -------------------------------------------------------------------
    # Loop through all clips starting from clip 2 (index 1)
    #
    # For each clip:
    #   offset = (duration of output so far) - fade
    #
    # Example:
    #   clip1: 8s
    #   clip2: 8s → offset = 8 - 1 = 7
    #   output now = 8 + 8 - 1 = 15
    #
    #   clip3: 4s → offset = 15 - 1 = 14
    #
    # NOTE: This offset is applied to the *current output timeline*,
    #       NOT the input file timeline.
    #
    # This is the correct FFmpeg logic for sequential xfades.
    # -------------------------------------------------------------------
    for i in range(1, len(videos)):

        # Place the transition exactly at the end of the output so far
        offset = out_duration - FADE

        # Names for next outputs
        v_out = f"v{i}"
        a_out = f"a{i}"

        # ---------------------------
        # Build video crossfade filter
        # ---------------------------
        filters.append(
            f"[{v_prev}][{i}:v] "
            f"xfade=transition=fade:duration={FADE}:offset={offset} "
            f"[{v_out}];"
        )

        # ---------------------------
        # Build audio crossfade filter
        # ---------------------------
        filters.append(
            f"[{a_prev}][{i}:a] "
            f"acrossfade=d={FADE} "
            f"[{a_out}];"
        )

        # Update running timeline:
        # out_duration = previous_output + next_clip - fade overlap
        out_duration = out_duration + durations[i] - FADE

        # Set new previous nodes for next iteration
        v_prev = v_out
        a_prev = a_out

    # Combine all filters into a single filter_complex string
    filter_complex = " ".join(filters)

    # ---------------------------
    # Build final FFmpeg command
    # ---------------------------
    cmd = [
        FFMPEG, "-y",                # Overwrite existing output file
        *inputs,                    # All video inputs
        "-filter_complex", filter_complex,   # Our xfade chain
        "-map", f"[{v_prev}]",      # Map final VIDEO output
        "-map", f"[{a_prev}]",      # Map final AUDIO output
        "-preset", "fast",          # Encoding speed preset
        "-c:v", "libx264",          # Encode video using H.264
        "-c:a", "aac",              # Encode audio using AAC
        output                      # Output file name
    ]

    print("Running:", " ".join(cmd))

    # Run the FFmpeg process
    subprocess.run(cmd, check=True)

    print("\n🎉 NO FREEZE VERSION COMPLETE:", output)


# -------------------------------------------------------------------
# Main entry point
# -------------------------------------------------------------------
if __name__ == "__main__":
    merge(videos, OUTPUT)
