import time
import subprocess
import mimetypes
from google import genai
from google.genai import types
import os

# ----------------------------------------------------------
#  INITIALIZE GOOGLE GEMINI CLIENT
# ----------------------------------------------------------
client = genai.Client(api_key="AIzaSyB3Cet7JEKPf--O7Mcw6QRUB2hHvyaKFp8")


# ----------------------------------------------------------
#  SCENE DEFINITIONS (14 scenes)
#  → Correct image paths
#  → Correct file extensions
#  → Clean narration prompts
# ----------------------------------------------------------
scenes = [

    # Scene 1 — Building Exterior
    {
        "image": r"Data/images/building_exterior/FAU_EE_Building_2.jpg",
        "prompt": (
            "Cinematic shot of the FAU Engineering building at sunrise, warm light, palm trees, "
            "modern architecture. Use THIS image as the visual basis. "
            "Voice-over narration only: 'At Florida Atlantic University… innovation begins the moment you step on campus.'"
        ),
        "duration": 8
    },

    # Scene 2 — Lab Interior 1
    {
        "image": r"Data/images/lab_interior/Lab_Student_1.jpg",
        "prompt": (
            "Inside FAU engineering labs, students working collaboratively. Use this uploaded image as reference."
            "Soft, futuristic lighting. Voice-over narration only: 'Inside our engineering labs, ideas turn into discovery…'"
        ),
        "duration": 8
    },

    # Scene 3 — Lab Interior 2
    {
        "image": r"Data/images/lab_interior/Lab_Student_2.png",  # Corrected extension
        "prompt": (
            "Close-up lab work, hands interacting with equipment. Use THIS image as the visual base. "
            "Voice-over: '…and discovery becomes impact.'"
        ),
        "duration": 4
    },

    # Scene 4 — Lab Interior 3
    {
        "image": r"Data/images/lab_interior/Lab_Student_4.jpg",
        "prompt": (
            "Students working with engineering instruments. High-tech atmosphere. "
            "Use THIS real image as the source frame."
        ),
        "duration": 4
    },

    # Scene 5 — Lab Interior 4
    {
        "image": r"Data/images/lab_interior/Lab_Student_5.jpg",
        "prompt": (
            "Macro/mid-shot of tools, circuits, lab processes. Use THIS uploaded image. "
            "Subtle glowing highlights."
        ),
        "duration": 4
    },

    # Scene 6 — Collaboration 1
    {
        "image": r"Data/images/student_collab/Student_Colab_1.jpg",
        "prompt": (
            "Students collaborating in an FAU engineering space. Use this image as the visual basis. "
            "Voice-over: 'Collaboration drives every breakthrough…'"
        ),
        "duration": 4
    },

    # Scene 7 — Collaboration 2
    {
        "image": r"Data/images/student_collab/Student_Colab_2.jpg",
        "prompt": (
            "Students working together on laptops/hardware. Use THIS real photo. "
            "Voice-over: '…because engineering is never a solo journey.'"
        ),
        "duration": 8
    },

    # Scene 8 — Collaboration 3
    {
        "image": r"Data/images/student_collab/Student_Colab_3.jpg",
        "prompt": (
            "Energetic FAU team problem-solving moment. Base the video motion off THIS uploaded image."
        ),
        "duration": 4
    },

    # Scene 9 — Library / Study Space 1
    {
        "image": r"Data/images/hallways/Library_1.jpg",
        "prompt": (
            "Bright FAU library interior. Calm academic environment. "
            "Use this real image. Voice-over: 'Across FAU, every space is built to inspire creativity…'"
        ),
        "duration": 8
    },

    # Scene 10 — Library / Study Space 2
    {
        "image": r"Data/images/hallways/Library_2.jpg",
        "prompt": (
            "Quiet study area. Use THIS photo. "
            "Voice-over: '…focus, and growth.'"
        ),
        "duration": 4
    },

    # Scene 11 — Experiment Close-Up
    {
        "image": r"Data/images/student_collab/Experiment_1.jpg",
        "prompt": (
            "Macro close-up engineering experiment, glowing circuitry. Use this real uploaded image. "
            "Voice-over: 'Innovation happens one experiment… one design… one breakthrough at a time.'"
        ),
        "duration": 8
    },

    # Scene 12 — Palm Trees Transition
    {
        "image": r"Data/images/city_beach/Palm_trees_1.jpg",
        "prompt": (
            "Cinematic Florida palm trees, gentle breeze. Use THIS photo. "
            "Voice-over: 'And at FAU, your environment is as inspiring as your ambition.'"
        ),
        "duration": 8
    },

    # Scene 13 — Boca Raton City
    {
        "image": r"Data/images/city_beach/Boca_city_1.jpeg",
        "prompt": (
            "Beautiful Boca Raton coastline. Use THIS image. "
            "Voice-over: 'Just minutes from campus… the beauty of Boca Raton brings balance to every journey.'"
        ),
        "duration": 8
    },

    # Scene 14 — Ending Logo
    {
        "image": r"Data/images/logo_text/Ending_logo_1.png",
        "prompt": (
            "Professional FAU Engineering ending frame with centered logo. Use THIS uploaded file. "
            "Voice-over: 'Florida Atlantic University… College of Engineering. Where the future begins with you.'"
        ),
        "duration": 8
    }
]


# ----------------------------------------------------------
#  LOAD IMAGE — NOW MIME SAFE
# ----------------------------------------------------------
def load_image(path):
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        return types.Image(
            image_bytes=f.read(),
            mime_type=mime
        )


# ----------------------------------------------------------
#  GENERATE SCENE VIDEO — CLEAN INDEXED NAMES
# ----------------------------------------------------------
def generate_scene_video(image_path, prompt, duration, index):

    print(f"\n🎬 Processing Scene {index}:")
    print(f"   Image     : {image_path}")
    print(f"   Duration  : {duration}")
    print(f"   Prompt    : {prompt[:80]}...\n")

    img = load_image(image_path)

    # Removed "NO PEOPLE" because your images contain people
    full_prompt = (
        "Use the uploaded image EXACTLY as the visual basis. Do NOT replace people or objects. "
        "Create a subtle camera motion effect (push-in, parallax, or drift). "
        "Voice-over only narration; nobody should visibly talk.\n" +
        prompt
    )

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=full_prompt,
        image=img,
        config=types.GenerateVideosConfig(
            duration_seconds=duration,
            resolution="720p",
        )
    )

    # Wait for generation
    while not operation.done:
        print("⏳ Veo is generating... waiting...")
        time.sleep(10)
        operation = client.operations.get(operation)

    if operation.response is None:
        print("❌ Scene failed.")
        return None

    result = operation.response.generated_videos[0]

    filename = f"scene_{index}.mp4"
    download = client.files.download(file=result.video)

    if isinstance(download, (bytes, bytearray)):
        with open(filename, "wb") as f:
            f.write(download)

    elif isinstance(download, str):
        with open(download, "rb") as src, open(filename, "wb") as dst:
            dst.write(src.read())
        os.remove(download)

    print(f"✅ Saved as {filename}")
    return filename


# ----------------------------------------------------------
#  MAIN — GENERATE ALL INDIVIDUAL VIDEOS
# ----------------------------------------------------------
if __name__ == "__main__":
    outputs = []

    for i, scene in enumerate(scenes, start=1):
        out = generate_scene_video(
            image_path=scene["image"],
            prompt=scene["prompt"],
            duration=scene["duration"],
            index=i
        )
        if out:
            outputs.append(out)

    print("\n🎉 ALL SCENES GENERATED SUCCESSFULLY!")
    for x in outputs:
        print(" →", x)

    print("\nNow run your transition/merge script on these scene files.")
