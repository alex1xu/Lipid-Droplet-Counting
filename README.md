# Neuronal Cell Lipid Droplet Counting Software

> First-ever machine learning software to count lipid droplets in neuroblastoma cell lines

[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try) ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white) ![Keras](https://img.shields.io/badge/Keras-FF0000?style=for-the-badge&logo=keras&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-654FF0?style=for-the-badge&logo=SciPy&logoColor=white)

![Screenshot 2024-07-26 133909](https://github.com/user-attachments/assets/971cf081-e559-4602-8124-dd499d6199a2)![Screenshot 2024-07-26 133846](https://github.com/user-attachments/assets/e0aa40e7-277b-4358-ab46-716cf6d39706)

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

## Novel Pipeline Breakdown

![Screenshot 2024-07-25 125837](https://github.com/user-attachments/assets/1c968439-58a2-4f92-9766-d384d0be18d1)

### Data Augmentation

Tiling, albumentations etc... balancing

![Screenshot 2024-07-26 125907](https://github.com/user-attachments/assets/bca708ba-fc8c-4656-b82a-0e63ed040611)

show images

### U-Net Training

Define layers, try to get architecture visualization

### Centroid Identification

Density maps
Center of mass detection on .... in the future hough transform for circle detection may be used in place of centroid identification

### Stain Subtraction

 1. Convert to grayscale to focus on intensity values
 2. Contrast Limited Adaptive Histogram Equalization (CLAHE) to enhance the local contrast
 3. Mean Bilateral Filtering and Non-Local Means Denoising to reduce noise without blurring the stain boundaries
 4. Otsu's thresholding to convert to a binary image
 5. Dilation to fill small gaps and remove small objects

![Screenshot 2024-07-26 135305](https://github.com/user-attachments/assets/24d98cf8-ceff-44b4-a971-2cfc13ff4181)

_Image stain automatically segmented_

Centroids detected outside of cell stain masks are then removed to obtain the final droplet count. 

## Model Evaluation

![Screenshot 2024-07-26 133909](https://github.com/user-attachments/assets/971cf081-e559-4602-8124-dd499d6199a2) ![Screenshot 2024-07-26 133846](https://github.com/user-attachments/assets/e0aa40e7-277b-4358-ab46-716cf6d39706)

![Screenshot 2024-07-26 130700](https://github.com/user-attachments/assets/713b8351-2ea0-4053-a25b-8b08c3680c22)

