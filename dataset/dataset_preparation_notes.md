# Dataset Preparation Notes for "PAIN" Dataset

## 1. Dataset Source and Overview

The "PAIN" image dataset, consisting of pre-extracted face crops, was provided via a Google Drive link: `https://drive.google.com/drive/folders/1RARwImoZgenV6Kdl_jiLsUK01HV61gkA?usp=drive_link`.

The dataset is organized into four class folders, numerically labeled '0', '1', '2', and '3'.

Initial class distribution (as loaded by the notebook):
*   Class 0: 3092 images
*   Class 1: 2909 images
*   Class 2: 2351 images
*   Class 3: 3109 images
*   **Total Images:** 11461

## 2. Data Splitting

The dataset was split into training and validation (test) sets using an 80-20 ratio. The split was performed using `sklearn.model_selection.train_test_split` with stratification (`stratify=labels`) to ensure proportional representation of each class in both sets. A `random_state=42` was used for reproducibility.

*   **Training set size:** 9168 images (80%)
*   **Validation/Test set size:** 2293 images (20%)

## 3. Data Preprocessing and Augmentation

The following PyTorch `transforms` were applied:

**Training Set Transforms (`train_tf`):**
*   `transforms.RandomResizedCrop(224, scale=(0.6,1.0))`: Randomly crops a region of the image and resizes it to 224x224. The scale parameter ensures that between 60% and 100% of the original image area is included.
*   `transforms.RandomHorizontalFlip()`: Horizontally flips the image with a 50% probability.
*   `transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1)`: Randomly changes the brightness, contrast, saturation, and hue of an image.
*   `transforms.ToTensor()`: Converts the PIL Image to a PyTorch tensor (scales pixel values to [0, 1]).
*   `transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])`: Normalizes the tensor image with ImageNet's mean and standard deviation.

**Validation/Test Set Transforms (`val_tf`):**
*   `transforms.Resize(256)`: Resizes the image to 256x256 pixels.
*   `transforms.CenterCrop(224)`: Crops the center 224x224 portion of the image.
*   `transforms.ToTensor()`: Converts the PIL Image to a PyTorch tensor.
*   `transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])`: Normalizes the tensor image.

## 4. Handling Class Imbalance (During Training)

The training dataset exhibited some class imbalance:
*   Training class counts (before sampling):
    *   Class 0: 2473
    *   Class 1: 2327
    *   Class 2: 1881
    *   Class 3: 2487

To address this, `torch.utils.data.WeightedRandomSampler` was used for the training `DataLoader`. This sampler assigns weights to each sample inversely proportional to its class frequency, effectively oversampling minority classes and undersampling majority classes during batch creation.

Per-class sampling weights (inverse frequencies):
*   Class 0: ~0.0004044
*   Class 1: ~0.0004297
*   Class 2: ~0.0005316
*   Class 3: ~0.0004021

## 5. Transfer Learning Strategy

Transfer learning was employed for both ResNet50 and SqueezeNet models.

**ResNet50:**
*   Pre-trained weights: `ResNet50_Weights.IMAGENET1K_V2`.
*   All parameters were initially frozen.
*   The following layers were unfrozen for fine-tuning: `layer2`, `layer3`, and `layer4`.
*   The final fully connected layer (`model.fc`) was replaced with a new `nn.Linear` layer with `NUM_CLASSES` (4) outputs.

**SqueezeNet (squeezenet1_1):**
*   Pre-trained weights: `pretrained=True` (equivalent to `SqueezeNet1_1_Weights.IMAGENET1K_V1`).
*   All parameters were initially frozen.
*   The following Fire modules were unfrozen for fine-tuning: `features.12` (fire7) and `features.14` (fire8).
*   The original classifier was replaced with a new `nn.Sequential` block:
    ```
    nn.Dropout(p=0.5),
    nn.Conv2d(512, NUM_CLASSES, kernel_size=1),
    nn.ReLU(inplace=True),
    nn.AdaptiveAvgPool2d((1,1))
    ```

