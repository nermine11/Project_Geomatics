from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import base64
from pathlib import Path
import geojson

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

output_folder = Path("images")
output_folder.mkdir(exist_ok=True)


def scrape_images(keyword):

    formatted_keyword = keyword.replace(" ", "+")

    print(formatted_keyword)
    driver = webdriver.Chrome(options=options)
    driver.get(
        f"https://www.google.com/search?q={formatted_keyword}+monument&tbm=isch&brd_json=1"
    )

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
    with open("monuments_historiques.geojson", encoding="utf-8") as f:
        gj = geojson.load(f)

    references = []
    for feature in gj.get("features", []):
        references.append(feature.get("properties", {}).get("reference"))
    cpt = 0
    for ref in references:
        cpt += 1
        scrape_images(ref)
        print(cpt)


main()
