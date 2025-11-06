# OpenCheetah
---

##  1. Setup Instructions

### Step 1: Clone OpenCheetah

I recommend placing OpenCheetah **outside** the Athos folder:

```bash
git clone https://github.com/Alibaba-Gemini-Lab/OpenCheetah.git
cd OpenCheetah
```

### Step 2: Install Dependencies

```bash
bash scripts/build-deps.sh
```

This will install necessary libraries including SEAL, Eigen3, emp-toolkit, etc., into the `build` directory.

---

## 2. Code Replacement

After dependency setup, follow these steps to integrate the customized code:

### 2.1. Replace Scripts

```bash
cp -f ../opencheetah/scripts/build.sh scripts/build.sh
```

### 2.2. Replace `networks` Folder

```bash
rm -rf networks
cp -r ../opencheetah/network networks
```

### 2.3. Replace `SCI/networks` Folder

```bash
rm -rf SCI/networks
cp -r networks/sci SCI/networks
```

### 2.4. Replace Top-Level CMakeLists.txt

```bash
cp -f ../opencheetah/scripts/CMakeLists.txt .
```

### 2.5. Replace SCI Networks CMakeLists.txt

```bash
cp -f ../opencheetah/scripts/SCI/CMakeLists.txt SCI/networks/CMakeLists.txt
```

---

##  3. Build All Binaries

From the root of OpenCheetah:

```bash
bash scripts/build.sh
```

This builds the following binaries in `build/bin/`:

- `resnet50-cheetah`
- `resnet50-SCI_HE`
- `resnet50_quantized-cheetah`
- `resnet50_quantized-SCI_HE`
- `sqnet-cheetah`
- `sqnet-SCI_HE`
- `sqnet_quantized-cheetah`
- `sqnet_quantized-SCI_HE`

---

## 4. Understanding the Code Generation

The `.cpp` files inside `networks/` and `networks/sci/` are generated using scripts provided under `scripts/`:

- `mod_cpp.py`: 
  Automatically modifies the generated `.cpp` files to be compatible with OpenCheetah conventions (e.g., switching wrappers, modifying globals, conditional compilation). It simplifies tedious manual edits.

- `fix_dead_filter.py`: 
  Scans the input weight files and corrects any filters that are entirely zero. This is important to avoid runtime errors in OpenCheetah, particularly:  
  `conv2DOneFilter: filter with all zero is not supported`.

The .inp files and .cpp files you moved to networks and pretrained folder have already been preprocessed with these two scripts.

---

## 5. Available Inference Combinations

Each of the following binary variants can be executed using either `run-server.sh` or `run-client.sh`:

| Model               | Backend     | Binary Name                   |
|--------------------|-------------|-------------------------------|
| ResNet50 (FP32)     | SCI_HE      | `resnet50-SCI_HE`            |
|                    | Cheetah     | `resnet50-cheetah`           |
| ResNet50 (Quantized)| SCI_HE      | `resnet50_quantized-SCI_HE`  |
|                    | Cheetah     | `resnet50_quantized-cheetah` |
| SqueezeNet (FP32)   | SCI_HE      | `sqnet-SCI_HE`               |
|                    | Cheetah     | `sqnet-cheetah`              |
| SqueezeNet (Quant.) | SCI_HE      | `sqnet_quantized-SCI_HE`     |
|                    | Cheetah     | `sqnet_quantized-cheetah`    |

The input files for each combination are present in the `pretrained/` directory.

---
