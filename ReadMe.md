# SecFePAS: Secure Facial-expression-based Pain Assessment at the Edge

**Paper:** [SecFePAS: Secure Facial-expression-based Pain Assessment with Deep Learning at the Edge](https://eprint.iacr.org/2025/1280.pdf)  
**Authors:** Kanwal Batool et al.

---

## Overview

SecFePAS is a multiphase project to enable **secure, privacy-preserving facial-expression-based pain assessment**.  
It consists of:

1. **Phase 1 – Dataset Preparation & CNN Model Development**  
2. **Phase 2 – Secure Model Compilation & MPC with Athos/EzPC**  
3. **Phase 3 – Secure Inference with OpenCheetah**

> **Note:** Due to privacy and IP restrictions, the **original PAIN dataset and secured model binaries are not included**.  
> Public users can run the **mock pipeline** using toy datasets and dummy secure inference files. [ToDo]

---

## Phase 1: Dataset & Model Development

- Notebooks: `notebooks/train_and_quantize.ipynb`
- Public models: toy dataset trained models (`phase1_dataset_models/toy_dataset/*.onnx`) [ToDo]
- Training & quantization demonstrated on open-source datasets
- Logs, evaluation metrics, and ONNX export procedures documented

---

## Phase 2: Secure Inference with Athos (EzPC)

- Folder: `phase2_athos/`
- Contains scripts for compiling models using Athos / EzPC
- Public mode: uses **toy ONNX models** to emulate MPC workflow [ToDo]
- Demonstrates:
  - Server / client compilation (`--role server` / `--role client`)
  - Preprocessing & fixed-point conversion
  - Running secure protocol (mocked for public)
  - Extracting MPC results & comparing against baseline ONNX

---

## Phase 3: Secure Inference with OpenCheetah

- Folder: `phase3_opencheetah/`
- Scripts & structure mimic OpenCheetah integration
- Public mode: uses dummy `.inp` files for demonstration
- Builds binaries and runs secure inference **without exposing real models or patient data**
- Includes helper scripts:
  - `mod_cpp.py`, `fix_dead_filter.py` (for safe mock processing) [ToDo]
  - Orchestration scripts to run server/client simulation

---

## Docker / Public Demo [ToDo]

We provide optional Docker setups to run **mock inference end-to-end**:

```bash
docker-compose build
docker-compose up server
docker-compose run --rm client
