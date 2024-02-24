import os
import shutil
import numpy as np
import uuid
import cloudinary
import cloudinary.uploader
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CL_NAME"),
    api_key=os.getenv("CL_API_KEY"),
    api_secret=os.getenv("CL_SECRET")
)
classes = ['taro_late', 'taro_mid', 'taro_early', 'taro_healthy']

model_path = os.getenv("MODEL_PATH")
print("loading detection model....")
prediction_model = YOLO(model_path)


def get_detection_model():
    return prediction_model


def predict(img_url, model):
    save_path = 'runs/detect/predict'
    id = str(uuid.uuid4())
    filename = os.path.basename(img_url)
    results = model.predict(source=img_url, save=True)
    upload_url = img_url
    if results[0].boxes.cls.numel() > 0:
        save_full_path = os.path.join(save_path, filename)
        upload_url = upload_img(save_full_path, id)
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    if os.path.exists(filename):
        os.remove(filename)
    return results, upload_url, id


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
