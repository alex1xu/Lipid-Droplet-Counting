# Neuronal Cell Lipid Droplet Counting Software

> First-ever machine learning software to count lipid droplets in neuroblastoma cell lines

[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try) ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white) ![Keras](https://img.shields.io/badge/Keras-FF0000?style=for-the-badge&logo=keras&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-654FF0?style=for-the-badge&logo=SciPy&logoColor=white)

![Screenshot 2024-07-29 202600](https://github.com/user-attachments/assets/fac3c6ac-406f-4f0b-8f6d-3c1d6de584eb)

## Table of Contents

 * [Usage](#usage)
 * [Novel Pipeline Breakdown💃](#novel-pipeline-breakdown)
   * [Data Augmentation](#data-augmentation)
   * [U-Net Training](#u-net-training)
   * [Centroid Identification](#centroid-identification)
   * [Stain Subtraction](#stain-subtraction)
 * [Model Evaluation](#model-evaluation)

## Usage

1. Download the distribution file from the [releases page](https://github.com/alex1xu/Lipid-Droplet-Counting/releases).
   
2. Install the package:
```sh
pip install LDC-0.1-py3-none-any.whl
```

3. After installing the package, you can run the command using:
```sh
count /path/to/input_folder
```

In the current version, input images must be in standard pixel sizes such as 1024x768, or any multiples of 64.

## Novel Pipeline Breakdown

![Screenshot 2024-07-25 125837](https://github.com/user-attachments/assets/1c968439-58a2-4f92-9766-d384d0be18d1)

This repository contains a Python package for counting lipid droplets in images of Oil Red O-stained neuronal cells. It is designed to work with microscopy images by dividing them into smaller tiles for efficient processing. The main components are data augmentation, U-Net prediction, centroid identification, and stain subtraction.

### Data Sources and Augmentation

Microscopy images containing a total of approximately 4,000 Oil Red O-stained neuronal cell cultures at 50x magnification were obtained and manually segmented. Images and masks used for training were then cropped into 64x64 tiles. Minimal data preprocessing was applied. Image pixel values are normalized to a range of [0, 1]. 

A majority of tile masks were empty and contained no droplets. To account for this imbalance, my initial approach removed all empty masks. However, experimentation showed that a 1:1 ratio of tiles containing droplets and empty tiles was optimal.

![Screenshot 2024-07-26 125907](https://github.com/user-attachments/assets/bca708ba-fc8c-4656-b82a-0e63ed040611)

_Generated density maps of an empty tile for the two approaches to handling class imbalance. Yellow indicates a high probability of belonging to the positive class while blue indicates a low probability._

The dataset was split into training and validation sets in an 80:20 ratio. Data augmentation was applied to both the training and validation sets due to the low number of images. The following augmentations were applied using the Albumentations library:
 - CLAHE (Contrast Limited Adaptive Histogram Equalization)
 - Blur
 - Color Jitter
 - Sharpen
 - RGB Shift
 - Defocus
 - Hue, Saturation, and Value shift
 - Vertical and Horizontal Flip
 - Random Rotation
 - Grid Shuffle
 - Channel Dropout
 - Multiplicative Noise
 - Optical and Grid Distortion
 - Pixel Dropout

### U-Net Training

U-Net is a convolutional neural network designed for biomedical image segmentation tasks. It has a distinctive architecture that includes an encoder-decoder structure with skip connections.

The Contraction Path consisted of 4 downsampling blocks, each with:
 - Convolutional Layers: Apply two 3×3 convolutions with ReLU activation, followed by a dropout layer
 - MaxPooling Layer: Reduce spatial dimensions by a factor of 2

The Expansion Path consisted of upsampling blocks, each with:
 - Transpose Convolutional Layer: Upsample the feature maps
 - Concatenation with Skip Connection: Merge feature maps from the encoder
 - Convolutional Layers: Refine the combined features

A 1×1 convolution output layer reduced the feature maps for binary segmentation with a sigmoid activation function for pixel-wise classification.

The Adam optimizer is used with an initial learning rate of 5*10<sup>-4</sup>. U-Net trained for 6 epochs with a batch size of 32.

### Centroid Identification

The centroid detection function identified the centers of mass of segmented objects in output density maps. In the future, Hough circle transform may be used in place of centroid identification.

![Screenshot 2024-07-29 201711](https://github.com/user-attachments/assets/00db10bf-24cb-4ce5-86cb-cbb4dac354f7)

### Stain Subtraction

The stain subtraction technique isolates the background stained cells in images. Images were first converted to grayscale. Then, contrast enhancement and denoising techniques were applied. Otsu's thresholding is applied to extract a binary image. Finally, dilation was used to fill small gaps and remove small objects.

![Screenshot 2024-07-29 202349](https://github.com/user-attachments/assets/7a815a38-f299-4d23-9a89-d5aa087d8b33)

Centroids detected outside of cell stain masks are then removed to obtain the final droplet count. 

## Model Evaluation

The model predictions were manually verified through qualitative evaluation by a biomedicine professor with over 20 years of domain expertise. 

![Screenshot 2024-07-29 202600](https://github.com/user-attachments/assets/87f9c630-32d8-47cb-90fb-6bc385e7567f)

Comparison with human ground truths on a testing set are also shown below. Results indicate that for every 21.6 &pm; 5.0 cells in an image, one is miscounted.

![Screenshot 2024-07-29 204207](https://github.com/user-attachments/assets/a29d7512-bba4-4649-8b77-e0ca48ef35a6)
