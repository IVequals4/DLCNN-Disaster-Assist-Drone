import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import color
from skimage import io

class Controller:
  def __init__(self, model, view):
    self.model = model
    self.view = view

  def perform_inference(self, input_img):
    if input_img:
      img = np.array(input_img.resize((128, 128), Image.Resampling.LANCZOS))  # Example resize to match model input
      prediction = self.model.predict(img)
      if prediction == 1:
          self.status_label.config(text="Road Blocked")
      else:
          self.status_label.config(text="Road Clear")

  def predict_roads(self, img, filename):
    img = np.array(img.resize((512, 512)))/255.
    img = img[:,:,0:3]
    msk, msk_rgb = self.model.predict_image(img)
    # print(msk.shape())
    plt.imshow(msk_rgb)
    plt.savefig(f'{filename} mask.png')
    # print(msk.shape)
    # msk = color.rgb2gray(msk)
    # plt.imshow(msk)
    # plt.savefig(f'mask after conversion.png')
    status = self.predict_blockages(msk, filename)
    print(f'Blocked Detected is: {status}')

    return (msk_rgb, status)


  def predict_blockages(self, msk, filename):
    return self.model.predict_blockage(msk, filename)

    # msk_img = Image.open(msk)
    # msk_img.save('mask.png')
    # self.model.predict(img)

    # plt.axis([0, img_size[0], -img_size[0], 0])
    # plt.imshow(msk)
    # plt.clf()

    
