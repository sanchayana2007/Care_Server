import io
import os
import pandas as pd

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"../lib/google_ocr/GCP_OCR_Project-42d5f48097f0.json"

def extract_text(filename):
  # Instantiates a client
  client = vision.ImageAnnotatorClient()

  # The name of the image file to annotate
  file_name = os.path.abspath(filename)

  # Loads the image into memory
  with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

  image = types.Image(content=content)

  # Performs text detection on the image file
  response = client.text_detection(image=image)
  #print(response)
  texts = response.text_annotations
  df = pd.DataFrame(columns=['locale', 'description'])
  for text in texts:
    df = df.append(
        dict(
            locale=text.locale,
            description=text.description
        ),
        ignore_index=True
      )

  lines = df['description'][0].splitlines()
  #print(lines)
  return lines

#if __name__ == "__main__":
#  text = extract_text('/home/deb/Pictures/adhar_back.png')
