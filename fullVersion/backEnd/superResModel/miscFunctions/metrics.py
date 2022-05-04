def getPsnr(gTruth, pred):
    
    # denormalises the image data back into 0-255 integer rgb range
    gTruth = gTruth * 255
    gTruth = tf.cast(gTruth, tf.uint8)
    gTruth = tf.clip_by_value(gTruth, 0, 255)
    
    pred = pred * 255
    pred = tf.cast(pred, tf.uint8)
    pred = tf.clip_by_value(pred, 0, 255)
    
    # calculates the PSNR using tf.image.psnr and returns the value
    return tf.image.psnr(gTruth, pred, max_val=255)