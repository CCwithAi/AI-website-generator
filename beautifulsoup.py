import re
from bs4 import BeautifulSoup
from stablehorde import generate_image
import os

URL_PATTERN = r'url\(["\']?(?P<url>[^\)]+?)["\']?\)'

def generate_images(html_content, STABLEHORDE_API_KEY, local_directory):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        image_elements = soup.find_all("img")
        image_count = 1

        for image_element in image_elements:
            alt = image_element.get("alt", "A beautiful generated image")
            img_src = image_element.get("src", f"image_{image_count}.webp")
            style = image_element.get("style", "width: 400px; height: 300px;")
            
            image_path = generate_image(style, alt, img_src, STABLEHORDE_API_KEY, local_directory)
            if image_path:
                image_name = os.path.basename(image_path)
                image_element["src"] = f"./images/{image_name}"
            else:
                # Use a placeholder if image generation fails
                image_element["src"] = f"./images/placeholder_{image_count}.webp"
            image_count += 1

        # Process images in CSS
        style_elements = soup.find_all("style")
        for style_element in style_elements:
            css_content = style_element.string
            if css_content:
                css_urls = re.findall(URL_PATTERN, css_content)
                for css_url in css_urls:
                    image_path = generate_image(None, f"Generate a beautiful realistic photo for a background picture of a banner: {css_url}", 
                                             f"background_{image_count}.webp", STABLEHORDE_API_KEY, local_directory)
                    if image_path:
                        image_name = os.path.basename(image_path)
                        new_url = f'./images/{image_name}'
                        css_content = css_content.replace(css_url, new_url)
                    image_count += 1
                style_element.string.replace_with(css_content)

        return str(soup)
    except Exception as e:
        print(f"Error in generate_images: {str(e)}")
        return html_content  # Return original content if image generation fails
