from dotenv import load_dotenv
import os
from google import genai
from PIL import Image
from io import BytesIO

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Ask user for image description
prompt = input("Enter a description for the image: ")

# Generate the image
response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=prompt,  # just the text prompt
)

# Save the image
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save("generated_image.png")
        print("Image saved as generated_image.png")
    elif part.text is not None:
        print(part.text)