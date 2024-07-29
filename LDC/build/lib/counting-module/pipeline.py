import os
import cv2
import numpy as np
from skimage import exposure, filters, morphology
from scipy import ndimage as ndi
from scipy.ndimage import label
import tensorflow as tf
TILE_SIZE=64

def normalize_image(image):
    return tf.cast(image, tf.float32) / 255.0

def to_binary(image):
    _,binary = cv2.threshold(image, 0.2, 1, cv2.THRESH_BINARY)
    return binary.astype(np.float32)

# Tile input image for inference
def tile_image(image):
    tiles = []
    img_shape = image.shape
    
    for i in range(img_shape[0] // TILE_SIZE):
        for j in range(img_shape[1] // TILE_SIZE):
            tiled_img = image[
                TILE_SIZE * i:min(TILE_SIZE * (i + 1), img_shape[0]),
                TILE_SIZE * j:min(TILE_SIZE * (j + 1), img_shape[1])
            ]
            tiles.append(tiled_img)
    
    return tiles

# Recombine tiles
def stitch_image(tiles,image):
    img_shape = image.shape
    rows = [
        np.concatenate(tiles[row_i * (img_shape[1] // TILE_SIZE):(row_i + 1) * (img_shape[1] // TILE_SIZE)], axis=1)
        for row_i in range(img_shape[0] // TILE_SIZE)
    ]
    
    return np.concatenate(rows,axis=0)

# Recombine centroid predictions
def stitch_centroids(centroids,image):
    img_shape = image.shape
    res = [(
            tile_centroid[0] + (i // (img_shape[1] // TILE_SIZE)) * TILE_SIZE,
            tile_centroid[1] + (i % (img_shape[1] // TILE_SIZE)) * TILE_SIZE)
        for i, tile_centroids in enumerate(centroids)
        for tile_centroid in tile_centroids]
    
    return res

# Extract cell background
def extract_stain(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = exposure.equalize_adapthist(gray, clip_limit=0.03)
    gray = filters.rank.mean_bilateral(gray, morphology.disk(30))
    gray = cv2.fastNlMeansDenoising(gray.astype(np.uint8), h=10)
    gray = cv2.bitwise_not(gray)
    gray = filters.unsharp_mask(gray, radius=1, amount=1)
    
    binary = gray > filters.threshold_otsu(gray)   
    binary = morphology.dilation(binary, morphology.disk(1))
    binary = morphology.remove_small_objects(binary.astype(bool), min_size=200)
    
    return binary.astype(np.float32)

def detect_centroids(feature_map):
    labeled_array, num_features = label(feature_map)
    centers = ndi.center_of_mass(feature_map, labeled_array, range(1, num_features+1))
    return centers

# Exclude centroids not present on stains
def filter_centroids(centroids,stain):
    return [centroid for centroid in centroids if stain[int(centroid[0])][int(centroid[1])]]

# Main function to make predictions on entire folder
def predict_folder(image_folder,model,verbose=False):
    res = {}
    for filename in os.listdir(image_folder):
        n_features = predict_image(os.path.join(image_folder, filename), model)
        res[filename] = n_features

        if verbose:
            print(f'{filename}: {n_features}')
    
    return res
        
# Make prediction on a single file
def predict_image(image_path,model):
    image = cv2.imread(image_path, cv2.COLOR_BGR2RGB)
    
    # Image pre processing
    working_image = normalize_image(image)
    stain = extract_stain(image)
    tiles = tile_image(working_image)
        
    # U-Net prediction
    preds = model.predict(np.array(tiles), verbose=False)
#     pred_image=stitch_image(preds,image)    # Predictions can be visualized if needed
    binaries = [to_binary(pred) for pred in preds]
    
    # Centroid identification
    centroids = [detect_centroids(binary) for binary in binaries]
    scaled_centroids = stitch_centroids(centroids,image)
    all_centroids = filter_centroids(scaled_centroids,stain)
            
    return len(all_centroids)