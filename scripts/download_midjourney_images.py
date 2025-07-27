import base64
import os

import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scripts.utils import name_to_key


def download_images(df: pd.DataFrame, name_col: str, url_col: str):
    os.makedirs("images", exist_ok=True)
    for idx, row in df.iterrows():
        name = row[name_col]
        url = row[url_col]
        key = name_to_key(name)
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        img_data = driver.execute_script("""
            var img = document.querySelector('img');
            var canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            return canvas.toDataURL('image/png').substring(22);
        """)

        with open(f"images/{key}.png", "wb") as f:
            f.write(base64.b64decode(img_data))

        driver.quit()


if __name__ == '__main__':
    df = pd.read_csv("archetypes.csv")
    download_images(df, "Nom", "midjourney url")