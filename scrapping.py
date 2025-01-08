from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import requests
from time import sleep
import base64
import geojson

options = webdriver.ChromeOptions()
output_folder = Path("images")
def scrape_images(keyword):

    formatted_keyword = keyword.replace(" ", "+")
    
    print(formatted_keyword)
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.google.com/search?q={formatted_keyword}&tbm=isch&brd_json=1")

    try:
        first_image = driver.find_element(By.CSS_SELECTOR, "g-img > img")
        img_url = first_image.get_attribute("src")

        if img_url.startswith("data:image"):

            base64_binary = img_url.split("base64,")[-1]
            mime_type = img_url.split(";")[0].split(":")[1]
            file_extension = mime_type.split("/")[-1]
            filename = f"{keyword}.{file_extension}"

            image_binary = base64.b64decode(base64_binary)
            output_path = output_folder.joinpath(filename)

            with open(output_path, "wb") as file:
                file.write(image_binary)
    except Exception as e:
        print(e)
    finally:
          driver.quit()


def main():
    with open("monuments_historiques.geojson") as f:
        gj = geojson.load(f)

    references = []
    for feature in gj.get("features", []):
        references.append(feature.get("properties", {}).get("reference"))

    for ref in references:
        scrape_images(ref)

main()