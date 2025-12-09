from image_gen import generate_image_from_text
from image2video import generate_video_from_image

# Here is an example usage to run
generate_image_from_text("FAU Engineering building image")
generate_video_from_image(
    image_path="Data/Data/images/Test_Image_1.jpeg",
    prompt="Cinematic video of FAU engineering building"
)
