import os
import argparse
import tensorflow as tf
from countingmodule import model
from countingmodule import pipeline 
import warnings

TILE_SIZE = 64
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
warnings.filterwarnings("ignore")

def main():
    parser = argparse.ArgumentParser(description='Count lipid droplets in microscopy images')
    parser.add_argument('input_folder', type=str, help='Path to the input folder')
    args = parser.parse_args()
    input_folder = args.input_folder
    
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
        return
    else:
        inputs,outputs=model.build_unet_model()
        unet_model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
        current_dir = os.path.dirname(__file__)
        weights_path = os.path.join(current_dir, 'working.weights.h5')
        unet_model.load_weights(weights_path)

        pipeline.predict_folder(input_folder,unet_model,verbose=True)

if __name__ == '__main__':
    main()