# Mohammad Shehroz Ashraf & Sher Ali
# FAU
# Project: Image2Image + Image2Video Video Generation for FAU Engineering

## Description

This project uses AI models to turn images and text into short cinematic videos about FAU’s College of Engineering. We experimented with text-to-image, image-to-image, and image-to-video generation. The final system uses Google Veo 3.1 to animate real FAU images into smooth video clips, and then uses FFmpeg to merge those clips into one promotional-style video with crossfades and clean transitions.

The goal of this project is to generate short and realistic videos from FAU images that represent FAU Engineering’s buildings, labs, student life, and local environment.

## Progress Summary

We worked on this project over four weeks.

- At first, we used text-to-image models such as Stable Diffusion and Gemini. These produced creative results, but most images were too abstract and did not match the real FAU Engineering campus.  
- We also tried NanoBanana for text-to-image, but the faces, buildings, and details were inconsistent and not usable in a realistic promotional video.  
- Next, we moved to image-to-image generation to stylize real FAU photos. This improved the look but still did not give us natural motion.  
- Finally, we switched to image-to-video generation using RIO-3 (Veo 3.1). Veo takes a single FAU image and generates a short cinematic clip with slow push-in, parallax, and realistic camera motion. These clips   looked much closer to an actual promotional video.  
- To complete the final film, we used FFmpeg and FFprobe to read each scene duration, compute transition offsets, and apply crossfades between clips. This produced one continuous final video with smooth and professional transitions.

## Dataset

Our dataset includes real images taken around FAU’s College of Engineering:

1. FAU Engineering and Computer Science building exteriors  
2. Labs and research spaces  
3. Student collaboration photos  
4. Hallways, library areas, and study spots  
5. Experiments and technical close-ups  
6. Palm trees and campus surroundings  
7. Boca Raton city and beach  
8. FAU logo and ending frame  

All images were captured manually and then used as inputs for the image-to-video pipeline.

## Project Structure

```text
project/
│── Data/
│   └── images/              # Original FAU images organized by scene     
│── output/
    └── FinalVideo/
    └── scenes/                
│── image2video.py           
│── multi-image2video.py     
│── transitions.py           
│── Final_compilation.py     
│── image_gen.py             
│── concat_list.txt          
│── .env                     
│── requirements.txt
│── README.md
```

## Dependencies

### Python (requirements.txt)

```
google-genai>=0.3.0
python-dotenv>=1.0.1
Pillow>=10.4.0
```

### System Dependencies (Required)

| Dependency | Purpose |
|-----------|---------|
| **FFmpeg ≥ 6.0** | Video transitions, encoding, merging |
| **FFprobe ≥ 6.0** | Extract scene durations |

Download FFmpeg here:  
https://ffmpeg.org/download.html

---
## Google AI Studio Requirements

### Models Used:
| Model | Purpose |
|-------|---------|
| **Veo 3.1** | Cinematic video generation |
| **Veo 3** | Preview / fallback |
| **Gemini 2.5 Flash Image Preview** | Image generation |

### important Note: **You MUST enable billing**  
Video generation via Veo requires billing enabled on Google Cloud.

### API Key Setup:

1. Go to **Google AI Studio**:  
   https://aistudio.google.com  
2. Create a **New API Key**  
3. Enable **Billing**  
4. Add your key to `.env`:

```
GEMINI_API_KEY=YOUR_KEY_HERE
```

## Running the Project

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Ensure FFmpeg is installed
Check installation:

```bash
ffmpeg -version
ffprobe -version
```

### 3. Generate scenes

```bash
python multi-image2video.py
```

Scenes will output as:

```
scene_1.mp4
scene_2.mp4
...
scene_14.mp4
```

### 4. Merge scenes into a final cinematic output

```bash
python transitions.py
```

You will get:

```
final_output_fixed.mp4
```

---
