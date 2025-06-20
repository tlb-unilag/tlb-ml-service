import os
from PIL import Image
import numpy as np
import uuid
import cloudinary
import cloudinary.uploader
from ultralytics import YOLO
from dotenv import load_dotenv
import requests
from fastapi import HTTPException


load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CL_NAME"),
    api_key=os.getenv("CL_API_KEY"),
    api_secret=os.getenv("CL_SECRET")
)
classes = ['early', 'healthy', 'not_early']

model_path = os.getenv("MODEL_PATH")
print("loading detection model....")
prediction_model = YOLO(model_path)


async def get_detection_model():
    return prediction_model


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        raise HTTPException(status_code=500, detail="Unable to download image")


def predict(img_url, model):
    save_id = str(uuid.uuid4())
    download_id = str(uuid.uuid4())
    download_filename = f"{download_id}.jpg"
    download_image(img_url, download_filename)
    save = f"{save_id}.jpg"
    results = model.predict(source=download_filename)
    im_array = results[0].plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.save(save)  # save image
    upload_url = img_url
    if results[0].boxes.cls.numel() > 0:
        upload_url = upload_img(save, save_id)
    if os.path.exists(save):
        os.remove(save)
    if os.path.exists(download_filename):
        os.remove(download_filename)
    return results, upload_url, save_id


def upload_img(path, uuid_v4):
    response = cloudinary.uploader.upload(path,
                                          public_id=uuid_v4)
    return response['url']


def get_class_frequency(result):
    array = result.boxes.cls.numpy()
    unique_elements, counts = np.unique(array, return_counts=True)
    frequency_dict = dict(zip(unique_elements, counts))
    new_frequency_dict = {result.names[key]: value for key, value in frequency_dict.items() if
                          key in result.names}
    return new_frequency_dict


def prepare_all_class_count(frequency_dict):
    all_class_count = {taro_class: frequency_dict[taro_class] if taro_class in frequency_dict else 0 for
                       taro_class in classes}
    return all_class_count
