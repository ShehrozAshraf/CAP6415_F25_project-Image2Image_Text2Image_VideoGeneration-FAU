import time
from google import genai

# ------------------------------------------
# 🔑 YOUR API KEY
# ------------------------------------------
client = genai.Client(api_key="AIzaSyCiSZh7gT3T663_5zuFhGV9zmTZRW5qzTE")

# ------------------------------------------
# 🔧 Load local image correctly for Veo
# ------------------------------------------
def load_image_bytes(path):
    with open(path, "rb") as f:
        return f.read()  # raw bytes


# ------------------------------------------
# 🎬 Image → Video with Veo 3.1
# ------------------------------------------
def generate_video_from_image(image_path, prompt):
    print("📤 Sending request to Veo 3.1...")

    # Load image bytes
    img_bytes = load_image_bytes(image_path)

    # Veo expects this structure:
    image_payload = {
        "imageBytes": img_bytes,
        "mimeType": "image/jpeg"
    }

    # Send request
    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        image=image_payload,  # <-- CORRECT FORMAT
        config={
            "durationSeconds": 8,       # 4, 6, or 8 seconds
            "resolution": "1080p",      # 720p or 1080p
            "aspectRatio": "16:9"
        }
    )

    # Poll until done
    while not operation.done:
        print("⏳ Veo is generating... waiting 10s")
        time.sleep(10)
        operation = client.operations.get(operation)

    print("✅ Video completed!")

    # Download result
    result_video = operation.response.generated_videos[0]
    client.files.download(file=result_video.video)
    result_video.video.save("FAU_building_veo.mp4")

    print("🎉 Saved: FAU_building_veo.mp4")


# ------------------------------------------
# 🚀 RUN
# ------------------------------------------
if __name__ == "__main__":
    IMAGE_PATH = r"Data\images\building_exterior\FAU_EE_Building_1.jpg",
    
    EXTRA_IMAGES:r"Data\images\lab_interior\Lab_Student_2.png", 
    r"Data\images\lab_interior\Lab_Student_4.png",
    r"Data\images\lab_interior\Lab_Student_5.png",


    PROMPT = (
        "Cinematic drone-style slow push-in toward the engineering building. "
        "Smooth parallax, soft lighting, realistic textures, natural motion."
    )

    generate_video_from_image(IMAGE_PATH, PROMPT)
