from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2
import numpy as np


models_path = "models/"


def prepare_model(weights_path):
    base_model = InceptionV3(weights="imagenet",include_top=False)
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    predictions = tf.keras.layers.Dense(2, activation='softmax')(x)
    model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)
    model.compile(loss='categorical_crossentropy', optimizer="adam",metrics=['accuracy'])
    model.load_weights(weights_path)
    return model


ankle_ap_view = prepare_model(models_path + "Ankle_ap_view_best.hdf5")
ankle_lateral_view = prepare_model(models_path + "Ankle_lateral_view_best.hdf5")
ankle_oblique_view = prepare_model(models_path + "Ankle_oblique_view_best.hdf5")

foot_ap_view = prepare_model(models_path + "Foot_ap_view_best.hdf5")
foot_lateral_view = prepare_model(models_path + "Foot_lateral_view_best.hdf5")
foot_oblique_view = prepare_model(models_path + "Foot_oblique_view_best.hdf5")


views_to_label = {0:"Abnormal", 1:"Normal"}

def make_prediction(model, image):
    pred = model.predict(image)
    print(f"Prediction Done! --> {pred}")
    i = np.argmax(pred[0])
    label = views_to_label[i]
    return label, i

def load_image(img_path, shape, gray=False):
  img = load_img(img_path, target_size=shape)
  img = img_to_array(img)
  if gray:
      img = img.convert('L')
      img = np.asarray(img)/255
      img = img.reshape(1, img.shape[0], img.shape[1])
  else:
      img = np.asarray(img)/255
      img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
  return img
      