class Model:
  def __init__(self):
    pass

"""

import numpy as np
from tensorflow.keras.models import load_model

class Model:
    def __init__(self):
        # Load our pre-trained UNet model
        self.model = load_model('model.h5')

    def predict(self, img):
        # Preprocess the image as required by our model
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        img = img / 255.0  # Normalization

        # Perform prediction
        prediction = self.model.predict(img)

        # Process the prediction (Binary classification: road blocked = 1, road clear = 0)
        if prediction[0] > 0.5:
            return 1
        else:
            return 0

"""