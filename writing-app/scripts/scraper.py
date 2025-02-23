import os
import re
import shutil
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://sona.pona.la/wiki/sitelen_pona"
IMAGE_DIR = "sitelen_glyphs"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_glyph_images():
    """Fetches and downloads all Sitelen Pona glyph images from the wiki page."""
    # Create directory if it doesn't exist
    os.makedirs(IMAGE_DIR, exist_ok=True)

    # Fetch the webpage content with headers
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {response.status_code}")
        return

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all images inside the wiki content
    images = soup.find_all("img")

    print(f"Found {len(images)} images. Downloading...")

    for img in images:
        img_url = img.get("src")
        if not img_url:
            continue  # Skip if src is missing

        # Ensure full URL
        full_img_url = urljoin(BASE_URL, img_url)

        # Extract image filename
        img_name = img_url.split("/")[-1]
        img_path = os.path.join(IMAGE_DIR, img_name)

        # Download the image with headers
        try:
            img_data = requests.get(full_img_url, headers=HEADERS).content
            with open(img_path, "wb") as f:
                f.write(img_data)
            print(f"Downloaded: {img_name}")
        except Exception as e:
            print(f"Failed to download {img_name}: {e}")


def rename_glyph_files():
    """Renames glyph files according to the specified pattern."""
    # Create renamed directory
    renamed_dir = os.path.join(IMAGE_DIR, "renamed_svg")
    os.makedirs(renamed_dir, exist_ok=True)

    # Pattern to match files like 'A_-_sitelen_pona_pu_%28monospaced%29.svg'
    pattern = r"^([A-Za-z]+)_-_sitelen_pona_pu_%28monospaced%29.svg$"

    # Iterate through files in the directory
    for filename in os.listdir(IMAGE_DIR):
        if not filename.endswith(".svg"):
            continue

        match = re.match(pattern, filename)
        if match:
            # Extract the character and create new filename
            character = match.group(1).lower()
            new_filename = f"{character}.svg"

            # Source and destination paths
            src_path = os.path.join(IMAGE_DIR, filename)
            dst_path = os.path.join(renamed_dir, new_filename)

            # Copy and rename the file
            shutil.copy2(src_path, dst_path)
            print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    fetch_glyph_images()
    rename_glyph_files()
