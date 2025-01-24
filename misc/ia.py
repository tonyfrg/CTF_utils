from PIL import Image
import numpy as np
import os
from transformers import pipeline

coordonnees = [] #for the challenge, the pics are sorted by coords

pipe = pipeline("image-classification", model="Dricz/cat-vs-dog-resnet-50")

images_folder = "path/to/folder"
for filename in os.listdir(images_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        image_path = os.path.join(images_folder, filename)
        image = Image.open(image_path)
        result = pipe(image)
        label = result[0]['label']
        score = result[0]['score']
        if label=='dog':
            coordonnees.append(filename.replace(".jpg","").split("_"))

#now, we made the flag with piwels
largeur, hauteur = 500, 500
image = Image.new('1', (largeur, hauteur), color=0)
pixels = image.load()
for (x, y) in coordonnees:
    if 0 <= int(x) < largeur and 0 <= int(y) < hauteur:
        pixels[int(x), int(y)] = 1 #blanc
image.save('flag.png')