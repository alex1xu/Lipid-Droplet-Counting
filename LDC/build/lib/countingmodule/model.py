import tensorflow as tf
TILE_SIZE=64

def downsample_block(n_filters,prev_layer):
    c1 = tf.keras.layers.Conv2D(n_filters, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(prev_layer)
    c1 = tf.keras.layers.Dropout(0.1)(c1)
    c1 = tf.keras.layers.Conv2D(n_filters, (3, 3), activation='relu',kernel_initializer='he_normal', padding='same')(c1)
    p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1)
    return c1,p1

def upsample_block(n_filters,prev_layer,skip_layer):
    u1 = tf.keras.layers.Conv2DTranspose(n_filters, (2, 2), strides=(2, 2), padding='same')(prev_layer)
    u1 = tf.keras.layers.concatenate([u1, skip_layer])
    c1 = tf.keras.layers.Conv2D(n_filters, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u1)
    c1 = tf.keras.layers.Dropout(0.1)(c1)
    c1 = tf.keras.layers.Conv2D(n_filters, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
    return c1,u1

# Creates U-Net model
def build_unet_model():
    # Input layer
    inputs = tf.keras.layers.Input((TILE_SIZE, TILE_SIZE, 3))
    
    # Normalization
    s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)

    # Contraction Path
    c1,p1=downsample_block(16,s)
    c2,p2=downsample_block(32,p1)
    c3,p3=downsample_block(64,p2)
    c4,p4=downsample_block(128,p3)
    
    # Bottleneck layer
    c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
    c5 = tf.keras.layers.Dropout(0.2)(c5)
    c5 = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)

    # Expansion Path
    c6,u6=upsample_block(128,c5,c4)
    c7,u7=upsample_block(64,c6,c3)
    c8,u8=upsample_block(32,c7,c2)
    c9,u9=upsample_block(16,c8,c1)

    # Output layer for density map
    outputs = tf.keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)
    
    return inputs,outputs