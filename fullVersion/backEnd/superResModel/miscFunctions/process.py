# normalises image data from the 0-255 rgb range to 0-1 range of values
def normalise(image):
    image = image / 255
    return image