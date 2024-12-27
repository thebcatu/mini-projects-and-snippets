import os
import requests
from bs4 import BeautifulSoup

def download_slideshare_document(url, save_path="downloads"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        document_title = soup.title.string.strip().replace(" ", "_") if soup.title else "slideshare_document"

        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, f"{document_title}.html")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(soup.prettify())

        return f"Document saved at {file_path}"
    else:
        return f"Failed to fetch the document. Status code: {response.status_code}"

if __name__ == "__main__":
    slideshare_url = input("Enter the SlideShare document URL: ").strip()
    result = download_slideshare_document(slideshare_url)
    print(result)
