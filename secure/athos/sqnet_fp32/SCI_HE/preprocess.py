import numpy as np, torchvision.transforms as T
from PIL import Image

img_path = "input.png" # Or any other image
img = Image.open(img_path).convert("RGB")

# THIS IS THE CORRECT PREPROCESSING FOR YOUR SQUEEZENET MODEL
sqnet_preprocess_tf = T.Compose([
        T.Resize(256), # Standard practice before a 224 crop
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
     ])

# Apply the transform
processed_img_tensor = sqnet_preprocess_tf(img)

# Add batch dimension and convert to NumPy array
# Output shape will be (1, 3, 224, 224)
sqnet_input_numpy = processed_img_tensor.unsqueeze(0).numpy().astype("float32")

# Save it (e.g., specifically for SqueezeNet)
np.save("input.npy", sqnet_input_numpy)
