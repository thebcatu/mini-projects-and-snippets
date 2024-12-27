import os
import requests
from bs4 import BeautifulSoup

def download_images_from_html(html_path, save_path="images"):
    """
    Extracts and downloads high-quality images from the provided HTML file.

    Args:
        html_path (str): Path to the saved HTML file.
        save_path (str): Directory to save downloaded images.

    Returns:
        None
    """
    # Create the save directory if it does not exist
    os.makedirs(save_path, exist_ok=True)

    # Open and parse the HTML file
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find all image tags
    images = soup.find_all("img")
    if not images:
        print("No images found in the HTML file.")
        return

    print(f"Found {len(images)} images. Downloading...")

    for idx, img in enumerate(images, start=1):
        # Extract the high-resolution image URL from the srcset attribute (if available)
        srcset = img.get("srcset")
        if srcset:
            # Choose the largest image in the srcset
            urls = [entry.split(" ")[0] for entry in srcset.split(",")]
            img_url = urls[-1]  # The last entry is usually the highest resolution
        else:
            img_url = img.get("src")

        if not img_url:
            print(f"Image {idx} has no valid URL.")
            continue

        # Download the image
        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                img_ext = os.path.splitext(img_url)[-1].split("?")[0]  # Handle URLs with query params
                img_name = f"slide_{idx:03}{img_ext}"
                img_path = os.path.join(save_path, img_name)

                with open(img_path, "wb") as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)

                print(f"Downloaded: {img_name}")
            else:
                print(f"Failed to download image {idx}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading image {idx}: {e}")

if __name__ == "__main__":
    html_file_path = input("Enter the path to the saved SlideShare HTML file: ").strip()
    image_save_dir = "downloaded_images"
    
    if os.path.exists(html_file_path):
        download_images_from_html(html_file_path, image_save_dir)
        print(f"Images saved in: {os.path.abspath(image_save_dir)}")
    else:
        print("HTML file not found. Please provide a valid path.")
