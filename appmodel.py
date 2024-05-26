from unet import ModelLoader
from blockageprediction import BlockageAlgorithm
import numpy as np

class Model:
  def __init__(self):
    self.unet = ModelLoader()
    self.blocka = BlockageAlgorithm()

  def predict_image(self, img):
    pred = self.unet.predict(np.expand_dims(img, 0))

    #mask post-processing
    msk = pred.squeeze()
    msk[msk >= 0.5] = 1
    msk[msk < 0.5] = 0
    msk_rgb = np.stack((msk,)*3, axis=-1)

    return msk, msk_rgb

    #show the mask and the segmented image
    # combined = np.concatenate([raw, msk, raw* msk], axis = 1)
    # plt.axis('off')
    # plt.imshow(combined)
    # plt.show()

  def predict_blockage(self, msk, filename):
    print(msk.shape)
    return self.blocka.input_from_mask(msk, filename)