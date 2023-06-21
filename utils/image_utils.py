import io
import os
import subprocess
from pathlib import Path
from typing import List

from fastapi import UploadFile
from PIL import Image, ImageChops, ImageOps


def trim_border(image: Image.Image, border_color=(255, 255, 255)) -> Image.Image:
    rgb_image = image.convert("RGB")
    # Exclude alpha value
    bg = Image.new('RGB', rgb_image.size, border_color)
    diff = ImageChops.difference(rgb_image, bg)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    else:
        raise ValueError("Unable to trim border from image.")


async def process_images(files: List[UploadFile], local_image_path: Path):
    images = []
    # Read files into PIL Images
    for file in files:
        content = await file.read()  # async read
        img = Image.open(io.BytesIO(content))
        if img.format != 'PNG':
            raise ValueError("All files must be in PNG format.")
        images.append(img)

    # Trim existing white space
    images = [trim_border(img) for img in images]
    # Add 16px of white border to each image
    images = [ImageOps.expand(img, border=16, fill='white')
              for img in images]

    if len(images) > 1:

        # Create a new image composed of the first image on top of the second image
        widths, heights = zip(*(i.size for i in images))
        max_width = max(widths)
        total_height = sum(heights)
        new_img = Image.new('RGB', (max_width, total_height), "white")

        y_offset = 0
        for img in images:
            x_offset = (max_width - img.width) // 2
            new_img.paste(img, (x_offset, y_offset))
            y_offset += img.height

    else:
        new_img = images[0]

    temp_path = Path("temp").joinpath("temp_image.png")

    # Save the image to a temporary file
    new_img.save(temp_path)

    # Create dir and parent dirs if not exists
    local_image_path.parent.mkdir(parents=True, exist_ok=True)

    # Use pngquant to compress the image
    subprocess.run(['pngquant', '--force', '--output',
                     str(local_image_path), str(temp_path)])
    
    os.remove(temp_path)
