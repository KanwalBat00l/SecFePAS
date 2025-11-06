# Secure Inference with **Athos (EzPC)**


| Model folder | Backend(s) | ONNX file |
|--------------|------------|-----------|
| `resnet50_fp32/` | `SCI_HE/`, `SCI_OT/` | `resnet50_fp32.onnx` |
| `resnet50_fp16/` | `SCI_HE/`, `SCI_OT/` | `resnet50_fp16.onnx` |
| `sqnet_fp32/`    | `SCI_HE/`, `SCI_OT/` | `sqnet_fp32.onnx`    |
| `sqnet_fp16/`    | `SCI_HE/`, `SCI_OT/` | `sqnet_fp16.onnx`    |

Each **backend folder** already contains a ready-to-run **`config.json`**, weights **`*.inp`**, sample image **`input.png`**, and starter scripts.

```
athos/
├── resnet50_fp32/
│   ├── SCI_HE/    
│   └── SCI_OT/     
├── resnet50_fp16/
├── sqnet_fp32/
└── sqnet_fp16/
scripts/            
```

---

## 1  Install EzPC & activate virtual-env

```bash
git clone https://github.com/mpc-msri/EzPC.git ~/EzPC
cd ~/EzPC
./setup_env_and_build.sh quick          # builds EzPC + dependencies
source mpc_venv/bin/activate            # ALWAYS do this before running python scripts
```

> The script creates **`~/EzPC/mpc_venv/`**.  
> All Python utilities below assume the venv is *active*.

---

## 2  Compile a model (once per backend)

### 2.1 Server side (`--role server`)

```bash
cd athos/resnet50_fp32/SCI_HE           # ⬅ choose any model/backend folder
python ~/EzPC/Athos/CompileONNXGraph.py \
       --config config.json             \
       --role   server
```

Outputs in the same folder:

* `resnet50_fp32_SCI_HE.out`   — compiled MPC binary  
* `resnet50_fp32_41_sci_HE0.cpp`  — cpp model file to be used as input for opencheetah
* `resnet50_fp32_input_weights_fixedpt_scale_15.inp` — fixed-pt weights  
* `client.zip` — **config + stripped ONNX** to send to the client

### 2.2 Client side (`--role client`)

```bash
cd athos/resnet50_fp32/SCI_HE
unzip client.zip                         # received from server
python ~/EzPC/Athos/CompileONNXGraph.py \
       --config config.json             \
       --role   client
```

Now both parties have identical binaries.

---

## 3  Pre-process an input & convert to fixed-point

All helper scripts are in **`athos/scripts/`**.

```bash
cd athos/resnet50_fp32/SCI_HE

# 3.1  Pre-process (makes input.npy from input.png)
python scripts/preprocess.py input.png input.npy --dtype float32


# 3.2  Convert to fixed-point (makes input_fixedpt_scale_15.inp)
python ~/EzPC/Athos/CompilerScripts/convert_np_to_fixedpt.py \
       --inp    input.npy \
       --config config.json
```

*The `scale` and `bitlength` are read from **`config.json`**.*

---

## 4  Run the secure protocol

Choose an open port (example: **`12345`**).

### 4.1 Server (machine A)

```bash
cd athos/resnet50_fp32/SCI_HE
./resnet50_fp32_SCI_HE.out \
    r=1              \
    port=12345       \
    < resnet50_fp32_input_weights_fixedpt_scale_15.inp \
```

### 4.2 Client (machine B)

```bash
cd athos/resnet50_fp32/SCI_HE
./resnet50_fp32_SCI_HE.out \
    r=2              \
    ip=<SERVER_IP>   \
    port=12345       \
    < input_fixedpt_scale_15.inp \
    > output.txt 2>&1
```

*`output.txt` capture the full log. Including the resources used, performance, bandwidth analysis.* 

---

**Each of the scripts here as well as in opencheetah folder have a clear input/output structure that is easy to discover using --help command. 

## 5  Extract MPC result & (optionally) verify against ONNX

```bash
# 5.1  Convert raw text → NumPy vector
python ~/EzPC/Athos/CompilerScripts/get_output.py \
       output.txt config.json         # → model_output.npy

# 5.2  Plain ONNX inference (baseline)
python ../../../scripts/run_onnx.py \
       input.npy                             \
       ../resnet50_fp32.onnx                 # path relative to this folder

# 5.3  Compare for sanity
python ~/EzPC/Athos/CompilerScripts/comparison_scripts/compare_np_arrs.py \
       onnx_output/input_output_for_resnet50_fp32.npy \
       model_output.npy
```

`compare_np_arrs.py` should report *“Arrays matched up to x decimal points”*. for the .inp files provided x is 2!

---

