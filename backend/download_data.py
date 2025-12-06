# backend/download_data.py
import io
import requests
import zipfile
import os
import shutil

print("Downloading MovieLens dataset...")

url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
response = requests.get(url)

print("Extracting files...")

with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    z.extractall(".")

# Move files to backend folder
shutil.move("ml-latest-small/movies.csv", "movies.csv")
shutil.move("ml-latest-small/ratings.csv", "ratings.csv")

# Delete the extracted folder
shutil.rmtree("ml-latest-small")

print("Done! movies.csv and ratings.csv are ready.")