import os
import requests
import zipfile
import io

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_DIR = "model"

if os.path.exists(MODEL_DIR):
    print(f"Model directory '{MODEL_DIR}' already exists. Skipping download.")
else:
    print(f"Downloading model from {MODEL_URL}...")
    try:
        r = requests.get(MODEL_URL)
        r.raise_for_status()
        print("Download complete. Extracting...")
        
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(".")
        
        # Rename the extracted folder to 'model'
        extracted_folder = "vosk-model-small-en-us-0.15"
        if os.path.exists(extracted_folder):
            os.rename(extracted_folder, MODEL_DIR)
            print(f"Model extracted and renamed to '{MODEL_DIR}'.")
        else:
            print(f"Error: Could not find extracted folder '{extracted_folder}'.")
            
    except Exception as e:
        print(f"Failed to download/extract model: {e}")
