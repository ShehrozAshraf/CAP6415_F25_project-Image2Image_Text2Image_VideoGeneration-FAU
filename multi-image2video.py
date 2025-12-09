import time
import base64
import subprocess
from google import genai
from google.genai import types
import os

# ----------------------------------------------------------
#  INITIALIZE GOOGLE GEMINI CLIENT
# ----------------------------------------------------------
client = genai.Client(api_key="AIzaSyB3Cet7JEKPf--O7Mcw6QRUB2hHvyaKFp8")

# ----------------------------------------------------------
#  LIST OF SCENES
# ----------------------------------------------------------
scenes = [
    {
        "image": r"Data\images\logo_text\24collegeofengineeringandcomputersciencelogo.png",
        "prompt": (
            "It is the logo of our university "
            "Soft ambient background music plays. "
            "Voice-over only narration (no people appear): 'Welcome to Florida Atlantic University Engineering.' "
            "Light wind SFX in the background."
        ),
        "duration": 4
    },
    {
        "image": r"Data/images/building_exterior/FAU_EE_Building_1.jpg",
        "prompt": (
            "Slow forward push-in toward the modern glass façade reflecting the blue sky. "
            "Camera motion is smooth and steady, like a cinematic gimbal. "
            "Subtle ambient music continues. "
            "Voice-over only narration (no people appear): 'A hub of innovation, research, and real-world engineering excellence.'"
        ),
        "duration": 4
    },
    {
        "image": r"Data/images/building_exterior/FAU_EE_Building_3.jpg",
        "prompt": (
            "Low-angle shot revealing sunlight rays behind the building. "
            "Camera slowly tilts upward for a dramatic reveal. "
            "Voice-over only narration (no people appear): 'Here, ideas become reality.' "
            "Gentle atmospheric sound effects."
        ),
        "duration": 4
    }
]

# ----------------------------------------------------------
#  LOAD IMAGE
# ----------------------------------------------------------
def load_image(path):
    with open(path, "rb") as f:
        return types.Image(
            image_bytes=f.read(),
            mime_type="image/jpeg"
        )


# ----------------------------------------------------------
#  GENERATE SCENE VIDEO (UPDATED WITH SEQUENTIAL NAMING)
# ----------------------------------------------------------
def generate_scene_video(image_path, prompt, duration, index):

    print(f"\n🎬 Processing Scene {index}:")
    print(f"   Image  : {image_path}")
    print(f"   Prompt : {prompt}")
    print(f"   Duration: {duration}s\n")

    img = load_image(image_path)

    # EXTRA PROTECTION AGAINST PEOPLE APPEARING
    full_prompt = prompt + " (NO PEOPLE should appear. Voice-over only narration.)"

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=full_prompt,
        image=img,
        config=types.GenerateVideosConfig(
            duration_seconds=duration,
            resolution="720p",
        )
    )

    while not operation.done:
        print("⏳ Veo is generating the video... waiting 10 seconds...")
        time.sleep(10)
        operation = client.operations.get(operation)

    # safety check
    if operation.response is None or not hasattr(operation.response, "generated_videos"):
        print("\n❌ ERROR: Veo failed to generate this scene.")
        return None

    video_obj = operation.response.generated_videos[0]

    # FORCE CLEAN SEQUENTIAL FILENAME
    safe_name = f"scene_{index}.mp4"

    # Download handling
    download_result = client.files.download(file=video_obj.video)

    if isinstance(download_result, (bytes, bytearray)):
        with open(safe_name, "wb") as f:
            f.write(download_result)

    elif isinstance(download_result, str):
        os.rename(download_result, safe_name)

    print(f"✅ Scene {index} saved as: {safe_name}")
    return safe_name


# ----------------------------------------------------------
#  MAIN EXECUTION  — NO MERGING, JUST SAVING INDIVIDUAL SCENES
# ----------------------------------------------------------
if __name__ == "__main__":
    generated_clips = []

    for idx, scene in enumerate(scenes, start=1):
        clip_file = generate_scene_video(
            image_path=scene["image"],
            prompt=scene["prompt"],
            duration=scene.get("duration", 8),
            index=idx
        )

        if clip_file is not None:
            generated_clips.append(clip_file)

    print("\n🎉 All scenes generated:")
    for c in generated_clips:
        print(" -", c)

    print("\nYou can now run your transition script on:")
    print(generated_clips)
