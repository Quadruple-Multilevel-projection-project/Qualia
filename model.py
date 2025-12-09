import tensorflow as tf
from tensorflow.keras.layers import Conv3D, MaxPooling3D, Flatten

def cnn_5d_to_3d(input_data):
    model = tf.keras.Sequential([
        Conv3D(64, kernel_size=(3,3,3), activation='relu', input_shape=input_data.shape[1:]),
        MaxPooling3D(pool_size=(2,2,2)),
        Flatten()
    ])
    return model.predict(input_data)
