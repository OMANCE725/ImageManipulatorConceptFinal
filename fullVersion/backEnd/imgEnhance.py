import os
import tensorflow as tf
import numpy as np
import PIL
from PIL import Image

from backEnd.superResModel.miscFunctions.metrics import getPsnr
from backEnd.superResModel.miscFunctions.process import normalise

tf.config.set_visible_devices([], 'GPU')

class Enhance:
    
    def __init__(self):
        
        self.modelSR = self.__getModel()
        
    # Method to import the Super Resolution Model
    def __getModel(self):
        # the directory path to where the model is saved
        loadPath = os.path.join("backEnd/superResModel/savedModel")
        
        # importing the model including the custom psnr metric
        return(tf.keras.models.load_model(loadPath, custom_objects={"getPsnr": getPsnr}))
    
    # method to upscale an image using the Super Resolution Model
    def upscaleImage(self, imagePIL):
    
        # converts to ycbcr and extracts the luma component
        ycbcr = imagePIL.convert("YCbCr")
        y, cb, cr = ycbcr.split()
        
        # converts into a NumPy array and normalises the data
        y = tf.keras.utils.img_to_array(y)
        y = normalise(y.astype("float32"))
        
        modelInput = np.expand_dims(y, axis=0)
        
        # use the model to create a prediction from the given input
        modelOut = self.modelSR.predict(modelInput)
        
        yUpscaled = modelOut[0]
        
        # denormalises the upscaled y-component back into the 0-255 RGB range
        yUpscaled = yUpscaled * 255
        
        # ensures the values fit within the RGB range
        yUpscaled = yUpscaled.clip(0, 255)
        
        # reshapes the y-component and converts to PIL
        yUpscaled = yUpscaled.reshape((np.shape(yUpscaled)[0], np.shape(yUpscaled)[1]))
        yUpscaled = PIL.Image.fromarray(np.uint8(yUpscaled), mode="L")
        
        # resizes the other components to the same size as the upscaled y-component
        cbUpscaled = cb.resize(yUpscaled.size, PIL.Image.BICUBIC)
        crUpscaled = cr.resize(yUpscaled.size, PIL.Image.BICUBIC)
        
        # merges the upscaled components and converts to RGB
        upscaledImg = PIL.Image.merge("YCbCr", (yUpscaled, cbUpscaled, crUpscaled)).convert("RGB")
        
        return upscaledImg
