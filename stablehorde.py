import requests
import json
from time import sleep
import re
import math
import urllib.request
import os

def generate_image(style, alt, img_src, STABLEHORDE_API_KEY, local_directory):
    try:
        if style is None:
            # Default values if style is not provided
            width_adjusted = 64 * math.ceil(400 / 64)
            height_adjusted = 64 * math.ceil(300 / 64)
        else:
            # Extract width and height from the style string
            width_search = re.search(r'width:\s*(\d+)px', style)
            height_search = re.search(r'height:\s*(\d+)px', style)

            if width_search and height_search:
                width = int(width_search.group(1))
                height = int(height_search.group(1))
                # Adjust width and height to the nearest multiple of 64
                width_adjusted = 64 * math.ceil(width / 64)
                height_adjusted = 64 * math.ceil(height / 64)
            else:
                # Default values if width and height are not found
                width_adjusted = 64 * math.ceil(400 / 64)
                height_adjusted = 64 * math.ceil(300 / 64)

        # Make a POST request to the Stablehorde API
        url = "https://stablehorde.net/api/v2/generate/async"
        headers = {
            "Content-Type": "application/json",
            "apikey": STABLEHORDE_API_KEY,
        }
        body = {
            "prompt": (alt or "Generate a beautiful image") + " ### poorly drawn face, cloned face, poorly drawn animal, disfigured, mutilated, ugly, strange eyes, out of frame",
            "params": {
                "steps": 30,
                "n": 1,
                "sampler_name": "k_euler",
                "post_processing": ['GFPGAN'],
                "width": width_adjusted,
                "height": height_adjusted,
                "cfg_scale": 7,
                "seed_variation": 1000,
            },
            "nsfw": False,
            "censor_nsfw": True,
            "models": ["stable_diffusion"],
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise an error for bad responses
        response_json = response.json()
        
        if "id" not in response_json:
            print("Error: API response does not contain 'id'")
            print(response_json)
            return None

        image_id = response_json["id"]
        status_url = f"https://stablehorde.net/api/v2/generate/status/{image_id}"
        
        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                status_response = requests.get(status_url)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                if status_data.get("done"):
                    if not status_data.get("generations"):
                        print("No generations in response")
                        return None
                    
                    image_url = status_data["generations"][0]["img"]
                    # Create images directory if it doesn't exist
                    images_dir = os.path.join(local_directory, "images")
                    os.makedirs(images_dir, exist_ok=True)
                    
                    # Generate a unique filename
                    base_name = os.path.splitext(os.path.basename(img_src))[0]
                    local_image_path = os.path.join(images_dir, f"{base_name}.webp")
                    
                    # Download the image
                    urllib.request.urlretrieve(image_url, local_image_path)
                    print(f"Image generated successfully: {local_image_path}")
                    return local_image_path
                
                wait_time = status_data.get("wait_time", 5)
                print(f"Waiting {wait_time} seconds for image generation...")
                sleep(wait_time)
                retry_count += 1
                
            except Exception as e:
                print(f"Error during status check: {str(e)}")
                sleep(5)
                retry_count += 1

        print("Max retries reached while waiting for image generation")
        return None

    except Exception as e:
        print(f"Error in generate_image: {str(e)}")
        return None
